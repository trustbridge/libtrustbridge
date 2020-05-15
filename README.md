Trustbridge library
===================

Run tests:
----------

To run test locally, first setup new venv and install the package:

```
pip install -e ".[testing]"
```
Run the tests:

```
py.test
```


Development along with the Intergov
-----------------------------------

1. checkout the intergov repository
2. checkout the trustbridge repo in the `intergov` folder of intergov repo
3. ensure that PYTHONPATH contains the libtrustrbridge code (looks like `PYTHONPATH=/src/:/src/intergov/libtrustbridge/`)
4. start the intergov as usual

Now any changes you made in the checked out repo will be immediately applicable in your node - thanks to smart PYTHONPATH configuration.
