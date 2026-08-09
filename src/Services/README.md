# CIF Manager services (NI Linux RT)

System V init scripts and supporting tools to start and stop the CIF Manager on NI Linux Real-Time.

## Layout

| Path | Installed location | Purpose |
|------|-------------------|---------|
| `init.d/cifmanager` | `/etc/init.d/cifmanager` | Boot-time service (installed and enabled by CIF ipk `postinst`) |
| `cif_manager_destroy` | `/usr/local/bin/cif_manager_destroy` | Python stop client (single file) |
| `DestroyCli/` | *(optional)* | C++ stop client — not recommended for deployment |

## Service behavior

**Start** runs the LabVIEW RT launcher:

```sh
/usr/local/cif/manager/loaders/launch_lvrt_cif.sh \
  /usr/local/cif/manager/loaders/lvrt_cif_manager.conf \
  Default_LabVIEW_Manager \
  /var/run/cifmanager.pid
```

The launcher starts a second `./lvrt` process for the CIF Manager and records its PID in `/var/run/cifmanager.pid`.

**Stop** calls `cif_manager_destroy`, which:

1. Parses `/usr/local/cif/etc/cif.conf` for `Manager_Port` and `Server_Certificate_File`
2. Connects to `localhost:<port>` (TLS when a server certificate path is configured)
3. Invokes the `Destroy` RPC from `cif_manager.proto`

If the lvrt process is still running after the RPC, the init script waits up to 30 seconds, then sends `SIGTERM`.

---

## Deploy `cif_manager_destroy` (recommended)

The stop client is a **single Python script** — no compile step, no `libgrpc++.so` to ship separately, and **no generated protobuf stubs**. It calls `/cif.manager.Manager/Destroy` directly via `grpcio`.

### What you install

| Item | Required? | Notes |
|------|-----------|--------|
| `cif_manager_destroy` | Yes | One file → `/usr/local/bin/cif_manager_destroy` |
| CIF ipk | Yes | Manager, launch scripts, `cif.conf` |
| `python3` | Yes | Declared in CIF ipk `Depends`; used by `launch_rt.py` on RT |
| `python3-pip` | Yes | Declared in CIF ipk `Depends`; used as fallback when grpcio is not in opkg |
| `grpcio` | Yes | Installed by CIF ipk `postinst` via opkg (`python3-grpcio`) or `pip install grpcio` |
| CIF orchestration Python stubs | **No** | Script encodes the RPC without `cif_manager_pb2` |
| Separate gRPC C++ install | **No** | Avoided by using Python grpcio |

### Install the script

Copy with **LF line endings** (Windows CRLF breaks the `#!/usr/bin/env python3` shebang on Linux):

```sh
scp src/Services/cif_manager_destroy admin@<rt-ip>:/tmp/
ssh admin@<rt-ip> 'sed -i "s/\r$//" /tmp/cif_manager_destroy && install -m 755 /tmp/cif_manager_destroy /usr/local/bin/cif_manager_destroy'
```

If you already copied a broken file, fix it on the target:

```sh
sed -i 's/\r$//' /usr/local/bin/cif_manager_destroy
# or: dos2unix /usr/local/bin/cif_manager_destroy
```

Or include it in your CIF ipk under `usr/local/bin/` (see `Installers/cif_core_ipk`).

The full CIF ipk also installs `src/Services/init.d/cifmanager` to `/etc/init.d/cifmanager`,
runs `update-rc.d cifmanager defaults 99 20` during `postinst`, and starts the service with
`/etc/init.d/cifmanager start` so the manager is running without a reboot.

## Boot order (System V init / rc.d)

NI Linux RT uses **System V init**: `update-rc.d` creates `SNN`/`KNN` symlinks under
`/etc/rc2.d` … `/etc/rc5.d` from the LSB headers in `/etc/init.d/*`.

`cifmanager` is configured to:

| Mechanism | Setting | Effect |
|-----------|---------|--------|
| `Required-Start` | `nilvrt` | Start **after** the primary LabVIEW RT service (`/etc/init.d/nilvrt`) |
| `update-rc.d … 99 20` | Start seq. 99 | Start **late** in the boot sequence |
| `update-rc.d … 99 20` | Stop seq. 20 | Stop **early** on shutdown (before many other services) |

Verify on the target after install:

```sh
grep -E '^# Required-Start' /etc/init.d/cifmanager
ls -la /etc/rc5.d/S*cifmanager /etc/rc5.d/S*nilvrt
# S number for cifmanager should be greater than S number for nilvrt
```

Re-apply boot links after editing the init script:

```sh
update-rc.d -f cifmanager remove
update-rc.d cifmanager defaults 99 20
```

### Python gRPC on the target

The CIF ipk `postinst` script installs `grpcio` automatically. It tries opkg
package names such as `python3-grpcio` first, then falls back to:

```sh
python3 -m pip install grpcio protobuf
```

If you install `cif_manager_destroy` without the full CIF ipk, install manually:

```sh
opkg update && opkg install python3-grpcio
# or:
python3 -m pip install grpcio
```

Verify:

```sh
python3 -c "import grpc"
sed -i 's/\r$//' /usr/local/bin/cif_manager_destroy   # if copied from Windows
/usr/local/bin/cif_manager_destroy --help
```

### Install the init.d service manually

Only needed if you deploy `cif_manager_destroy` or loader assets without the full CIF ipk:

```sh
scp src/Services/init.d/cifmanager admin@<rt-ip>:/tmp/cifmanager
ssh admin@<rt-ip> 'install -m 755 /tmp/cifmanager /etc/init.d/cifmanager && update-rc.d cifmanager defaults 99 20'
```

Ensure CIF launcher assets are installed (CIF ipk / RT Loader):

- `/usr/local/cif/manager/loaders/launch_lvrt_cif.sh`
- `/usr/local/cif/manager/loaders/lvrt_cif_manager.conf`
- `/usr/local/cif/etc/cif.conf`

### Test

With the CIF Manager running:

```sh
/usr/local/bin/cif_manager_destroy
/etc/init.d/cifmanager stop
```

Expected output: `Destroy accepted (manager_pid=...)`.

### Why not the C++ `DestroyCli`?

The C++ binary links against native `libgrpc++.so` libraries that are **not** part of the CIF or LabVIEW install. Prefer the Python `cif_manager_destroy` script unless you have a specific reason to use C++.

See [Appendix: C++ DestroyCli](#appendix-c-destroycli) if you still want a native binary.

---

## Appendix: C++ DestroyCli

<details>
<summary>Optional native C++ client (click to expand)</summary>

The `DestroyCli/` CMake project builds a C++ binary that also calls `Destroy`. It requires building **gRPC C++** on the RT target and shipping native `.so` libraries at runtime. Prefer the Python `cif_manager_destroy` script unless you have a specific reason to use C++.

Build on the controller (not WSL). Install upstream [grpc/grpc](https://github.com/grpc/grpc) to `/usr/local/grpc`, then:

```sh
cd Services/DestroyCli
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=/usr/local/grpc
cmake --build build
install -m 755 build/cif_manager_destroy /usr/local/bin/cif_manager_destroy
echo /usr/local/grpc/lib > /etc/ld.so.conf.d/grpc.conf && ldconfig
```

See git history or `DestroyCli/README.md` for full C++ build notes.

</details>

---

```sh
/etc/init.d/cifmanager start
/etc/init.d/cifmanager stop
/etc/init.d/cifmanager restart
/etc/init.d/cifmanager status
```

Manual graceful shutdown (without the init script):

```sh
/usr/local/bin/cif_manager_destroy
```
