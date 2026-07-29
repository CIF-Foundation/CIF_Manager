#!/bin/sh
# launch_lvrt_cif.sh — Merge a CIF-style INI into the live LabVIEW RT config with
# nirtcfg, start a second ./lvrt as lvuser, wait 0.2s for it to read lvrt.conf, then
# restore the config from a snapshot. Prints the new lvrt PID on stdout.
#
# Usage:
#   ./launch_lvrt_cif.sh <path-to-lvrt_cif.conf> <lvrt_argv_marker> [pidfile]
#
#   lvrt_argv_marker  Extra argv for ./lvrt (shown in ps). Avoid quotes/shell metacharacters.
#
# Environment (optional):
#   LVRT_CONF   Live INI (default: /etc/natinst/share/lvrt.conf)
#   NIRTCFG     default: /usr/local/natinst/bin/nirtcfg
#   LVRT_DIR    LabVIEW install dir (default: /usr/local/natinst/labview)
#   LVRT_CIF_SNAPSHOT  Canonical pre-overlay snapshot (default: /tmp/lvrt-cif-original.conf)
#
# When a second launch starts before the first has restored lvrt.conf, the shared snapshot
# ensures every launcher restores from the same original instead of a CIF-mutated LIVE copy.
#
# Caller must be root or lvuser. The second runtime always runs as lvuser: root uses
# runuser(1) (also checks /sbin and /usr/sbin when PATH is minimal) or, if missing,
# script(1)+su(1) so su has a pseudo-TTY. lvuser invokes /bin/sh -l on a generated
# runner (no su; works from LabVIEW RT System Exec without a terminal).
#
# Temp dir: root-owned mktemp dirs are 0700; chmod 701 on $WORKDIR so lvuser can
# traverse and execute the runner when using runuser.
#
# Requires: nirtcfg read/write to LIVE for the caller; setsid, nohup; lvrt binary.
# Fractional sleep 0.2 requires a shell sleep that accepts decimals.

set -e

# --- Paths and arguments ---
NIRTCFG="${NIRTCFG:-/usr/local/natinst/bin/nirtcfg}"   # NI tool to read/write INI keys
LIVE="${LVRT_CONF:-/etc/natinst/share/lvrt.conf}"       # Live LabVIEW RT config on disk
LVRT_DIR="${LVRT_DIR:-/usr/local/natinst/labview}"     # Directory containing ./lvrt binary
CIF="$1"                                                # Path to temporary CIF override INI
LVRT_EXTRA="$2"                                         # Extra argv for ./lvrt (visible in ps)
PIDFILE="${3:-/tmp/lvrt-cif-$$.pid}"                    # Runner writes new lvrt PID here
LOG="/tmp/lvrt-cif-$(basename "$PIDFILE" .pid).log"     # lvrt stdout/stderr from runner
# Shared copy of lvrt.conf before any CIF overlay; reused by overlapping launches.
STANDARD_SNAPSHOT="${LVRT_CIF_SNAPSHOT:-/tmp/lvrt-cif-original.conf}"

TAB=$(printf '\t')                                      # Field sep: section<TAB>token<TAB>value
WORKDIR=""                                              # Temp dir for snapshot, CIF, runner
RESTORE_DONE=0                                          # 1 after happy-path restore (skip in on_exit)
MUTATED=0                                               # 1 after LIVE modified (on_exit must restore)

usage() {
	echo "Usage: $0 <path-to-lvrt_cif.conf> <lvrt_argv_marker> [pidfile]" >&2
	exit 1
}

# Find the first usable command from a list of names/paths.
# LabVIEW RT often runs with a minimal PATH, so we also try absolute paths like /sbin/runuser.
find_first_cmd() {
	for _p in "$@"; do
		if command -v "$_p" >/dev/null 2>&1; then
			command -v "$_p"
			return 0
		fi
		if [ -x "$_p" ]; then
			printf '%s\n' "$_p"
			return 0
		fi
	done
	return 1
}

# Parse an INI file into normalized lines: section<TAB>token<TAB>value
parse_ini_assignments() {
	_file=$1
	section=""
	while IFS= read -r raw || [ -n "$raw" ]; do
		line=$(printf '%s' "$raw" | tr -d '\r')
		line=$(printf '%s' "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
		case "$line" in
		'' | \#* | \;*) continue ;;
		'['*']'*)
			section=$(printf '%s' "$line" | sed 's/^\[\([^]]*\)\].*/\1/' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
			continue
			;;
		esac
		case "$line" in
		*=*)
			[ -n "$section" ] || continue
			token=${line%%=*}
			value=${line#*=}
			token=$(printf '%s' "$token" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
			value=$(printf '%s' "$value" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
			value=$(printf '%s' "$value" | sed 's/^"\(.*\)"$/\1/')
			printf '%s\t%s\t%s\n' "$section" "$token" "$value"
			;;
		esac
	done <"$_file"
}

# Unique sorted list of section<TAB>token keys (no values); used for set-difference via comm.
keys_only_sorted() {
	parse_ini_assignments "$1" | cut -f1,2 | LC_ALL=C sort -u
}

# Populate $WORKDIR/snapshot.ini with the true original config.
# Why: a second launch (e.g. plugin loader) may start while the first is still running.
# By then LIVE may already hold the first launcher's CIF overlay — copying LIVE would
# save the wrong baseline. The shared file keeps the pre-overlay original for everyone.
acquire_workdir_snapshot() {
	if [ -f "$STANDARD_SNAPSHOT" ]; then
		# Overlapping launch — reuse the canonical original, not current LIVE.
		cp "$STANDARD_SNAPSHOT" "$WORKDIR/snapshot.ini"
		return 0
	fi
	# First launch in this burst — snapshot LIVE before we mutate it.
	cp "$LIVE" "$WORKDIR/snapshot.ini"
	if cp "$WORKDIR/snapshot.ini" "$STANDARD_SNAPSHOT" 2>/dev/null; then
		return 0
	fi
	# Rare race: another launcher published STANDARD_SNAPSHOT first; use theirs.
	if [ -f "$STANDARD_SNAPSHOT" ]; then
		cp "$STANDARD_SNAPSHOT" "$WORKDIR/snapshot.ini"
	fi
}

# Put LIVE back to the snapshot baseline via nirtcfg (not a raw file copy).
restore_snapshot() {
	_snap="$WORKDIR/snapshot.ini"
	_cifini="$WORKDIR/cif.ini"
	_ks="$WORKDIR/keys.snap"
	_kc="$WORKDIR/keys.cif"

	keys_only_sorted "$_snap" >"$_ks"
	keys_only_sorted "$_cifini" >"$_kc"

	# Re-apply every key/value from the original snapshot into LIVE.
	parse_ini_assignments "$_snap" | LC_ALL=C sort -t "$TAB" -k1,1 -k2,2 >"$WORKDIR/snap.rows"
	while IFS="$TAB" read -r sec tok val || [ -n "$sec" ]; do
		[ -z "$sec" ] && continue
		"$NIRTCFG" --file "$LIVE" --set section="$sec",token="$tok",value="$val"
	done <"$WORKDIR/snap.rows"

	# Keys added by CIF but absent from snapshot were temporary — remove them from LIVE.
	LC_ALL=C comm -13 "$_ks" "$_kc" >"$WORKDIR/to_clear_restore"
	while IFS="$TAB" read -r sec tok || [ -n "$sec" ]; do
		[ -z "$sec" ] && continue
		"$NIRTCFG" --file "$LIVE" --clear section="$sec",token="$tok" --rm-if-empty
	done <"$WORKDIR/to_clear_restore"
}

# If we modified LIVE but exit early, attempt restore so lvrt.conf is not left overlayed.
on_exit() {
	_ex=$?
	if [ "$RESTORE_DONE" -eq 1 ]; then
		[ -n "$WORKDIR" ] && rm -rf "$WORKDIR" 2>/dev/null || true
		exit "$_ex"
	fi
	if [ "$MUTATED" -eq 1 ] && [ -n "$WORKDIR" ] && [ -f "$WORKDIR/snapshot.ini" ]; then
		restore_snapshot || true
	fi
	[ -n "$WORKDIR" ] && rm -rf "$WORKDIR" 2>/dev/null || true
	exit "$_ex"
}

trap 'on_exit' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

# --- Validate arguments and required tools ---
[ -n "$CIF" ] && [ -f "$CIF" ] || usage
[ -n "$LVRT_EXTRA" ] || {
	echo "$0: lvrt_argv_marker (2nd argument) is required" >&2
	usage
}
[ -r "$LIVE" ] || {
	echo "$0: cannot read live config: $LIVE" >&2
	exit 1
}
[ -x "$NIRTCFG" ] || {
	echo "$0: nirtcfg not executable: $NIRTCFG" >&2
	exit 1
}
[ -x "$LVRT_DIR/lvrt" ] || {
	echo "$0: lvrt not found: $LVRT_DIR/lvrt" >&2
	exit 1
}
command -v setsid >/dev/null 2>&1 || {
	echo "$0: setsid not found" >&2
	exit 1
}
command -v nohup >/dev/null 2>&1 || {
	echo "$0: nohup not found" >&2
	exit 1
}

# --- Step 1: Save snapshot (shared) and CIF copy in a temp directory ---
WORKDIR=$(mktemp -d "${TMPDIR:-/tmp}/lvrt-cif-launch.XXXXXX")
acquire_workdir_snapshot
cp "$CIF" "$WORKDIR/cif.ini"

keys_only_sorted "$WORKDIR/snapshot.ini" >"$WORKDIR/keys.snap"
keys_only_sorted "$WORKDIR/cif.ini" >"$WORKDIR/keys.cif"

MUTATED=1

# --- Step 2: Apply this launcher's CIF overlay to LIVE via nirtcfg ---

# Remove keys present in snapshot but omitted from CIF (intentional clears in overlay).
LC_ALL=C comm -23 "$WORKDIR/keys.snap" "$WORKDIR/keys.cif" >"$WORKDIR/to_clear_apply"
while IFS="$TAB" read -r sec tok || [ -n "$sec" ]; do
	[ -z "$sec" ] && continue
	"$NIRTCFG" --file "$LIVE" --clear section="$sec",token="$tok" --rm-if-empty
done <"$WORKDIR/to_clear_apply"

# Set every key/value from the CIF file into LIVE (temporary — only for new lvrt startup).
parse_ini_assignments "$WORKDIR/cif.ini" >"$WORKDIR/cif.rows"
while IFS="$TAB" read -r sec tok val || [ -n "$sec" ]; do
	[ -z "$sec" ] && continue
	"$NIRTCFG" --file "$LIVE" --set section="$sec",token="$tok",value="$val"
done <"$WORKDIR/cif.rows"

# --- Step 3: Generate lvrt-run.sh for lvuser to start ./lvrt in the background ---
# Runner sets LabVIEW RT environment, starts lvrt, writes PID, sleeps 0.2s so lvrt
# can read LIVE before the main script restores the snapshot.
LVRT_EXTRA_SQ=$(printf '%s' "$LVRT_EXTRA" | sed "s/'/'\\\\''/g")
RUNNER_SH="$WORKDIR/lvrt-run.sh"
{
	printf '%s\n' '#!/bin/sh'
	printf "export LVRT_EXTRA='%s'\n" "$LVRT_EXTRA_SQ"
	printf '%s\n' \
		"trap '' HUP" \
		"cd '${LVRT_DIR}' || exit 1" \
		"ulimit -s 256" \
		'export LVRT_STATUS=${LVRT_STATUS:-NORMAL_START}'
	printf '%s\n' "export LD_LIBRARY_PATH='${LVRT_DIR}':/usr/local/natinst/lib\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}"
	printf '%s\n' 'nohup setsid ./lvrt "$LVRT_EXTRA" </dev/null >>'"${LOG}"' 2>&1 &'
	printf '%s\n' "echo \$! >'${PIDFILE}'"
	printf '%s\n' 'sleep 0.2'
} >"$RUNNER_SH"
# lvuser must traverse WORKDIR (x) and execute the runner when launched via runuser.
chmod 701 "$WORKDIR"
chmod 755 "$RUNNER_SH"

LVUSER_UID=$(id -u lvuser 2>/dev/null) || LVUSER_UID=
RUNUSER_BIN=$(find_first_cmd runuser /sbin/runuser /usr/sbin/runuser) || RUNUSER_BIN=
SCRIPT_BIN=$(find_first_cmd script /usr/bin/script) || SCRIPT_BIN=
SU_BIN=$(find_first_cmd su /bin/su) || SU_BIN=

# --- Step 4: Run the generated script as lvuser (lvrt must not run as root) ---
if [ "$(id -u)" -eq 0 ]; then
	: >"$PIDFILE"
	chown lvuser:ni "$PIDFILE" 2>/dev/null || chown lvuser "$PIDFILE"
	chmod 644 "$PIDFILE"
	chown lvuser:ni "$RUNNER_SH" 2>/dev/null || chown lvuser "$RUNNER_SH"
	if [ -n "$RUNUSER_BIN" ]; then
		"$RUNUSER_BIN" -u lvuser -- /bin/sh -l "$RUNNER_SH"
	elif [ -n "$SCRIPT_BIN" ] && [ -n "$SU_BIN" ]; then
		"$SCRIPT_BIN" -qec "$SU_BIN -- lvuser -l -c \"/bin/sh -l '$RUNNER_SH'\"" /dev/null
	else
		echo "$0: as root need runuser (util-linux), or script+su; or run this script as lvuser" >&2
		exit 1
	fi
elif [ -n "$LVUSER_UID" ] && [ "$(id -u)" -eq "$LVUSER_UID" ] || [ "$(id -un)" = lvuser ]; then
	rm -f "$PIDFILE"
	/bin/sh -l "$RUNNER_SH"
else
	echo "$0: run as root or lvuser (other users cannot launch lvrt here)" >&2
	exit 1
fi

# --- Step 5: Restore LIVE from snapshot; CIF overlay was only needed at lvrt startup ---
restore_snapshot
RESTORE_DONE=1
# Clear shared snapshot so the next unrelated launch snapshots fresh LIVE again.
rm -f "$STANDARD_SNAPSHOT"

# --- Step 6: Read PID and verify lvrt is still running ---
PID=$(tr -d ' \r\n' <"$PIDFILE")
[ -n "$PID" ] || {
	echo "$0: empty pid in $PIDFILE" >&2
	exit 1
}

[ -n "$WORKDIR" ] && rm -rf "$WORKDIR"
WORKDIR=""
MUTATED=0
trap - EXIT INT TERM

if ! kill -0 "$PID" 2>/dev/null; then
	echo "$0: lvrt pid $PID not running; see $LOG" >&2
	exit 1
fi

echo "$PID"
