__author__ = "Maxime Gendebien"
__copyright__ = """

    Copyright 2017-2026 Elk Audio AB

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
from . import sushi_info_types as info_types
from .rpc import sushi_rpc_pb2

###############################
#   System Controller class   #
###############################


class SystemController(object):
    """Class to manage system-level settings in Sushi"""

    def __init__(self, stub) -> None:
        self._stub = stub

    def get_sushi_version(self) -> str:
        try:
            response = self._stub.GetSushiVersion(sushi_rpc_pb2.GenericVoidValue())
            return response.value
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_sushi_api_version(self) -> str:
        try:
            response = self._stub.GetSushiApiVersion(sushi_rpc_pb2.GenericVoidValue())
            return response.value
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_build_info(self) -> info_types.SushiBuildInfo:
        try:
            response = self._stub.GetBuildInfo(sushi_rpc_pb2.GenericVoidValue())
            return info_types.SushiBuildInfo(response)
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_input_audio_channel_count(self) -> int:
        try:
            response = self._stub.GetInputAudioChannelCount(
                sushi_rpc_pb2.GenericVoidValue()
            )
            return response.value
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_output_audio_channel_count(self) -> int:
        try:
            response = self._stub.GetOutputAudioChannelCount(
                sushi_rpc_pb2.GenericVoidValue()
            )
            return response.value
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)
