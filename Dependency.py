##############################################################################
#  Copyright (c) 2019 by Paul Scherrer Institute, Switzerland
#  All rights reserved.
#  Authors: Oliver Bruendler
##############################################################################
import os

class Dependency:
    """
    This class describes a dependency
    """

    def __init__(self, libraryName : str, url : str, relativePath : str, minVersion : str):
        """
        Constructor

        :param libraryName: Name of the library
        :param url: Url of the remote git repo
        :param relativePath: Path relative to the library the dependencies are resolved for
        :param minVersion: Minimum required version
        """
        self.libraryName = libraryName
        self.url = url
        self.relativePath = relativePath
        self.minVersion = minVersion

    def GetParentDir(self) -> str:
        """
        Get parent directory
        :return: Parent directory of this dependency relative to the library the dependencies are resolved for
        """
        return os.path.dirname(self.relativePath)