##############################################################################
#  Copyright (c) 2019 by Paul Scherrer Institute, Switzerland
#  All rights reserved.
#  Authors: Oliver Bruendler
##############################################################################
from .Dependency import Dependency
from typing import List
from enum import Enum
import os
from argparse import ArgumentParser
import subprocess

##############################################################################
# Definitions
##############################################################################
def PSI_GFA_HTTPS_TO_SSH(path : str) -> str:
    """
    Convert PSI-GIT URLs into SSH URLs
    :param path:
    :return:
    """
    if path.startswith("https://git.psi.ch/GFA"):
        path = path.replace("https://git.psi.ch/GFA", "git@git.psi.ch:GFA")
        path += ".git"
    return path

#All URL replacement (more may be added in future)
URL_REPLACEMENTS = [PSI_GFA_HTTPS_TO_SSH]

class CHECKOUT_MODE(Enum):
    """
    Checkout mode
    """
    Master = 0
    LatestRelease = 1
    SpecifiedRelease = 2

class DependencyDoesNotExistException(Exception):
    pass

##############################################################################
# Actions
##############################################################################
def ListDependencies(deps : List[Dependency]):
    """
    List all dependencies
    :param deps: A list of dependencies
    """
    for dep in deps:
        print("{} - {} - {}".format(dep.libraryName, dep.url, dep.minVersion))

def CheckIfPresent(rootdir : str, deps : List[Dependency]):
    """
    Check if all dependencies are present and throw an exception otherwise
    :param rootdir: Directory to check the dependencies relative to
    :param deps: List of dependencies
    """
    oldDir = os.path.abspath(os.curdir)
    try:
        os.chdir(rootdir)
        for dep in deps:
            if os.path.isdir(dep.relativePath):
                continue
            else:
                raise DependencyDoesNotExistException("Dependency {} does not exist".format(dep.relativePath))
    finally:
        os.chdir(oldDir)


def Checkout(rootdir : str, deps : List[Dependency], mode : CHECKOUT_MODE = CHECKOUT_MODE.Master, asSubmodule : bool = False):
    """
    Checkout all dependencies
    :param rootdir: Directory to check the dependencies relative to
    :param deps: List of dependencies
    :param mode: Checkout mode (checkout master or latest release or exact version specified)
    :param asSubmodule: True = Add dependencies as submodule, False = checkout only
    """
    oldDir = os.path.abspath(os.curdir)
    rootdir = os.path.abspath(rootdir)
    try:
        for dep in deps:
            os.chdir(rootdir)
            parent = os.path.abspath(dep.GetParentDir())
            if os.path.exists(dep.relativePath):
                print("> {} skipped, already exists".format(dep.relativePath))
            else:
                print("> checkout {}".format(dep.relativePath))
                if not os.path.exists(parent):
                    os.makedirs(parent, exist_ok=True)
                os.chdir(parent)
                url = dep.url
                for repl in URL_REPLACEMENTS:
                    url = repl(url)
                if not asSubmodule:
                    os.system("git clone --recurse-submodules {} {}".format(url, dep.libraryName))
                else:
                    os.system("git submodule add {} {}".format(PSI_GFA_HTTPS_TO_SSH(url), dep.libraryName))
                if mode == CHECKOUT_MODE.SpecifiedRelease:
                    os.chdir(dep.libraryName)
                    os.system("git checkout {}".format(dep.minVersion))
                elif mode == CHECKOUT_MODE.LatestRelease:
                    os.chdir(dep.libraryName)
                    latest = subprocess.check_output("git describe --tags").decode()
                    os.system("git checkout {}".format(latest))
    finally:
        os.chdir(oldDir)

def ExecMain(repoPath : str, dependencies : List[Dependency]):
    """
    Execute program as main and parse arguments from command line
    :param repoPath: Path of the repository to check dependencies
    :param dependencies: List of dependencies
    """
    parser = ArgumentParser()
    parser.add_argument("-list", dest="list", help="List all dependencies", required=False, default=False, action="store_true")
    parser.add_argument("-check", dest="check", help="Check if all dependencies are present", required=False, default=False, action="store_true")
    parser.add_argument("-checkout", dest="checkout", help="Checkout dependencies", required=False,default=False, action="store_true")
    parser.add_argument("-as_submodule", dest="as_submodule", help="Add dependencies as submodules (must be used together with -checkout)", required=False, default=False, action="store_true")
    parser.add_argument("-mode", dest="mode", help="Checkout mode", choices=["master", "latest_release", "specified_version"], required=False, default="latest_release")
    args = parser.parse_args()

    if args.list:
        print("*** Dependencies ***")
        ListDependencies(dependencies)

    if args.check:
        print("*** Dependency Check ***")
        try:
            CheckIfPresent(repoPath, dependencies)
        except Exception as e:
            print(e)

    if args.checkout:
        print("*** Checkout ***")
        if args.mode == "latest_release":
            mode = CHECKOUT_MODE.LatestRelease
        elif args.mode == "master":
            mode = CHECKOUT_MODE.Master
        elif args.mode == "specified_version":
            mode = CHECKOUT_MODE.SpecifiedRelease
        else:
            raise Exception("Illegel -mode: {}".format(args.mode))
        Checkout(repoPath, dependencies, mode, args.as_submodule)

