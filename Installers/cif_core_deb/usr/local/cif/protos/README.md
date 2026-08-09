# CIF gRPC Interface Definitions

These `.proto` files define the public gRPC API for the CIF (Component Interface Framework) system. They describe services and messages used to manage plugins, channels, loaders, and related configuration—not the CIF Manager implementation itself.

## Licensing

| Scope | License |
|-------|---------|
| Files in this directory (`*.proto`) | [Apache License 2.0](LICENSE) |
| Code generated from these definitions (e.g. via `protoc`) | Apache-2.0 |
| CIF Manager implementation elsewhere in this repository | [GNU LGPL v2.1](../../LICENSE) |

Third-party projects may copy, modify, and distribute these interface definitions and use them to generate client or server stubs under Apache-2.0. Using the protos to implement a gRPC client or server does not, by itself, require adopting LGPL for your application.

Linking against or embedding CIF Manager binaries or libraries is governed separately by the LGPL. See the root [LICENSE](../../LICENSE) for those terms.

Each `.proto` file includes an Apache-2.0 header and `SPDX-License-Identifier: Apache-2.0`.

## Files

| File | Package | Description |
|------|---------|-------------|
| `cif_common.proto` | `cif.common` | Shared types (status, version, plugin names, etc.) |
| `cif_management_common.proto` | `cif.management_common` | Shared management and channel metadata messages |
| `cif_manager.proto` | `cif.manager` | CIF Manager service (load/register plugins, query system state) |
| `cif_plugin_core.proto` | `cif.plugincore` | Plugin lifecycle and configuration service |
| `cif_plugin_loader.proto` | `cif.pluginloader` | Plugin loader service |
| `cif_channel_core.proto` | `cif.channelcore` | Channel connection and FIFO management service |

Import dependencies: most services import `cif_common.proto` and/or `cif_management_common.proto`. Generate or compile dependent protos in dependency order.

## Generating code

Use `protoc` (or language-specific plugins) with this directory as the import path (`-I`).

### Python

From [`src/Orchestration/Python/`](../Orchestration/Python/), see [readme.md](../Orchestration/Python/readme.md) for full setup. Example:

```powershell
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_common.proto
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_management_common.proto
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_manager.proto
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_plugin_core.proto
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_plugin_loader.proto
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_channel_core.proto
```

### Other languages

Point your `protoc` invocation at this directory for imports. Generated stubs inherit the Apache-2.0 terms of these definitions; add the standard Apache header to generated files if your toolchain does not do so automatically.

## Canonical source

`src/protos/` is the authoritative location for these definitions. Copies shipped with installers should stay in sync with this directory.
