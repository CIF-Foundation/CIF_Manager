# LabVIEW RT CIF launcher

`launch_lvrt_cif.sh` merges a temporary CIF-style INI into the live LabVIEW RT config (`lvrt.conf`), starts a second `./lvrt` process as `lvuser`, waits briefly for that process to read the config, then restores `lvrt.conf` from a snapshot. The new lvrt PID is printed on stdout.

## Usage

```sh
./launch_lvrt_cif.sh <path-to-lvrt_cif.conf> <lvrt_argv_marker> [pidfile]
```

| Argument | Purpose |
|----------|---------|
| `lvrt_cif.conf` | CIF overlay INI (e.g. `lvrt_cif_manager.conf`, `lvrt_cif_pluginloader.conf`) |
| `lvrt_argv_marker` | Extra argv for `./lvrt` (visible in `ps`). Avoid quotes and shell metacharacters. |
| `pidfile` | Optional. Default: `/tmp/lvrt-cif-<pid>.pid` |

Example markers used in this project:

- Manager: `Default_LabVIEW_Manager`
- Plugin loader: `Default_LabVIEW`

## Launch chain

Typical startup on RT:

1. **`launch_rt.py`** — starts the manager via `launch_lvrt_cif.sh` and `lvrt_cif_manager.conf`.
2. **Manager LabVIEW VI** — System Exec starts the plugin loader via the same script and `lvrt_cif_pluginloader.conf`.

Both launches mutate `lvrt.conf` briefly and restore it when finished. Overlapping runs can race on the live config.

## Shared snapshot (`/tmp/lvrt-cif-original.conf`)

When a second launch starts before the first has restored `lvrt.conf`, copying LIVE at snapshot time could capture the first launcher's CIF overlay instead of the true original.

The script uses a shared canonical snapshot:

- **First launch in a burst** — copies LIVE to `/tmp/lvrt-cif-original.conf` before applying its overlay.
- **Overlapping launch** — reuses that shared file as its restore baseline (not current LIVE).
- **After successful restore** — removes the shared snapshot so the next unrelated launch snapshots fresh LIVE again.

Environment override: `LVRT_CIF_SNAPSHOT` (default `/tmp/lvrt-cif-original.conf`).

## LabVIEW System Exec: sequencing manager and plugin loader

The plugin loader should not start while the manager launch still holds the shared snapshot (manager has not finished restoring). A simple guard before the plugin-loader launch:

```sh
/bin/sh -c 'while [ -f /tmp/lvrt-cif-original.conf ]; do sleep 0.1; done; exec /usr/local/cif/manager/loaders/launch_lvrt_cif.sh /usr/local/cif/manager/loaders/lvrt_cif_pluginloader.conf Default_LabVIEW'
```

While the wait loop runs, the manager launch is still in progress (overlay applied, restore not yet complete). After the manager removes `/tmp/lvrt-cif-original.conf`, the plugin loader can proceed.

**Note:** A remaining race is possible if the second launch mutates LIVE while the first is still restoring. The shared snapshot fixes the wrong-baseline problem; full serialization would require additional coordination (not implemented in the script).

## Zombie processes with "don't wait for completion"

If LabVIEW System Exec is configured with **don't wait for completion**, the VI does not call `wait()` on the shell it spawned. When that shell exits (after the wait loop and full launch complete), it becomes a **zombie** (`<defunct>`) until the parent reaps it. LabVIEW never reaps it, so the process entry persists.

This affects any long-running `sh -c '...'` command started with don't-wait — not a bug in the wait loop itself.

### Planned fix: async wrapper (not implemented)

**Status: to-do.** Do not use in production until the wrapper script is added and deployed.

The intended approach is a small wrapper that forks the real work into a new session and exits immediately. LabVIEW **waits on the wrapper** (returns in milliseconds), which reaps the wrapper and avoids zombies. The actual launch continues in the background under `init`.

Proposed wrapper (`launch_lvrt_cif_async.sh`):

```sh
#!/bin/sh
# Fast exit for LabVIEW System Exec (use WITH wait on completion).
# Worker is reparented to init; LV only waits milliseconds.

if [ "$1" = "--worker" ]; then
	shift
	while [ -f /tmp/lvrt-cif-original.conf ]; do sleep 0.1; done
	exec /usr/local/cif/manager/loaders/launch_lvrt_cif.sh "$@"
fi

setsid /bin/sh "$0" --worker "$@" </dev/null >>/tmp/lvrt-cif-async.log 2>&1 &
exit 0
```

LabVIEW System Exec command (once the wrapper exists):

```sh
/usr/local/cif/manager/loaders/launch_lvrt_cif_async.sh /usr/local/cif/manager/loaders/lvrt_cif_pluginloader.conf Default_LabVIEW
```

| LabVIEW setting | Value |
|-----------------|-------|
| Wait for completion | **Yes** — required so LV reaps the wrapper (wrapper exits almost immediately) |
| Effective behavior | Plugin loader still starts asynchronously; LV is not blocked for the full launch |

Log output from the background worker: `/tmp/lvrt-cif-async.log`.

### Alternatives if "wait" cannot be enabled

- **`systemd-run`** or **`start-stop-daemon`** (if available on the RT image) to detach the worker from LabVIEW's process tree.
- A **long-lived RT daemon** that accepts launch requests (e.g. via a request file) and manages its own child processes.

Without one of these patterns, don't-wait System Exec will leave zombie shells when they exit.

## Related files

| File | Role |
|------|------|
| `launch_lvrt_cif.sh` | Main launcher script |
| `lvrt_cif_manager.conf` | CIF overlay for the manager lvrt |
| `lvrt_cif_pluginloader.conf` | CIF overlay for the plugin-loader lvrt |
| `launch_lvrt_cif_async.sh` | **Planned** — async wrapper for LabVIEW (not yet implemented) |

Deployed copies on RT typically live under `/usr/local/cif/manager/loaders/`.
