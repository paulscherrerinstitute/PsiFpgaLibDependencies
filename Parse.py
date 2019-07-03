##############################################################################
#  Copyright (c) 2019 by Paul Scherrer Institute, Switzerland
#  All rights reserved.
#  Authors: Oliver Bruendler
##############################################################################
import re
from .Dependency import Dependency
from typing import List


class Parse:
    """
    This class contains parsers for parsing dependencies from different sources
    """

    class Folder:
        """
        Internal class, do not use
        """
        def __init__(self, name : str, parent, indent):

            self.name = name
            self.parent = parent
            self.indent = indent
            self.subfolders = []
            self.repos = []

        def AddSubFolder(self, folder):
            self.subfolders.append(folder)

        def AddRepo(self, repo):
            self.repos.append(repo)

        def GetParentByChildIndent(self, indent):
            if indent <= self.indent:
                return self.parent.GetParentByChildIndent(indent)
            else:
                return self

        def GetPath(self):
            if self.parent.name == "ROOT":
                return self.name
            else:
                return self.parent.GetPath() + "/" + self.name

        def __str__(self):
            return self.name

    class Repo:
        """
        Internal class, do not use
        """

        def __init__(self, name : str, url : str, version : str, folder):
            self.name = name
            self.url = url
            self.version = version
            self.folder = folder

        def GetPath(self):
            return self.folder.GetPath() + "/" + self.name

        def __str__(self):
            return self.name



    @classmethod
    def FromReadme(cls, readmeFile : str) -> List[Dependency]:
        """
        Parse the dependencies from a standard PSI readme.md file.

        In order for this to work, the readme file must contain a section '#Dependencies' that list the
        folder structure and dependencies as bullet list. The library the dependencies are resolved from must
        be shown in bold (** in markdown)

        Example:

        # Dependencies

        * A folder
          * Subfolder
            * [some\_lib] (url) (1.0.0 or higher)
            * [other\_lib (url) (1.2.3)
          * OtherFolder
            * [**this\_lib**]

        :param readmeFile: Path of the readme.md file to parse
        :return: A list of dependencies
        """

        #Read File
        with open(readmeFile) as f:
            lines = f.readlines()

        #Parse content
        startFound = False
        rootFolder = cls.Folder("ROOT", None, -2)
        lastFolder = rootFolder
        allRepos = []
        thisRepo = None
        for line in lines:
            line = line.replace("\n", "")
            #Skip until dependencies found
            if "#dependencies" in line.replace(" ", "").lower():
                startFound = True
                continue
            elif not startFound:
                continue
            #Stop at next section
            if line.startswith("#"):
                break
            #Parse
            if re.sub(r"\s", "", line).startswith("*"):
                indent = line.find("*")
                text = line.split("*", 1)[1].replace(" ", "")
                #*** Repo ***
                if "[" in text:
                    name = re.findall("\[([^\]]+)]", text)[0].replace("\\", "")
                    url = re.findall("\(([^\)]+)\)", text)[0]
                    if name.startswith("**"):
                        version = "None"
                    else:
                        version = re.findall("\(([0-9\.]+)", text)[0]
                    if indent > lastFolder.indent:
                        repo = cls.Repo(name, url, version, lastFolder)
                        lastFolder.AddRepo(repo)
                    else:
                        fld = lastFolder.GetParentByChildIndent(indent)
                        repo = cls.Repo(name, url, version, fld)
                        fld.AddRepo(repo)
                    if name.startswith("**"):
                        thisRepo = repo
                    allRepos.append(repo)
                #*** Folder ***
                else:
                    #Same level
                    if indent == lastFolder.indent:
                        fold = cls.Folder(text, lastFolder.parent, indent)
                        lastFolder.parent.AddSubFolder(fold)
                    #Lower level
                    elif indent > lastFolder.indent:
                        fold = cls.Folder(text, lastFolder, indent)
                        lastFolder.AddSubFolder(fold)
                    #Higher level
                    else:
                        par = lastFolder.GetParentByChildIndent(indent)
                        fold = cls.Folder(text, par, indent)
                        par.AddSubFolder(fold)
                    lastFolder = fold
        #Check
        if thisRepo == None:
            raise Exception("Active repository not marked with **[repo]**")
        #Put together dependency list
        levelsToRoot = 1
        fld = thisRepo.folder
        while fld.name != "ROOT":
            fld = fld.parent
            levelsToRoot += 1
        pathPrefix = "/".join([".."] * levelsToRoot)
        dependencies = []
        for repo in allRepos:
            if repo != thisRepo:
                dep = Dependency(repo.name, repo.url, pathPrefix + "/" + repo.GetPath(), repo.version)
                dependencies.append(dep)
        #return list of all dependencies
        return dependencies




