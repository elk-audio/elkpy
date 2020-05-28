import grpc

from . import sushierrors
from . import grpc_gen
from . import sushi_info_types as info_types
from typing import List

####################################
# Sushi program controller class #
####################################

class ProgramController(object):
    '''
    A class to control the program in sushi via gRPC.

    Attributes:
        _stub (ProgramControllerStub): Connection stubs to the gRPC program interface implemented in sushi.
    '''
    def __init__(self,
                 address = 'localhost:51051',
                 sushi_proto_def = '/usr/share/sushi/sushi_rpc.proto'):
        '''
        The constructor for the ProgramController class.

        Parameters:
            address (str): 'ip-addres:port' The ip-addres and port at which to connect to sushi.
            sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition
        '''
        try:
            channel = grpc.insecure_channel(address)
        except AttributeError as e:
            raise TypeError("Parameter address = {}. Should be a string containing the ip-address and port of sushi ('ip-address:port')".format(address)) from e

        self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self._stub = self._sushi_grpc.ProgramControllerStub(channel)

    def get_processor_current_program(self, processor_identifier: int) -> int:
        '''
        Get the id of the current program of the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the current program id from.

        Returns:
            int: The id of the processors current program.
        '''
        try:
            response = self._stub.GetProcessorCurrentProgram(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))
            return response.program

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))

    def get_processor_current_program_name(self, processor_identifier: int) -> str:
        '''
        Get the name of the current program of the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the current program name from.

        Returns:
            str: The name of the processors current program.
        '''
        try:
            response = self._stub.GetProcessorCurrentProgramName(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))

    def get_processor_program_name(self, processor_identifier: int, program_identifier: int) -> str:
        '''
        Get the name of the specified program on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the program name from.
            program_identifier (int): The id of the program to get the name of.

        Returns:
            str: The name of the program matching the processor and program id.
        '''
        try:
            response = self._stub.GetProcessorProgramName(self._sushi_proto.ProcessorProgramIdentifier(
                processor = self._sushi_proto.ProcessorIdentifier(id = processor_identifier),
                program = program_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, program id: {}".format(processor_identifier, program_identifier))

    def get_processor_programs(self, processor_identifier: int) -> List[info_types.ProgramInfo]:
        '''
        Get a list of the available programs of the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the programs from.

        Returns:
            List[info_types.ProgramInfo]: A list of the programs available to the processor matching the id.
        '''
        try:
            response = self._stub.GetProcessorPrograms(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))

            program_info_list = []
            for program_info in response.programs:
                program_info_list.append(info_types.ProgramInfo(program_info))

            return program_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))

    def set_processor_program(self, processor_identifier: int, program_identifier: int) -> None:
        '''
        Set the program of the specified processor to the one matching the specified program id.

        Parameters:
            processor_identifier (int): The id of the processor to set the program of.
            program_identifier (int): The id of the program to set.
        '''
        try:
            self._stub.SetProcessorProgram(self._sushi_proto.ProcessorProgramSetRequest(
                processor = self._sushi_proto.ProcessorIdentifier(id = processor_identifier),
                program = self._sushi_proto.ProgramIdentifier(program = program_identifier)
            ))

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, program id: {}".format(processor_identifier, program_identifier))
