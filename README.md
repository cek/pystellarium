# pystellarium #

A quick-and-dirty python interface for interacting with a local running [Stellarium](https://stellarium.org/) instance.

**This project is in no way associated with (the totally amazing) Stellarium project or its developers.**

The interface is incomplete, brittle, undoubtedly buggy, and not published as a package. You almost certainly should be using Stellarium's [scripting engine]() instead. This code was thrown together in an afternoon to facilitate generating images for a separate project. Caveat emptor, abandon all hope ye who enter here, etc.

## Regenerating the class implementation

To generate the full python implementation of the Stellarium class

* Launch Stellarium on the local machine
* `cd gen`
* `python genactions.py`
* `python genprops.py`
* `cp _StellariumActions.py _StellariumProperties.py ../Stellarium`

This will generate an implementation of a python module with methods and properties reflecting those supported by the running app instance.

See the `test` directory and `gensubs.py` for example use of the generated module.

