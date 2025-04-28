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

from . import sushierrors
from . import grpc_gen

####################################
# Sushi keyboard controller class #
####################################

class KeyboardController(object):
    """
    A class to control the keyboard in sushi via gRPC. It can send typical keyboard events like
    note on, note off, pitch bend, modulation and after touch.

    Attributes:
        _stub (KeyboardControllerStub): Connection stubs to the gRPC keyboard interface implemented in sushi.
    """
    def __init__(self,
                 parent,
                 address = 'localhost:51051',
                 sushi_proto_def = '/usr/share/sushi/sushi_rpc.proto',
                 sushi_proto = None, sushi_grpc = None):
        """
        The constructor for the KeyboardController class setting up the gRPC connection with sushi.

        Parameters:
            address (str): 'ip-addres:port' The ip-addres and port at which to connect to sushi.
            sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition
        """
        try:
            channel = grpc.insecure_channel(address)
        except AttributeError as e:
            raise TypeError("Parameter address = {}. Should be a string containing the ip-address and port of sushi ('ip-address:port')".format(address)) from e

        if sushi_proto and sushi_grpc:
            self._sushi_proto = sushi_proto
            self._sushi_grpc = sushi_grpc
        else:
            self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self._stub = self._sushi_grpc.KeyboardControllerStub(channel)
        self._parent = parent

    #######################
    # // Keyboard control #
    #######################

    def send_note_on(self, track_identifier: int, channel: int, note: int, velocity: float) -> None:
        """
        Sends a note on message to the specified track.

        Parameters:
            track_identifier (int): The id of the track that should receive the message.
            channel (int): The channel on which the message should be sent.
            note (int): The note to send. Follows the MIDI standard where middle c = 60.
            velocity (float): The velocity of the note. Should be in range (0.0-1.0).
        """
        try:
            cr = self._stub.SendNoteOn(self._sushi_proto.NoteOnRequest(
                track = self._sushi_proto.TrackIdentifier(id = track_identifier),
                channel = channel,
                note = note,
                velocity = velocity
            ))
            return self._parent.validate_command_response(cr, "Sending NoteOn")

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, " With track id: {}, channel: {}, note: {}, velocity: {}".format(track_identifier, channel, note, velocity))

    def send_note_off(self, track_identifier: int, channel: int, note: int, velocity: float) -> None:
        """
        Sends a note off message to the specified track.

        Parameters:
            track_identifier (int): The id of the track that should receive the message.
            channel (int): The channel on which the message should be sent.
            note (int): The note to send. Follows the MIDI standard where middle c = 60.
            velocity (float): The velocity of the note. Should be in range (0.0-1.0).
        """
        try:
            cr = self._stub.SendNoteOff(self._sushi_proto.NoteOffRequest(
                track = self._sushi_proto.TrackIdentifier(id = track_identifier),
                channel = channel,
                note = note,
                velocity = velocity
            ))
            return self._parent.validate_command_response(cr, "Sending NoteOff")

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, " With track id: {}, channel: {}, note: {}, velocity: {}".format(track_identifier, channel, note, velocity))

    def send_note_aftertouch(self, track_identifier: int, channel: int, note: int, value: float) -> None:
        """
        Sends a aftertouch message to the specified track and note.

        Parameters:
            track_identifier (int): The id of the track that should receive the message.
            channel (int): The channel on which the message should be sent.
            note (int): The note which should receive the message. Follows the MIDI standard where middle c = 60.
            value (float): The aftertouch value of the note. Should be in range (0.0-1.0).
        """
        try:
            cr = self._stub.SendNoteAftertouch(self._sushi_proto.NoteAftertouchRequest(
                track = self._sushi_proto.TrackIdentifier(id = track_identifier),
                channel = channel,
                note = note,
                value = value
            ))
            return self._parent.validate_command_response(cr, "Sending NoteAfterTouch")

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, " With track id: {}, channel: {}, note: {}, value: {}".format(track_identifier, channel, note, value))

    def send_aftertouch(self, track_identifier: int, channel: int, value: float) -> None:
        """
        Sends a aftertouch message to the specified track.

        Parameters:
            track_identifier (int): The id of the track that should receive the message.
            channel (int): The channel on which the message should be sent.
            value (float): The aftertouch value. Should be in range (0.0-1.0).
        """
        try:
            cr = self._stub.SendAftertouch(self._sushi_proto.NoteModulationRequest(
                track = self._sushi_proto.TrackIdentifier(id = track_identifier),
                channel = channel,
                value = value
            ))
            return self._parent.validate_command_response(cr, "Sending AfterTouch")

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, " With track id: {}, channel: {}, value: {}".format(track_identifier, channel, value))

    def send_pitch_bend(self, track_identifier: int, channel: int, value: float) -> None:
        """
        Sends a pitch bend message to the specified track.

        Parameters:
            track_identifier (int): The id of the track that should receive the message.
            channel (int): The channel on which the message should be sent.
            value (float): The pitch bend value. Should be in range (0.0-1.0).
        """
        try:
            cr = self._stub.SendPitchBend(self._sushi_proto.NoteModulationRequest(
                track = self._sushi_proto.TrackIdentifier(id = track_identifier),
                channel = channel,
                value = value
            ))
            return self._parent.validate_command_response(cr, "Sending Pitchbend")

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, " With track id: {}, channel: {}, value: {}".format(track_identifier, channel, value))

    def send_modulation(self, track_identifier: int, channel: int, value: float) -> None:
        """
        Sends a modulation message to the specified track.

        Parameters:
            track_identifier (int): The id of the track that should receive the message.
            channel (int): The channel on which the message should be sent.
            value (float): The modulation value. Should be in range (0.0-1.0).
        """
        try:
            cr = self._stub.SendModulation(self._sushi_proto.NoteModulationRequest(
                track = self._sushi_proto.TrackIdentifier(id = track_identifier),
                channel = channel,
                value = value
            ))
            return self._parent.validate_command_response(cr, "Sending Modulation")

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, " With track id: {}, channel: {}, value: {}".format(track_identifier, channel, value))
