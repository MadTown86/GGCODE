"""
This class will house error/exception handling for the GGCODE project.
"""
import traceback
from GGCODE.ggcode_errormsgbox import GGCODE_ErrorMsgBox as MB


class ToolNotFoundException(BaseException):
    """
    This exception is raised when a tool is not found in the tool database.

    This can be caused if during initial parsing whole tool numbers are not identified correctly.

    Examples: If 'T' is incorrectly found as an initial tool number, then can't be found during parsing or updating.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidToolException(OverflowError):
    """
    This exception is raised when no tool is selected when attempting to log tool update information.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class InvalidFileFormat(BaseException):
    """
    This exception is raised when a few things aren't found in the file, which determines whether it is a valid GCODE
    file or not.

    The initial example is that the first line of the file that contains text needs to have a % symbol as does
    the last line of text found in the file.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidOffsetEntry(BaseException):
    """
    This exception is raised when an invalid offset is entered into the work offset tab.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)





