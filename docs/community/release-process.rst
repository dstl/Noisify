Release Process and Rules
=========================

All code will be required to implement unit tests to ensure that it does not introduce
unexpected behaviour.

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
