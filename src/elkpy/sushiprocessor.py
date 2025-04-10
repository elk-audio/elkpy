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

from .sushicontroller import SushiController
from typing import List

class SushiProcessor:
    """
    A Class to provide control of a specific processor in sushi.

    Attributes:
        _name (str): The name of the processor.
        _controller (SushiController): The sushi controller to use.
        _track_id (int): The id of the track the processor is assigned to.
        _id (int): The id corresponding to the name of the processor.
        _parameters (dict): A mapping from parameter name to parameter id.
        _programs (dict): A mapping from program name to program id.
    """
    def __init__(self, processor_name: str, controller: SushiController):
        """
        Constructor for the sushi processor. Takes the name and the controller used to control sushi.

        Parameters:
            processor_name (str): The name of the processor to control.
            controller (SushiController): The controller to use for controlling the processor.
        """
        self._name = processor_name
        self._controller = controller
        self._track_id = -1
        self._id = self._controller.audio_graph.get_processor_id(self._name)
        self._parameters = {}
        self._programs = {}


        # TODO: Use try block when error handling is approved
        for parameter in controller.parameters.get_processor_parameters(self._id):
            self._parameters[parameter.name] = parameter.id

        if (self._controller.audio_graph.get_processor_info(self._id).program_count > 0):
            # TODO: Use try block when error handling is approved
            for program in controller.programs.get_processor_programs(self._id):
                self._programs[program.name] = program.id

    #####################
    # Parameter Control #
    #####################

    def set_parameter_value(self, parameter_name: str, value: float) -> None:
        """
        Set the value of parameter by name.

        Parameters:
            parameter_name (str): The name of the parameter to set the value of.
            value (float): The value to set the parameter to.
        """
        self._controller.parameters.set_parameter_value(self._id, self._parameters[parameter_name], value)

    def get_parameter_value(self, parameter_name: str) -> float:
        """
        Get the value of a parameter by name.

        Parameters:
            parameter_name (str): The name of the parameter to get the value from.

        Returns:
            float: The current value of the parameter.
        """
        return self._controller.parameters.get_parameter_value(self._id, self._parameters[parameter_name])

    def get_parameters(self) -> List[str]:
        """
        Get a list of the names of the parameters available to the processor.

        Returns:
            List[str]: List of parameter names.
        """
        return list(self._parameters)

    def get_parameter_values(self) -> dict:
        """
        Get the current value of the parameters with their name as the key.

        Returns:
            dict: Dictionary with key as parameter names and value as the current parameter value.
        """
        parameter_values = {}
        for param in self._parameters:
            parameter_values[param] = self._controller.parameters.get_parameter_value(self._id, self._parameters[param])

        return parameter_values

    def get_bypass_state(self) -> bool:
        """
        Get the bypass state of the processor.

        Returns:
            bool: The bypass state of the processor.
        """
        return self._controller.audio_graph.get_processor_bypass_state(self._id)

    def set_bypass_state(self, bypass_state: bool) -> None:
        """
        Set the bypass state of the processor.

        Parameters:
            bypass_state (bool): The bypass state to set the processor to.
        """
        self._controller.audio_graph.set_processor_bypass_state(self._id, bypass_state)

    ###################
    # Program control #
    ###################

    def set_program(self, program_name: str) -> None:
        """
        Set the current program of the processor with the program name

        Parameters:
            program_name (str): The name of the program to set the processor to.
        """
        try:
            self._controller.programs.set_processor_program(self._id, self._programs[program_name])
        except KeyError:
            pass

    def set_program_next(self):
        """
        Set the processor to the next program or loopback to the beginning if at the end of the program list
        """
        number_of_programs = len(self._programs)
        current_program_index = self._controller.programs.get_processor_current_program(self._id)

        if current_program_index == number_of_programs-1:
            new_program_index = 0
        else:
            new_program_index = current_program_index + 1

        self._controller.programs.set_processor_program(self._id, new_program_index)

    def set_program_previous(self):
        """
        Set the processor to the previous program or loopback to the end if at the start of the program list
        """
        number_of_programs = len(self._programs)
        current_program_index = self._controller.programs.get_processor_current_program(self._id)

        if current_program_index == 0:
            new_program_index = number_of_programs-1
        else:
            new_program_index = current_program_index - 1

        self._controller.programs.set_processor_program(self._id, new_program_index)

    def get_program(self) -> str:
        """
        Get the name of the current program.

            Returns (str): The name of the current program.
        """
        return self._controller.programs.get_processor_current_program_name(self._id)

    def get_programs(self) -> List[str]:
        """
        Get a list of the names of the available programs.

            Returns:
                List[str]: The names of the available programs.
        """
        return list(self._programs)

    ####################
    # Keyboard control #
    ####################

    def send_note_on(self, channel: int, note: int, velocity: float):
        """
        Send a note on message to the track containing the processor.

        Parameters:
            channel (int): The channel to send the message on.
            note (int): The midi note value to send.
            velocity (float): The velocity of the note as a float between 0-1.
        """
        self._controller.keyboard.send_note_on(self._track_id, channel, note, velocity)

    def send_note_off(self, channel: int, note: int, velocity: float):
        """
        Send a note off message to the track containing the processor.

        Parameters:
            channel (int): The channel to send the message on.
            note (int): The midi note value to send.
            velocity (float): The velocity of the note as a float between 0-1.
        """
        self._controller.keyboard.send_note_off(self._track_id, channel, note, velocity)

    def send_note_aftertouch(self, channel: int, note: int, value: float):
        """
        Send a note aftertouch message to the track containing the processor.

        Parameters:
            channel (int): The channel to send the message on.
            note (int): The midi note value to send.
            value (float): The aftertouch value of the note as a float between 0-1.
        """
        self._controller.keyboard.send_note_aftertouch(self._track_id, channel, note, value)

    def send_aftertouch(self, channel: int, value: float):
        """
        Send a aftertouch message to the track containing the processor.

        Parameters:
            channel (int): The channel to send the message on.
            value (float): The aftertouch value of the note as a float between 0-1.
        """
        self._controller.keyboard.send_aftertouch(self._track_id, channel, value)

    def send_pitch_bend(self, channel: int, value: float):
        """
        Send a pitch bend message to the track containing the processor.

        Parameters:
            channel (int): The channel to send the message on.
            value (float): The pitch bend value of the note as a float between 0-1.
        """
        self._controller.keyboard.send_pitch_bend(self._track_id, channel, value)

    def send_modulation(self, channel: int, value: float):
        """
        Send a modulation message to the track containing the processor.

        Parameters:
            channel (int): The channel to send the message on.
            value (float): The modulation value of the note as a float between 0-1.
        """
        self._controller.keyboard.send_pitch_bend(self._track_id, channel, value)
