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

import __main__
import os
import sys
import importlib
import grpc_tools.protoc as gprotoc
from types import ModuleType
from typing import Tuple 


def modules_from_proto(proto_filename: str) -> Tuple[ModuleType, ModuleType]:
    """
    Run protoc compiler and get generated modules.

    Parameters:
        proto_filename : path to .proto file with service definition

    Returns:
        (protobuf_module, grpc_module)
    """
    full_path = os.path.abspath(proto_filename)
    [inc_path, rel_proto_filename] = os.path.split(full_path)
    out_dir = "."
    if hasattr(__main__, "__file__"):
        file_path = os.path.dirname(os.path.abspath(__main__.__file__))
        if sys.path[0] == file_path:
            out_dir = file_path

    protoc_args = [ 'dummy',
                    '-I%s' % inc_path,
                    f'--python_out={out_dir}',
                    f'--grpc_python_out={out_dir}',
                    rel_proto_filename ]
    gprotoc.main(protoc_args)
    proto_base_name = os.path.splitext(rel_proto_filename)[0]
    proto_module_name = '%s_pb2' % proto_base_name
    proto_module = importlib.import_module(proto_module_name)
    grpc_module_name = '%s_pb2_grpc' % proto_base_name
    grpc_module = importlib.import_module(grpc_module_name)
    return (proto_module, grpc_module)
