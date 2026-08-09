Instructions to build installers for RT (ipk), Windows (NSIS), and Ubuntu (deb)

## cif_lvcore_ipk (LabVIEW RT)

1. Update the version in `Installers/cif_lvcore_ipk/control/control` when needed.
2. Update `Installers/cif_lvcore_ipk.build.json` when new source files must be copied from `src/` into the package.
3. From Windows, run:

   `Installers\build_cif_lvcore_ipk.bat`

   Or from WSL/Linux:

   `bash Installers/build_cif_lvcore_ipk.sh`

The build stages `Installers/cif_lvcore_ipk/`, copies files listed in `Installers/cif_lvcore_ipk.build.json`, normalizes text files to LF line endings, creates the IPK, and writes it to `Installers/output/`.

`postinst` enables `/etc/init.d/cifmanager` for boot with `update-rc.d cifmanager defaults 99 20` (starts after `nilvrt`, late in boot) and runs `cifmanager start` after install. See `src/Services/README.md`.

## cif_lvcore Windows (NSIS)

1. Update the version in `Installers/Windows/cif-lvcore.nsi` when needed.
2. Update `Installers/cif_lvcore_windows.build.json` when new source files must be copied from `src/` into the package.
3. Run:

   `Installers\Windows\build_nsis.bat`

The build stages `Installers/Windows/resource/`, copies files listed in `Installers/cif_lvcore_windows.build.json` (canonical protos and Python orchestration from `src/`), and creates `cif-lvcore.<version>.exe` in `Installers/Windows/`.

## cif_lvcore_deb (Ubuntu)

Update the version in `Installers/cif_lvcore_deb/DEBIAN/control`

From WSL/Linux:

`bash Installers/build_deb.sh`

The `.deb` is created in `Installers/`.
