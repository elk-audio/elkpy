# Sushi - gRPC controller wrapper

A simple wrapper for controlling sushi over gRPC via a python script.

## Prerequisites

To use this wrapper, [python3.7](https://www.python.org/downloads/) or greater needs to be installed, together with the `grpcio-tools` Python package. Both are installed by default in the development releases of Elk for the various supported architectures.

## Installation

If you are running your Python program on a device running Elk Audio OS, the latest `elkpy` should already be installed.

But, if you use elkpy on another system, e.g. macOS, you can either copy the module folder to the directory where it will be used, or install it locally with `pip3 install -e elkpy` or similar.
`elkpy` is also available on Pypi: `pip install elkpy`.

## Usage

First import the sushicontroller package, e.g.:

```python
from elkpy import sushicontroller as sc
```

Then create an instance of the `SushiController` object:

```python
controller = sc.SushiController()
```

The default gRPC address is `localhost:51051`.
To connect to another address, pass it as an argument to the constructor of the controller with the format `ip-address:port`.

The second argument to the constructor of SushiController is a path to the `sushi_rpc.proto` file, which contains Sushi's Protobuf protocol definition.
If the argument is empty, the class will look for it at `usr/share/sushi/sushi_rpc.proto`, the default installation path for Sushi.

To use the controller simply use the methods of the controller objects different sections. For example:

```python
# To make sure all the sub-controllers of SushiController close properly, you can wrap them in a try except block:
try:
    # Get a list of the tracks available in sushi
    list_of_tracks = controller.audio_graph.get_tracks()

    # Get the parameters of the track with the id passed to the method
    track_id = 0
    list_of_processors = controller.parameters.get_track_parameters(track_id)

    # Send a note on message to a track in sushi
    track_id = 0
    channel = 0
    note = 65
    velocity = 0.8
    controller.keyboard.send_note_on(track_id, channel, note, velocity)

# To ensure proper closing of SushiController, close() should be called on your instance when you're done using it
except KeyboardInterrupt:
    controller.close()
```

For full documentation on all available methods, use:

```console
$ pydoc3 elkpy.sushicontroller.SushiController
```

On the terminal where the elkpy folder is located.

## Important notes on return values

In Sushi, get requests are processed synchronously, while set requests are scheduled asynchronously. The former will return the requested data, but
the latter can only return a confirmation that the command has been registered.

This can lead to situations where a user could for instance try to set a parameter on a processor that has not yet been created by Sushi, even though 
the call to `create_processor_on_track` had been made.

### Elkpy asyncio events 

To alleviate this burden for _simple_ use-cases, `elkpy` adopts the following behavior:

Commands that edit the audio graph:

- create_track
- delete_track
- create_processor_on_track
- create_processor_on_track
- ...

return an `SushiCommandResponse`: an asyncio.Event that will be **set** by `elkpy` whenever the corresponding notification is emitted by Sushi.

An asyncio user can elect to `await SushiCommandResponse.wait()` to ensure that the command has been properly carried out before carrying on
with further rpcs.
Ignoring the event is also a valid option for cases where absolute confirmation is not critical.

If an error has occurred in grpc, `wait()` will raise a `SushiUnknownError`.


#### CAUTION
elkpy uses an asyncio.EventLoop to run its notification monitoring. In asyncio programs, it will simply get the current running loop. And if that fails (for instance
if you are writing a synchronous program), it will starts a new loop in a separate thread.

You MUST therefore be careful when you instantiate the main SushiController class when writing asyncio applications. Make sure that a loop **is already running**, for instance by instantiating a SushiController inside your `async def main()`.

If you fail to do that, you will end up with 2 running loops: one in the main thread and one in an elkpy thread. And that will break the SushiCommandResponse system, because asyncio.Events are **not thread-safe**!

#### Synchronous programs and SushiCommandResponse
Synchronous programs may also leverage SushiCommandResponse but in a different way. The object *waiting* on such events can **not** wait() on them but MUST check their `event.is_set()` method instead. This 
will return `True` once *elkpy* has set the event.

For more information about `asyncio.Event`: [https://docs.python.org/3/library/asyncio-sync.html]

---

## Examples

The `examples` subdirectory contains examples of how elkpy can be used.

### Sushi Control Example

This demonstrates instantiating 3 processors onto Sushi started with an “empty” config, subscribing to notifications to wait for their instantiation, and then setting their parameters once they're available.

To run:

1. Ensure you have a Python environment set up where the packages described in requirements.txt are available, globally or in a `venv`.
2. Start Sushi with the provided "sushi_control_example_config.json", and the '--base-plugin-path' set to point to where `mda-vst.vst3` plugins are available:

```commandline
$ ./sushi --portaudio \
          --config-file /path/to/elkpy/examples/sushi_control_example_config.json \
          --base-plugin-path=/path/to/sushi/build/debug/VST3/Debug/
```

If you've built Sushi from source, the plugins are built and accessible in the above path relative to the sushi binary.

3. Start `sushi_control_example.py`:

```commandline
$ python3 ./sushi_control_example.py --protofile "/path/to/sushi/rpc_interface/protos/sushi_rpc.proto"
```

The `--protofile` argument points elkpy to the protocol buffer file used by Sushi.

You should hear Sushi play a familiar theme tune.

### Sushi Monitor

An example passive monitor app using elkpy.
It connects to a sushi instance, subscribes to notifications and displays all the parameter, transport and audio graph changes that Sushi broadcasts.

##### Usage

Ensure there is a Sushi instance running on the same computer.

Then run:

```
$ export SUSHI_GRPC_ELKPY_PROTO=./sushi_rpc.proto
$ python3 examples/sushi_monitor.py
```

## Running Unit Tests

Before running unit tests with the unittest command-line interface, you need to export the environment variable `SUSHI_GRPC_ELKPY_PROTO`, pointing to the Sushi's `.proto` definition file.

Example:

```
$ export SUSHI_GRPC_ELKPY_PROTO=./sushi_rpc.proto
$ python3 -m unittest discover -s tests -p '*_test.py'
```
