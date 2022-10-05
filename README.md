# Sushi - gRPC controller wrapper #

A simple wrapper for controlling sushi over gRPC via a python script.

### Prerequisites ###

To use this wrapper, [python3.6](https://www.python.org/downloads/) or greater needs to be installed, 
together with the `grpcio-tools` Python package. Both are installed by default in the development 
releases of Elk for the various supported architectures.

### Installation ###

If you are running your python program on a device running Elk Audio OS, the latest `elkpy` should already be installed.

But, if you use elkpy on another system, e.g. macOS, you can either copy the module folder to the directory where it will be used,
or install it locally with `pip3 install -e elkpy` or similar.

### Usage ###

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

The second argument to the constructor of SushiController is a path to the `sushi_rpc.proto` file, 
which contains Sushi's Protobuf protocol definition.
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

### Examples ###

The `examples` subdirectory contains examples of how elkpy can be used.

#### Sushi Monitor ####

An example passive monitor app using elkpy.
It connects to a sushi instance, subscribes to notifications and displays all the
parameter, transport and audio graph changes that Sushi broadcasts.

##### Usage ##### 

Ensure there is a Sushi instance running on the same computer.

Then run:
```
$ export SUSHI_GRPC_ELKPY_PROTO=./sushi_rpc.proto
$ python3 examples/sushi_monitor.py
```

### Running Unit Tests ###
Before running unit tests with the unittest command-line interface, 
you need to export the environment variable `SUSHI_GRPC_ELKPY_PROTO`, pointing to the Sushi's `.proto` definition file.

Example:
```
$ export SUSHI_GRPC_ELKPY_PROTO=./sushi_rpc.proto
$ python3 -m unittest discover -s tests -p '*_test.py'
```
