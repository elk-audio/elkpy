############################
# Error handling functions #
############################

class SushiUnkownError(Exception):
    pass

class SushiUnsupportedOperationError(Exception):
    pass

class SushiNotFoundError(Exception):
    pass

class SushiOutOfRangeError(Exception):
    pass

class SushiInvalidArgumentError(Exception):
    pass

class SushiInternalError(Exception):
    pass

def grpc_error_handling(e, context_info = ''):
    if (e.code().name == 'UNKNOWN'):
        raise SushiUnkownError(e.details() , context_info) from e
    elif (e.code().name == 'FAILED_PRECONDITION'):
        raise SushiUnsupportedOperationError(e.details() , context_info) from e
    elif (e.code().name == 'NOT_FOUND'):
        raise SushiNotFoundError(e.details() , context_info) from e
    elif (e.code().name == 'OUT_OF_RANGE'):
        raise SushiOutOfRangeError(e.details() , context_info) from e
    elif (e.code().name == 'INVALID_ARGUMENT'):
        raise SushiInvalidArgumentError(e.details() , context_info) from e
    elif (e.code().name == 'INTERNAL'):
        raise SushiInternalError(e.details() , context_info) from e
    else:
        print(context_info)
        raise e
      #  print('Grpc error: ' + str e.code().name) + ', ' + e.details())
