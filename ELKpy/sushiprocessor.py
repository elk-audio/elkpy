from .sushicontroller import SushiController
from typing import List

class SushiProcessor(object):

    def __init__(self, processor_name: str, controller: SushiController):
        pass

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

