"""
This will contain the core functions of the code updating tool
"""

class GCodeUpdate:
    def __init__(self):
        pass

    def renumber(self, only_tools: bool = False):
        """
        This method gives the user the option to renumber the file with 'N' numbers.
        :param only_tools: Turning this setting to True, will remove all other N##'s and
        replace with numbered lines only with a tool change
        :return:
        """

    def add_comments(self, **kwargs):
        """
        This method takes a dictionary input and will add comments at tool changes or M00
        :param kwargs:
        :return:
        """
