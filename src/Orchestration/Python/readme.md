Instructions adapted from tutorial:
https://grpc.io/docs/languages/python/quickstart/

## Imports on RT and Windows

After the CIF IPK is installed on NI Linux RT, `postinst` registers
`/usr/local/cif/orchestrations/Python` with python3 via a site-packages
`.pth` file. Example scripts can then use `import cif_orchestration_base`
without modifying `sys.path`.

On Windows, example scripts fall back to the default install path under
`C:\Users\Public\Documents\CIF\orchestrations\Python` when the module is
not already on `PYTHONPATH`.

Regenerate the python files for grpc.  From this folder run:
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_common.proto
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_management_common.proto
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_manager.proto    
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_plugin_core.proto
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_channel_core.proto