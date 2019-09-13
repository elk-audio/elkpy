from . import sushicontroller as sc
from .sushicontroller import SushiController
from typing import List

class SushiProcessor(object):
    '''
    A Class to provide control of a specific processor in sushi.

    Attributes:
        _name (str): The name of the processor.
        _controller (SushiController): The sushi controller to use.
        _id (int): The id corresponding to the name of the processor.
        _parameters (dict): A mapping from parameter name to parameter id.
        _programs (dict): A mapping from program name to program id.
    '''
    def __init__(self, processor_name: str, controller: SushiController):
        '''
        Constructor for the sushi processor. Takes the name and the controller used to control sushi.

        Parameters:
            processor_name (str): The name of the processor to control.
            controller (SushiController): The controller to use for controlling the processor.
        '''
        self._name = processor_name
        self._controller = controller
        
        # TODO: Use try block when error handling is approved
        for track in controller.get_tracks():
            for processor in controller.get_track_processors(track.id):
                if processor.name == self._name:
                    self._id = processor.id

        # TODO: Use try block when error handling is approved
        self._parameters = {}
        for parameter in controller.get_processor_parameters(self._id):
            self._parameters[parameter.name] = parameter.id
        
        # TODO: Use try block when error handling is approved
        self._programs = {}
        for program in controller.get_processor_programs(self._id):
            self._programs[program.name] = program.id

    def set_parameter_value(self, parameter_name: str, value: float) -> None:
        '''
        Set the value of parameter by name.

        Parameters:
            parameter_name (str): The name of the parameter to set the value of.
            value (float): The value to set the parameter to.
        '''
        self._controller.set_parameter_value(self._id, self._parameters[parameter_name], value)

    def get_parameter_value(self, parameter_name: str) -> float:
        '''
        Get the value of a parameter by name.

        Parameters:
            parameter_name (str): The name of the parameter to get the value from.

        Returns:
            float: The current value of the parameter.
        '''
        return self._controller.get_parameter_value(self._id, self._parameters[parameter_name])

    def get_parameters(self) -> List[str]:
        '''
        Get a list of the names of the parameters available to the processor.

        Returns:
            List[str]: List of parameter names.
        '''
        return list(self._parameters)

    def get_parameter_values(self) -> dict:
        '''
        Get the current value of the parameters with their name as the key.

        Returns:
            dict: Dictionary with key as parameter names and value as the current parameter value.
        '''
        parameter_values = {}
        for param in self._parameters:
            parameter_values[param] = self._controller.get_parameter_value(self._id, self._parameters[param])

        return parameter_values

    def set_program(self, program_name: str) -> None:
        '''
        Set the current program of the processor with the program name

        Parameters:
            program_name (str): The name of the program to set the processor to.
        '''
        self._controller.set_processor_program(self._id, self._programs[program_name])

    def set_program_next(self):
        '''
        Set the processor to the next program or loopback to the beginning if at the end of the program list
        '''
        number_of_programs = len(self._programs)
        current_program_index = self._controller.get_processor_current_program(self._id)
        
        if current_program_index == number_of_programs-1:
            new_program_index = 0
        else:
            new_program_index = current_program_index + 1

        self._controller.set_processor_program(self._id, new_program_index)

    def set_program_previous(self):
        '''
        Set the processor to the previous program or loopback to the end if at the start of the program list
        '''
        number_of_programs = len(self._programs)
        current_program_index = self._controller.get_processor_current_program(self._id)
        
        if current_program_index == 0:
            new_program_index = number_of_programs-1
        else:
            new_program_index = current_program_index - 1

        self._controller.set_processor_program(self._id, new_program_index)

    def get_program(self) -> str:
        '''
        Get the name of the current program.

            Returns (str): The name of the current program.
        '''
        return self._controller.get_processor_current_program_name(self._id)

    def get_programs(self) -> List[str]:
        '''
        Get a list of the names of the available programs.

            Returns:
                List[str]: The names of the available programs.
        '''
        return list(self._programs)

