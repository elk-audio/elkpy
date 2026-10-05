## 1.4.0

New features:
  * ZMQ-based IPC API as an alternative transport to gRPC, including `sushi_rpc_zmq`, `sushi_zmq_stub`, `sushi_zmq_async_stub`, and `zmq_notificationcontroller` (EUB-942).
  * Client-side blocklist filtering for notifications received over the ZMQ transport, since `zmq_notificationcontroller` does not enforce blocklists itself.
  * `AsyncSushiController` and asyncio-based counterparts for several controllers (`async_audiographcontroller`, `async_parametercontroller`), enabling `asyncio.gather()`-style usage.
  * `recompile_protofile.sh` and a `grpc_gen.py` helper script for regenerating the `_pb2` files from `sushi_rpc.proto`.

Fixes:
  * Resolved a protobuf version mismatch that could occur depending on the installed `protobuf`/`grpcio` versions.
  * Fixed imports for `sushi_rpc` and related generated modules.
  * Fixed examples (`sushi_control_example.py`, `sushi_monitor.py`) so they work without a separate proto file.

Breaking changes:
  * Bundled and lazily imported the protobuf-generated `sushi_rpc_pb2` / `sushi_rpc_pb2_grpc` modules directly in the package instead of requiring a `sushi_rpc.proto` file at runtime.
  * Moved development dependencies (`pytest`, `pytest-cov`, `pytest-asyncio`, `pyright`, `grpcio-tools`, `build`, `twine`) into `pyproject.toml` and removed `requirements.txt` / `tests_requirements.txt`.
  * Pinned `protobuf==4.25.*` and `grpcio~=1.62.1`, and restricted supported Python versions to `>=3.10, <3.13`.

## 1.3.0 and earlier

See git history prior to this file's introduction.
