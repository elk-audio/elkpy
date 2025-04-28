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


############################
# Error handling functions #
############################

from typing import NoReturn


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


class SushiUnavailableError(Exception):
    pass


class SushiUnimplementedError(Exception):
    pass


def grpc_error_handling(e, context_info="") -> NoReturn:
    if e.code().name == "UNKNOWN":
        raise SushiUnkownError(e.details(), context_info) from e
    elif e.code().name == "UNAVAILABLE":
        raise SushiUnavailableError(e.details(), context_info) from e
    elif e.code().name == "UNIMPLEMENTED":
        raise SushiUnimplementedError(e.details(), context_info) from e
    else:
        if context_info != "":
            print(context_info)
        raise e
