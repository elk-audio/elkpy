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

from .sushi_zmq_stub import SushiZmqStub


class AsyncSushiZmqStub:
    """Async wrapper around SushiZmqStub.

    Exposes only the methods used by AsyncParameterController and
    AsyncAudioGraphController as coroutines, so those controllers can
    'await self._stub.X(...)' identically to how they use grpc.aio stubs.
    """

    def __init__(self, zmq_stub: SushiZmqStub):
        self._stub = zmq_stub

    # --- ParameterController methods ---
    async def GetTrackParameters(self, request): return self._stub.GetTrackParameters(request)
    async def GetProcessorParameters(self, request): return self._stub.GetProcessorParameters(request)
    async def GetParameterId(self, request): return self._stub.GetParameterId(request)
    async def GetParameterInfo(self, request): return self._stub.GetParameterInfo(request)
    async def GetParameterValue(self, request): return self._stub.GetParameterValue(request)
    async def GetParameterValueInDomain(self, request): return self._stub.GetParameterValueInDomain(request)
    async def GetParameterValueAsString(self, request): return self._stub.GetParameterValueAsString(request)
    async def SetParameterValue(self, request): return self._stub.SetParameterValue(request)
    async def GetTrackProperties(self, request): return self._stub.GetTrackProperties(request)
    async def GetProcessorProperties(self, request): return self._stub.GetProcessorProperties(request)
    async def GetPropertyId(self, request): return self._stub.GetPropertyId(request)
    async def GetPropertyInfo(self, request): return self._stub.GetPropertyInfo(request)
    async def GetPropertyValue(self, request): return self._stub.GetPropertyValue(request)
    async def SetPropertyValue(self, request): return self._stub.SetPropertyValue(request)

    # --- AudioGraphController methods ---
    async def GetAllProcessors(self, request): return self._stub.GetAllProcessors(request)
    async def GetAllTracks(self, request): return self._stub.GetAllTracks(request)
    async def GetTrackId(self, request): return self._stub.GetTrackId(request)
    async def GetTrackInfo(self, request): return self._stub.GetTrackInfo(request)
    async def GetTrackProcessors(self, request): return self._stub.GetTrackProcessors(request)
    async def GetProcessorId(self, request): return self._stub.GetProcessorId(request)
    async def GetProcessorInfo(self, request): return self._stub.GetProcessorInfo(request)
    async def GetProcessorBypassState(self, request): return self._stub.GetProcessorBypassState(request)
    async def GetProcessorState(self, request): return self._stub.GetProcessorState(request)
    async def SetProcessorBypassState(self, request): return self._stub.SetProcessorBypassState(request)
    async def SetProcessorState(self, request): return self._stub.SetProcessorState(request)
    async def SetDiscreteProcessorState(self, request): return self._stub.SetDiscreteProcessorState(request)
    async def CreateTrack(self, request): return self._stub.CreateTrack(request)
    async def CreateMultibusTrack(self, request): return self._stub.CreateMultibusTrack(request)
    async def CreatePreTrack(self, request): return self._stub.CreatePreTrack(request)
    async def CreatePostTrack(self, request): return self._stub.CreatePostTrack(request)
    async def CreateProcessorOnTrack(self, request): return self._stub.CreateProcessorOnTrack(request)
    async def MoveProcessorOnTrack(self, request): return self._stub.MoveProcessorOnTrack(request)
    async def DeleteProcessorFromTrack(self, request): return self._stub.DeleteProcessorFromTrack(request)
    async def DeleteTrack(self, request): return self._stub.DeleteTrack(request)
