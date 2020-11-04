__author__ = "Maxime Gendebien"
__copyright__ = """

    Copyright 2017-2019 Modern Ancient Instruments Networked AB, dba Elk

    elkpy is free software: you can redistribute it and/or modify it under the terms of the
    GNU General Public License as published by the Free Software Foundation, either version 3
    of the License, or (at your option) any later version.

    elkpy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
    even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with elkpy.  If
    not, see <http://www.gnu.org/licenses/>.
"""
__license__ = "GPL-3.0"

import grpc

from . import sushierrors
from . import grpc_gen
from typing import List

############################################
#   Sushi Audio Routing Controller class   #
############################################

class AudioRoutingController(object):
    """
    A class to control audio routing in Sushi via gRPC.

    Attributes:
        _stub (AudioRoutingControllerStub): connection stub to the gRPC audio routing interface in sushi
    """
    def __init__(self,
                 address: str='localhost:51051',
                 sushi_proto_def: str='/usr/share/sushi/sushi_rpc.proto') -> None:
        """
        Args:
            address: IP address to Sushi in the uri form : 'ip-addr:port'
            sushi_proto_def: path to the .proto file with SUSHI gRPC services definitions
        """
        try:
            channel = grpc.insecure_channel(address)
        except AttributeError as e:
            raise TypeError(f"Parameter address = {address}. Should be a string containing the ip-address and port "
                            f"to Sushi") from e

        self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self._stub = self._sushi_grpc.AudioRoutingControllerStub(channel)

    def get_all_input_connections(self) -> List:
        pass