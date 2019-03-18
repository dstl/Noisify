Release Process and Rules
=========================

All code that adds new features will be required to implement unit tests to ensure that it does not introduce
unexpected behaviour.

Pull requests that add new features will be very gladly accepted! Try and keep them small if possible. Larger requests
will naturally take longer for us to review. Please avoid adding any dependencies, if you're adding support for an extra
library then make sure this extra support is done in an optional way (importing a library in an implementation will
skip the implementation if the library is not installed, please use this for ecosystem support).

Most importantly however, thank you for contributing back to Noisify!

Versioning follows the `Semantic Versioning <https://semver.org/>`_ framework.

Major Releases
--------------

The first number in the version number is the major release (i.e ``vX.0.0``). Changes to the core
API that are not backwards compatible will result in a new major release version.
Releases of this nature will be infrequent.

Minor Releases
--------------

Minor releases will change the second number of the version number (i.e ``v0.Y.0``),
these releases will add new features, but will be fully backwards compatible with
prior versions.

Hotfix Releases
---------------

Hotfix releases will change the final number of the version (i.e ``v0.0.Z``),
these releases will consist of bug fixes between versions.
