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
import asyncio
import _thread
from . import sushierrors
from . import sushi_info_types as info_types
from . import grpc_gen
from typing import List

###########################################
#   Sushi Notification Controller class   #
###########################################


class NotificationController(object):
    """
    Class to manage subscriptions to Sushi notifications (changes, updates, ...)

    Attributes:
        _stub (NotificationControllerStub): Connection stub to the gRPC Notification controller interface in Sushi
    """
    def __init__(self,
                 address='localhost:51051',
                 sushi_proto_def='/usr/share/sushi/sushi_rpc.proto'):
        """
        Constructor for the Notification Controller
        Args:
            address (str): 'ip-address:port' The ip-address and port at which to connect to sushi.
            sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition.
        """
        self._start_notification_client()
        try:
            channel = grpc.aio.insecure_channel(address)
        except AttributeError as e:
            raise TypeError(f"Parameter address = {address}. "
                            f"Should be a string containing the IP address and port to Sushi")

        self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self._stub = self._sushi_grpc.NotificationControllerStub(channel)

    def _start_notification_client(self):
        _thread.start_new_thread(self._start_loop, ())

    def _start_loop(self):
        # Create new event loop and assigning it to this thread
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        # Starting the loop
        self.loop.run_forever()

    ####################################################
    # API : Subscription to Sushi notification streams #
    ####################################################

    def subscribe_to_transport_changes(self) -> None:
        """
        Subscribes to Transport changes notification stream from Sushi
        It receives a gRPC stream from the server, passes it to a listener and queues it up in the async loop.

        User needs to implement their own logic to process_transport_change_notifications()
        """
        try:
            stream = self._stub.SubscribeToTransportChanges(self._sushi_proto.GenericVoidValue())
            self.loop.create_task(self.process_transport_change_notifications(stream))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def subscribe_to_timing_updates(self):
        """
        Subscribes to Timing update notification stream from Sushi
        It receives a gRPC stream from the server, passes it to a listener and queues it up in the async loop.

        User needs to implement their own logic to process these notification in the placeholder methods below
        """
        try:
            stream = self._stub.SubscribeToTimingUpdates(self._sushi_proto.GenericVoidValue())
            self.loop.create_task(self.process_timing_update_notifications(stream))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def subscribe_to_track_changes(self):
        """
        Subscribes to Track change notification stream from Sushi
        It receives a gRPC stream from the server, passes it to a listener and queues it up in the async loop.

        User needs to implement their own logic to process these notification in the placeholder methods below
        """
        try:
            stream = self._stub.SubscribeToTrackChanges(self._sushi_proto.GenericVoidValue())
            self.loop.create_task(self.process_track_change_notifications(stream))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def subscribe_to_processor_changes(self):
        """
        Subscribes to Processor change notification stream from Sushi
        It receives a gRPC stream from the server, passes it to a listener and queues it up in the async loop.

        User needs to implement their own logic to process these notification in the placeholder methods below
        """
        try:
            stream = self._stub.SubscribeToProcessorChanges(self._sushi_proto.GenericVoidValue())
            self.loop.create_task(self.process_processor_change_notifications(stream))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def subscribe_to_parameter_updates(self, param_list: List[int]):
        """
        Subscribes to Parameter update notification stream from Sushi
        It receives a gRPC stream from the server, passes it to a listener and queues it up in the async loop.

        User needs to implement their own logic to process these notification in the placeholder methods below
        Args:
            param_list: a list of parameter IDs for which to get update notifications.
        """
        try:
            stream = self._stub.SubscribeToParameterUpdates(self._sushi_proto.GenericVoidValue())
            self.loop.create_task(self.process_parameter_update_notifications(stream))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    ########################################
    # API : Notification stream processing #
    ########################################

    async def process_transport_change_notifications(self, stream):
        async for notification in stream:
            # User logic here
            print(notification)

    async def process_timing_update_notifications(self, stream):
        async for notification in stream:
            # User logic here
            print(notification)

    async def process_track_change_notifications(self, stream):
        async for notification in stream:
            # User logic here
            print(notification)

    async def process_processor_change_notifications(self, stream):
        async for notification in stream:
            # User logic here
            print(notification)

    async def process_parameter_update_notifications(self, stream):
        async for notification in stream:
            # User logic here
            print(notification)