Instructions to build installers for RT (ipk), Windows (NSIS), and Ubuntu (deb)

## cif_core_ipk (Linux RT)

1. Update the version in `Installers/cif_core_ipk/CONTROL/control` when needed.
2. Update `Installers/cif_core_ipk.build.json` when new source files must be copied from `src/` into the package.
3. Build host needs `binutils`, `tar`, `gzip`, and `python3` (e.g. `sudo apt install binutils tar gzip python3`). The build uses the bundled `Installers/opkg-utils/opkg-build` script; Ubuntu/WSL does not provide an `opkg-utils` apt package.
4. From Windows, run:

   `Installers\build_cif_core_ipk.bat`

   Or from WSL/Linux:

   `bash Installers/build_cif_core_ipk.sh`

The build stages `Installers/cif_core_ipk/`, copies files listed in `Installers/cif_core_ipk.build.json`, normalizes text files to LF line endings, packages with `opkg-build`, and writes `cif-core_<version>_<arch>.ipk` to `Installers/output/`.

`postinst` enables `/etc/init.d/cifmanager` for boot with `update-rc.d cifmanager defaults 99 20` (starts after `nilvrt`, late in boot) and runs `cifmanager start` after install. See `src/Services/README.md`.

## cif_core Windows (NSIS)

1. Update the version in `Installers/Windows/cif-core.nsi` when needed.
2. Update `Installers/cif_core_windows.build.json` when new source files must be copied from `src/` into the package.
3. Run:

   `Installers\Windows\build_nsis.bat`

The build stages `Installers/Windows/resource/`, copies files listed in `Installers/cif_core_windows.build.json` (canonical protos and Python orchestration from `src/`), and creates `cif-core.<version>.exe` in `Installers/Windows/`.

## cif_core_deb (Ubuntu)

Update the version in `Installers/cif_core_deb/DEBIAN/control`

From WSL/Linux:

`bash Installers/build_deb.sh`

The `.deb` is created in `Installers/`.
