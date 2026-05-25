# CIF_Manager

Core code for managing a CIF target, loading plugins, and UI for interacting with the system for configuration.

## Licensing

This repository uses a dual-license model:

| Scope | License |
|-------|---------|
| CIF Manager implementation (LabVIEW, UI, loaders, orchestration, and other code under `src/` except `src/protos/`) | [GNU LGPL v2.1](LICENSE) |
| gRPC interface definitions (`src/protos/*.proto`) | [Apache License 2.0](src/protos/LICENSE) |

Third-party projects may use the `.proto` files and code generated from them (for example via `protoc`) under Apache-2.0. Using the protos to implement a gRPC client or server does not, by itself, require adopting LGPL for your application.

Linking against or embedding CIF Manager binaries or libraries is governed separately by the LGPL. See [LICENSE](LICENSE) for those terms.

For API file descriptions, code generation, and proto-specific licensing details, see [src/protos/README.md](src/protos/README.md).
