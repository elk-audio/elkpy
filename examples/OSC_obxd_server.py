from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

def print_handler(address, *args):
    print(f"{address}: {args}")

def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

dispatcher = Dispatcher()
dispatcher.map("/parameter/obxd/*", print_handler)
dispatcher.set_default_handler(default_handler)

ip = "192.168.1.140"
port = 1337

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()