from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
from typing import List, Any
from ELKpy import sushicontroller as sc 
import asyncio

# define the ip-address and the port for the server connection
ip_server = "192.168.1.140"
port_server = 1337

# define the ip-address and the port for the client connection
ip_client = "192.168.1.83"
port_client = 8080

# define the ip-address and the port for controlling sushi via grpc
sushi_controller_addres = 'localhost:51051'
controller = sc.SushiController(sushi_controller_addres) # Create controller object

# initialize dictionary for parameter name - id key value pair
parameter_ids = {}

# initialize dictionary for processor name - id key value pair
processor_ids = {}

# initializ dictionary for track name - id key value pair
track_ids = {}

# variable that holds the name of the processor to control
processor_name = "obxd"

processor_prefix = "/parameter/"

parameter_prefix = processor_prefix + processor_name + "/"

for track in controller.get_tracks():
    track_ids[track.name] = track.id
    for processor in controller.get_track_processors(track.id):
        processor_ids[processor.name] = processor.id
        if processor.name == processor_name:
            for parameter in controller.get_processor_parameters(processor.id):
                parameter_ids[parameter.name] = parameter.id



# handle to process the incoming OSC message and hand them over to grpc
def OSC_to_grpc(address: str, arg):
    print(f"{address}: {arg}")
    controller.set_parameter_value(processor_ids[processor_name], 
                                    parameter_ids[address[len(parameter_prefix):]], 
                                    arg)

# creates an OSC dispatcher
dispatcher = Dispatcher()

# map the OSC_to_grpc handler to the corresponding OSC message
dispatcher.map(parameter_prefix + "*", OSC_to_grpc)

async def client_loop():
    client = SimpleUDPClient(ip_client, port_client)

    while(1):
        for parameter in controller.get_processor_parameters(processor_ids[processor_name]):
            value = controller.get_parameter_value(processor_ids[processor_name], parameter.id)
            client.send_message(parameter_prefix + parameter.name, value)
        await asyncio.sleep(1)


async def init_main():
    server = AsyncIOOSCUDPServer((ip_server, port_server), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    
    task = asyncio.ensure_future(client_loop())
    await asyncio.gather(task)

    transport.close()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.ensure_future(init_main()))
    loop.close()