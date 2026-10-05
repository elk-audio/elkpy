#!/usr/bin/env bash

uv run python -m grpc_tools.protoc -I src/elkpy/rpc --python_out=src/elkpy/rpc --grpc_python_out=src/elkpy/rpc src/elkpy/rpc/sushi_rpc.proto

sed -i 's/import sushi_rpc_pb2 as sushi__rpc__pb2/from . import sushi_rpc_pb2 as sushi__rpc__pb2/' src/elkpy/rpc/sushi_rpc_pb2_grpc.py
