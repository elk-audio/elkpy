__author__ = "Ruben Svensson"
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
import sushi_rpc_pb2 as proto
import sushi_rpc_pb2_grpc
from src.elkpy import sushi_info_types as info

expected_build_info = info.SushiBuildInfo()
expected_build_info.version = "0.11.0"
expected_build_info.build_options = ["WITH_VST", "WITH_XENOMAI"]
expected_build_info.audio_buffer_size = 64
expected_build_info.commit_hash = "er7415hf"
expected_build_info.build_date = "15-11-2021 11:47"

grpc_build_info = proto.SushiBuildInfo(version=expected_build_info.version,
                                       build_options=expected_build_info.build_options,
                                       audio_buffer_size=expected_build_info.audio_buffer_size,
                                       commit_hash=expected_build_info.commit_hash,
                                       build_date=expected_build_info.build_date)

expected_input_channel_count = 3
expected_output_channel_count = 24

class SystemControllerServiceMockup(sushi_rpc_pb2_grpc.SystemControllerServicer):

    def __init__(self) -> None:
        super().__init__()

    def GetSushiVersion(self, request, context):
        return proto.GenericStringValue(value=expected_build_info.version)

    def GetBuildInfo(self, request, context):
        return grpc_build_info

    def GetInputAudioChannelCount(self, request, context):
        return proto.GenericIntValue(value=expected_input_channel_count)

    def GetOutputAudioChannelCount(self, request, context):
        return proto.GenericIntValue(value=expected_output_channel_count)
