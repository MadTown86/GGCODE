"""
This class will house error/exception handling for the GGCODE project.
"""
from GGCODE.ggcode_errormsgbox import GGCODE_ErrorMsgBox as MB


class ToolNotFoundException(BaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messagebox = MB()
        self.messagebox.setMsg('Tool Not Found')
        self.messagebox.setStackTrace(self.__context__)
        MB.mainloop()


