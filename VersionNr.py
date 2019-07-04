##############################################################################
#  Copyright (c) 2019 by Paul Scherrer Institute, Switzerland
#  All rights reserved.
#  Authors: Oliver Bruendler
##############################################################################
class VersionNr:

    def __init__(self, version : str):
        parts = version.strip().split(".")
        if len(parts) < 3:
            raise Exception("Got illegal version number: {}".format(version))
        self.major = int(parts[0])
        self.minor = int(parts[1])
        self.bugfix = int(parts[2])

    def __eq__(self, other):
        if self.major != other.major:
            return False
        if self.minor != other.minor:
            return False
        if self.bugfix != other.bugfix:
            return False
        return True

    def __gt__(self, other):
        if self.major > other.major:
            return True
        elif self.major < other.major:
            return False
        elif self.minor > other.minor:
            return True
        elif self.minor < other.minor:
            return False
        elif self.bugfix > other.bugfix:
            return True
        else:
            return False

    def __str__(self):
        return "{}.{}.{}".format(self.major, self.minor, self.bugfix)
