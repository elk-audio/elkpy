#!/usr/bin/env bash

uv run python -m grpc_tools.protoc -I src/elkpy/rpc --python_out=src/elkpy/rpc --grpc_python_out=src/elkpy/rpc src/elkpy/rpc/sushi_rpc.proto
