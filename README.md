# Sushi - gRPC controller wrapper #

A simple wrapper for controlling sushi over gRPC via a python script.

### Prerequisites ###

To use this wrapper, [python3.6](https://www.python.org/downloads/) or greater need to be installed, together with the `grpcio-tools` Python package. Both are installed by default in the development releases of Elk for the various supported architectures.

### Installation ###

The latest version of `elkpy` should be installed on your Elk device. If you want to use it from another
system you can either copy the module folder to the directory from where it should be used or install it locally
with `pip3 install -e elkpy` or similar.

### Usage ###

First import the sushicontroller package, e.g.:
```python
from elkpy import sushicontroller as sc
```
Then create an instance of the `SushiController` object:
```python
controller = sc.SushiController()
```
The default gRPC address is `localhost:51051` if you want to connect to another address. You can pass it as an argument to the constructor of the controller on the form `ip-address:port`.

The second argument to the constructor of SushiController is a path to the `sushi_rpc.proto` file with Protobuf protocol definition. If empty, the class will look at `usr/share/sushi/sushi_rpc.proto` which is the deafult installtion path for sushi.

To use the controller simply use the methods of the controller objects different sections. For example:
```python
# To make sure all the subcotrollers of sushicontroller close properly you can wrap them in a try except block
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

# To ensure proper closing of the controller close() should be called on the SushiController object when you're done with it
except KeyboardInterrupt:
    controller.close()
```

For a full documentation of the available methods. Use:
```console
$ pydoc3 elkpy.sushicontroller.SushiController
```
from where the elkpy folder is located.

### Running Unit Tests ###
Before running unit tests with the unittest command-line interface, you need to export the environment variable `SUSHI_GRPC_ELKPY_PROTO` pointing to the Sushi's `.proto` definition file.

Example:
```
$ export SUSHI_GRPC_ELKPY_PROTO=./sushi_rpc.proto
$ python3 -m unittest tests/sushi_controller_test.py
```
