# alephmarc21reader
## General 
Python library to read Marc obtained from Aleph, the catalogue of the library of the University of Basel.

Currently, this library only supports Marc21. In the future, we plan to add support for MARCXML.

## Documentation
The docstrings can be displayed with pydoc (from the project root): `pydoc alephmarcreader.AlephMarc21Reader`. 
For the inner classes such as `AlephMarc21Reader.Person`, run `pydoc alephmarcreader.AlephMarc21Reader.Person`.
 
## Unit Tests

From the project root, run `python -m unittest alephmarcreader.tests.test_Marc21Reader`

## Dependencies

- `pymarc`: install with pip

The library works both with python2 and python3.
