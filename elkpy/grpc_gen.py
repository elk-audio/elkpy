import os
import importlib
import grpc_tools.protoc as gprotoc

def modules_from_proto(proto_filename):
   """ Run protoc compiler and get generated modules.
       Input:
           proto_filename : path to .proto file with service definition
       Output:
           (protobuf_module, grpc_module)
   """
   full_path = os.path.abspath(proto_filename)
   [inc_path, rel_proto_filename] = os.path.split(full_path)
   protoc_args = [ 'dummy',
                   '-I%s' % inc_path,
                   '--python_out=.',
                   '--grpc_python_out=.',
                   rel_proto_filename ]
   gprotoc.main(protoc_args)
   proto_base_name = os.path.splitext(rel_proto_filename)[0]
   proto_module_name = '%s_pb2' % proto_base_name
   proto_module = importlib.import_module(proto_module_name)
   grpc_module_name = '%s_pb2_grpc' % proto_base_name
   grpc_module = importlib.import_module(grpc_module_name)
   return (proto_module, grpc_module)