##############################################################################
#  Copyright (c) 2019 by Paul Scherrer Institute, Switzerland
#  All rights reserved.
#  Authors: Oliver Bruendler
##############################################################################

import setuptools
import shutil
import os
from setuptools.command.sdist import sdist

#Cleanup before sdist
class CustomSdist(sdist):
    def run(self):
        #Cleanup before building
        shutil.rmtree("dist", ignore_errors=True)
        shutil.rmtree("PsiFpgaLibDependencies.egg-info", ignore_errors=True)

        #Build from directory above
        sdist.run(self)

#Package
setuptools.setup(
    name="PsiFpgaLibDependencies",
    version="2.1.0",
    author="Oliver Bründler",
    author_email="oliver.bruendler@psi.ch",
    description="Automatic checkout of dependencies for PSI Libraries",
    license="PSI HDL Library License, Version 1.0",
    url="https://github.com/paulscherrerinstitute/PsiFpgaLibDependencies",
    package_dir = {"PsiFpgaLibDependencies" : "."},
    packages = ["PsiFpgaLibDependencies"],
    install_requires = [
        "typing"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    cmdclass = {
        "sdist" : CustomSdist
    }
)