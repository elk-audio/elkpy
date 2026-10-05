import struct
import threading

import zmq

from .rpc import sushi_rpc_pb2
from .rpc.sushi_rpc_pb2 import (
    AsyncCommandResponse,
    CpuTimings,
    ParameterUpdate,
    ProcessorUpdate,
    PropertyValue,
    TrackUpdate,
    TransportUpdate,
)
from .rpc.sushi_rpc_zmq import Message, NotificationControllerCommand, Service
from .sushi_info_types import CommandResponseStatus

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .sushicontroller import SushiController


class ZmqNotificationController:
    """
    ZMQ-based notification controller with the same public interface as NotificationController.

    Listens on a ZMQ SUB socket for Sushi's published events. Each call to a
    subscribe_to_* method first registers the subscription server-side via the shared
    REQ stub, then subscribes the SUB socket to the corresponding message-type prefix.

    A single background thread receives and dispatches all incoming notifications.
    """

    def __init__(
        self,
        parent: "SushiController",
        stub,
        pub_address: str,
        auto_update_async_command_responses: bool = True,
    ) -> None:
        self._parent = parent
        self._stub = stub
        # msg_type int → (response_class, [callbacks])
        self._subscriptions: dict[int, tuple[type, list]] = {}
        self._lock = threading.Lock()

        ctx = zmq.Context.instance()
        self._socket = ctx.socket(zmq.SUB)
        self._socket.connect(pub_address)

        self._running = True
        self._thread = threading.Thread(target=self._recv_loop, daemon=True)
        self._thread.start()

        if auto_update_async_command_responses:
            self._stub.SubscribeToAsyncCommandUpdates(sushi_rpc_pb2.GenericVoidValue())
            self._register(Message.ASYNC_COMMAND_RESPONSE, self._handle_command_response, AsyncCommandResponse)

    def _register(self, msg_type: Message, callback: Callable, response_class: type) -> None:
        prefix = struct.pack("<I", int(msg_type))
        with self._lock:
            if int(msg_type) not in self._subscriptions:
                self._socket.setsockopt(zmq.SUBSCRIBE, prefix)
                self._subscriptions[int(msg_type)] = (response_class, [])
            self._subscriptions[int(msg_type)][1].append(callback)

    @staticmethod
    def _filtered(cb: Callable, blocklist, key: Callable) -> Callable:
        """
        Wrap ``cb`` so that notifications matching ``blocklist`` are dropped before
        reaching it. ``key`` extracts the (processor_id, id) tuple from a notification
        to compare against the blocklist entries.

        This is client-side filtering: the server-side blocklist request is sent
        independently, but is not yet honored by Sushi over the ZMQ publish path.
        """
        blocked = {tuple(entry) for entry in blocklist}

        def wrapper(notification):
            if key(notification) not in blocked:
                cb(notification)

        return wrapper

    def _recv_loop(self) -> None:
        while self._running:
            try:
                if self._socket.poll(100):
                    frames = self._socket.recv_multipart()
                    if len(frames) < 2:
                        continue
                    msg_type = struct.unpack("<I", frames[0])[0]
                    with self._lock:
                        entry = self._subscriptions.get(msg_type)
                    if entry:
                        response_class, callbacks = entry
                        notification = response_class.FromString(frames[1])
                        for cb in callbacks:
                            cb(notification)
            except Exception:
                pass

    def _handle_command_response(self, notification: AsyncCommandResponse) -> None:
        if ev := self._parent.command_responses.get(notification.request_id):
            match notification.status.status:
                case CommandResponseStatus.SUCCESS:
                    ev.set()
                case CommandResponseStatus.ERROR:
                    ev.error = True
                    ev.set()
            self._parent.command_responses.pop(notification.request_id)

    def close(self) -> None:
        self._running = False
        self._socket.close()

    def __del__(self) -> None:
        self.close()

    # ── Public subscribe API ──────────────────────────────────────────────────

    def subscribe_to_transport_changes(self, cb: Callable) -> None:
        self._stub.SubscribeToTransportChanges(sushi_rpc_pb2.GenericVoidValue())
        self._register(Message.TRANSPORT_UPDATE, cb, TransportUpdate)

    def subscribe_to_timing_updates(self, cb: Callable) -> None:
        self._stub.SubscribeToEngineCpuTimingUpdates(sushi_rpc_pb2.GenericVoidValue())
        self._register(Message.CPU_TIMINGS, cb, CpuTimings)

    def subscribe_to_track_changes(self, cb: Callable) -> None:
        self._stub.SubscribeToTrackChanges(sushi_rpc_pb2.GenericVoidValue())
        self._register(Message.TRACK_UPDATE, cb, TrackUpdate)

    def subscribe_to_processor_changes(self, cb: Callable) -> None:
        self._stub.SubscribeToProcessorChanges(sushi_rpc_pb2.GenericVoidValue())
        self._register(Message.PROCESSOR_UPDATE, cb, ProcessorUpdate)

    def subscribe_to_parameter_updates(self, cb: Callable, param_blocklist=None) -> None:
        if param_blocklist:
            params = [
                sushi_rpc_pb2.ParameterIdentifier(processor_id=p[0], parameter_id=p[1])
                for p in param_blocklist
            ]
            request = sushi_rpc_pb2.ParameterNotificationBlocklist(parameters=params)
            cb = self._filtered(
                cb, param_blocklist, lambda n: (n.parameter.processor_id, n.parameter.parameter_id)
            )
        else:
            request = sushi_rpc_pb2.GenericVoidValue()
        self._stub.SubscribeToParameterUpdates(request)
        self._register(Message.PARAMETER_UPDATE, cb, ParameterUpdate)

    def subscribe_to_property_updates(self, cb: Callable, property_blocklist=None) -> None:
        if property_blocklist:
            props = [
                sushi_rpc_pb2.PropertyIdentifier(processor_id=p[0], property_id=p[1])
                for p in property_blocklist
            ]
            request = sushi_rpc_pb2.PropertyNotificationBlocklist(properties=props)
            cb = self._filtered(
                cb, property_blocklist, lambda n: (n.property.processor_id, n.property.property_id)
            )
        else:
            request = sushi_rpc_pb2.GenericVoidValue()
        self._stub.SubscribeToPropertyUpdates(request)
        self._register(Message.PROPERTY_VALUE, cb, PropertyValue)

    def subscribe_to_async_command_response(self, cb: Callable) -> None:
        # Server-side subscription was already registered in __init__; just add the user callback.
        self._register(Message.ASYNC_COMMAND_RESPONSE, cb, AsyncCommandResponse)
