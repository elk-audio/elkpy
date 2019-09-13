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
        pass

    def get_parameter_value(self, parameter_name: str) -> float:
        pass

    def get_parameters(self) -> List[str]:
        pass

    def get_parameter_values(self) -> dict:
        pass

    def set_program(self, program_name: str):
        pass

    def set_program_next(self):
        pass

    def set_program_previous(self):
        pass

    def get_program(self) -> str:
        pass

    def get_programs(self) -> List[str]:
        pass

