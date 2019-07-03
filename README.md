# General Information

## Maintainer
Oliver Bründler [oliver.bruendler@psi.ch]

## License
This library is published under [PSI HDL Library License](License.txt), which is [LGPL](LGPL2_1.txt) plus some additional exceptions to clarify the LGPL terms in the context of firmware development.

## Changelog
See [Changelog](Changelog.md)

## Dependencies
None

## Tagging Policy
Stable releases are tagged in the form *major*.*minor*.*bugfix*. 

* Whenever a change is not fully backward compatible, the *major* version number is incremented
* Whenever new features are added, the *minor* version number is incremented
* If only bugs are fixed (i.e. no functional changes are applied), the *bugfix* version is incremented

# Description
This package allows parsing PSI library dependencies from the standard README.md files. Dependencies can then be listed, checked out or added as submodule to a project.

To parse the dependencies correctly, the README.md file must follow the PSI standard:
* Separate section **# Dependencies**
* In that section, dependencies are listed in a bullet list
* Add indent for every folder level
* Add submodules in the form **\[name\]\(url\)(1.0.0)**
* For an example, look at the repository mentioned below

For the exact usage, refer to the [psi_common Library](https://github.com/paulscherrerinstitute/psi_common).

# Installation
For using the package, it must be installed locally. To do so, download the archive in **dist** and install it using pip:

```
pip3 install <archive>
```

# Packaing
To package the project after making changes, update the version number in *setup.py* and run

```
python3 setup.py sdist
```




 