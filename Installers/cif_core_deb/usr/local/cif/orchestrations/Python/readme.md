Instructions adapted from tutorial:
https://grpc.io/docs/languages/python/quickstart/

Regenerate the python files for grpc.  From this folder run:
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_manager.proto    
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_plugin_core.proto
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_channel_core.proto
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/cif_common.proto