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

import grpc.experimental.aio
import asyncio
from threading import Thread
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
    It allows the User, through simple API calls, to subscribe to any notification stream implemented in Sushi,
    and to attach call-back functions to each subscribed stream.

    (See the API section at the bottom of this class.)

    Attributes:
        address: gRPC server IP (str: ip:port)
        loop: an asynchronous event loop

    Notes:
        close() should ALWAYS be called as part of an application housekeeping/cleanup-before-shutdown routine as it
        ensure proper releasing of resources and clean joining of concurrent threads.
    """
    def __init__(self,
                 address='localhost:51051',
                 sushi_proto_def='/usr/share/sushi/sushi_rpc.proto'):
        """
        The constructor for the NotificationController class setting up the gRPC connection with sushi.

        Parameters:
            address (str): 'ip-address:port' The ip-address and port at which to connect to sushi.
            sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition.
        """
        self.address = address
        self.loop = asyncio.get_event_loop()
        self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self.notification_thread = Thread(target=self._run_notification_loop, args=(self.loop,))
        self.notification_thread.setDaemon(True)
        self.notification_thread.start()

    def _run_notification_loop(self, loop):
        """ Attaches the asyncio event loop to the thread and start looping over it.
            Should not be called by the User.
            """
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def close(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.notification_thread.join()

    def __del__(self):
        self.close()

    #################################################
    # Notification stream processing                #
    # Should not be called directly by the user.    #
    #################################################

    async def process_transport_change_notifications(self, call_back=None):
        try:
            async with grpc.experimental.aio.insecure_channel(self.address) as channel:
                stub = self._sushi_grpc.NotificationControllerStub(channel)
                stream = stub.SubscribeToTransportChanges(self._sushi_proto.GenericVoidValue())
                async for notification in stream:
                    # User logic here
                    if call_back and callable(call_back):
                        call_back(notification)
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)
        except AttributeError:
            raise TypeError(f"Parameter address = {self.address}. "
                            f"Should be a string containing the IP address and port to Sushi")

    async def process_timing_update_notifications(self, call_back=None):
        try:
            async with grpc.experimental.aio.insecure_channel(self.address) as channel:
                stub = self._sushi_grpc.NotificationControllerStub(channel)
                stream = stub.SubscribeToEngineCpuTimingUpdates(self._sushi_proto.GenericVoidValue())
                async for notification in stream:
                    # User logic here
                    if call_back and callable(call_back):
                        call_back(notification)
                    else:
                        raise TypeError("No valid call-back function has been provided for Timing Update "
                                        "notification processing ")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)
        except AttributeError:
            raise TypeError(f"Parameter address = {self.address}. "
                            f"Should be a string containing the IP address and port to Sushi")

    async def process_track_change_notifications(self, call_back=None):
        try:
            async with grpc.experimental.aio.insecure_channel(self.address) as channel:
                stub = self._sushi_grpc.NotificationControllerStub(channel)
                stream = stub.SubscribeToTrackChanges(self._sushi_proto.GenericVoidValue())
                async for notification in stream:
                    # User logic here
                    if call_back and callable(call_back):
                        call_back(notification)
                    else:
                        raise TypeError("No valid call-back function has been provided for Track Change "
                                        "notification processing ")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)
        except AttributeError:
            raise TypeError(f"Parameter address = {self.address}. "
                            f"Should be a string containing the IP address and port to Sushi")

    async def process_processor_change_notifications(self, call_back=None):
        try:
            async with grpc.experimental.aio.insecure_channel(self.address) as channel:
                stub = self._sushi_grpc.NotificationControllerStub(channel)
                stream = stub.SubscribeToProcessorChanges(self._sushi_proto.GenericVoidValue())
                async for notification in stream:
                    # User logic here
                    if call_back and callable(call_back):
                        call_back(notification)
                    else:
                        raise TypeError("No valid call-back function has been provided for Processor Change "
                                        "notification processing ")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)
        except AttributeError:
            raise TypeError(f"Parameter address = {self.address}. "
                            f"Should be a string containing the IP address and port to Sushi")

    async def process_parameter_update_notifications(self, call_back=None, param_list=None):
        if not param_list:
            block_list = self._sushi_proto.GenericVoidValue()
        else:
            p_list = []
            for p in param_list:
                param = self._sushi_proto.ParameterIdentifier(processor_id=p[0], parameter_id=p[1])
                p_list.append(param)
            block_list = self._sushi_proto.ParameterNotificationBlocklist(parameters=p_list)
        try:
            async with grpc.experimental.aio.insecure_channel(self.address) as channel:
                stub = self._sushi_grpc.NotificationControllerStub(channel)
                stream = stub.SubscribeToParameterUpdates(block_list)
                async for notification in stream:
                    # User logic here
                    if call_back and callable(call_back):
                        call_back(notification)
                    else:
                        raise TypeError("No valid call-back function has been provided for Parameter Update "
                                        "notification processing ")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)
        except AttributeError:
            raise TypeError(f"Parameter address = {self.address}. "
                            f"Should be a string containing the IP address and port to Sushi")

    async def process_property_update_notifications(self, call_back=None, property_list=None):
        if not property_list:
            block_list = self._sushi_proto.GenericVoidValue()
        else:
            p_list = []
            for p in property_list:
                property = self._sushi_proto.PropertyIdentifier(processor_id=p[0], property_id=p[1])
                p_list.append(param)
            block_list = self._sushi_proto.PropertyNotificationBlocklist(properties=p_list)
        try:
            async with grpc.experimental.aio.insecure_channel(self.address) as channel:
                stub = self._sushi_grpc.NotificationControllerStub(channel)
                stream = stub.SubscribeToPropertyUpdates(block_list)
                async for notification in stream:
                    # User logic here
                    if call_back and callable(call_back):
                        call_back(notification)
                    else:
                        raise TypeError("No valid call-back function has been provided for Property Change "
                                        "notification processing ")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)
        except AttributeError:
            raise TypeError(f"Parameter address = {self.address}. "
                            f"Should be a string containing the IP address and port to Sushi")

    ####################################################
    # API : Subscription to Sushi notification streams #
    ####################################################

    def subscribe_to_transport_changes(self, cb) -> None:
        """
        Subscribes to Transport changes notification stream from Sushi
        User needs to implement their own stream consumer logic and pass it as cb.

        Parameters:
            cb: a callable that will be called for each notification received from the stream.
        """
        asyncio.run_coroutine_threadsafe(self.process_transport_change_notifications(cb), self.loop)

    def subscribe_to_timing_updates(self, cb):
        """
        Subscribes to Timing update notification stream from Sushi
        User needs to implement their own stream consumer logic and pass it as cb.

        Parameters:
            cb: a callable that will be called for each notification received from the stream.        """
        asyncio.run_coroutine_threadsafe(self.process_timing_update_notifications(cb), self.loop)

    def subscribe_to_track_changes(self, cb):
        """
        Subscribes to Track change notification stream from Sushi.
        User needs to implement their own stream consumer logic and pass it as cb.

        Parameters:
            cb: a callable that will be called for each notification received from the stream.
        """
        asyncio.run_coroutine_threadsafe(self.process_track_change_notifications(cb), self.loop)

    def subscribe_to_processor_changes(self, cb):
        """
        Subscribes to Processor change notification stream from Sushi.
        User needs to implement their own stream consumer logic and pass it as cb.

        Parameters:
            cb: a callable that will be called for each notification received from the stream.
        """
        asyncio.run_coroutine_threadsafe(self.process_processor_change_notifications(cb), self.loop)

    def subscribe_to_parameter_updates(self, cb, param_blocklist=None):
        """
        Subscribes to Parameter update notification stream from Sushi
        User needs to implement their own logic to process these notification in the placeholder methods below

        Parameters:
            cb: a callable that will be called for each notification received from the stream.
            param_blocklist: a list of parameter identifiers for which to block update notifications. \
                        A parameter identifier is itself a list of [processor_id: int, parameter_id: int] \
                        If no param_blocklist is passed, all parameter notifications will be subscribed to. \

        Notes to write useful callbacks:
            Notification objects have 2 attributes: parameter and value;
            Parameter itself has 2 attributes: processor_id and _parameter_id;
            ex: notification.parameter.parameter_id (gets the parameter ID)
            ex: notification.parameter.processor_id (gets the processor ID)
            ex: notification.normalized_value (gets the value normalized between 0 and 1)
            ex: notification.domain_value (gets the domain value)
            ex: notification.formatted_value (gets the value formatted as a string)
        """
        asyncio.run_coroutine_threadsafe(self.process_parameter_update_notifications(cb, param_blocklist), self.loop)

    def subscribe_to_property_updates(self, cb, property_blocklist=None):
        """
        Subscribes to Property update notification stream from Sushi
        User needs to implement their own logic to process these notification in the placeholder methods below

        Parameters:
            cb: a callable that will be called for each notification received from the stream.

        Notes to write useful callbacks:
            Notification objects have 2 attributes: property and value;
            Property itself has 2 attributes: processor_id and property_id;
            ex: notification.parameter.property_id (gets the property ID)
            ex: notification.parameter.processor_id (gets the processor ID)
            ex: notification.value (gets the value)
        """
        asyncio.run_coroutine_threadsafe(self.process_property_update_notifications(cb, property_blocklist), self.loop)
