# setup.py for building c_numpy_demo package. since extension modules can't be
# built without setup.py, we can't use the new PEP 517 format.

from setuptools import Extension, setup
from numpy import get_include

# package name and path for _np_bcast extension source code
_PACKAGE_NAME = "c_npy_demo"
_NP_BCAST_SRC_PATH = _PACKAGE_NAME + "/_np_bcast"


def _get_ext_modules():
    """Returns a list of :class:`~setuptools.Extension` modules to build.
    
    .. note:: The extensions must be true modules, i.e. define a ``PyInit_*``
       function. Use alternate means to build foreign C code.
    
    :rtype: list
    """
    # use get_include to get numpy include directory + add -std=gnu11 so that
    # the extension will build on older distros with old gcc like 4.8.2
    _np_bcast = Extension(
        name = "_np_bcast",
        sources = [_NP_BCAST_SRC_PATH + "/np_broadcast.c",
                   _NP_BCAST_SRC_PATH + "/_modinit.c"],
        include_dirs = [get_include()],
        extra_compile_args = ["-std=gnu11"]
    )
    return [_np_bcast]


def _setup():
    # get version
    with open("VERSION", "r") as vf:
        version = vf.read().rstrip()
    # short and long descriptions
    short_desc = (
        "A Python package demoing the combined use of ctypes, an extension "
        "module, and the NumPy C API."
    )
    with open("README.rst", "r") as rf:
        long_desc = rf.read()
    # perform setup
    setup(
        name = _PACKAGE_NAME,
        version = version,
        description = short_desc,
        long_description = long_desc,
        long_description_content_type = "text/x-rst",
        author = "Derek Huang",
        author_email = "djh458@stern.nyu.edu",
        license = "MIT",
        url = "https://github.com/phetdam/c_npy_demo",
        classifiers = [
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8"
        ],
        project_urls = {
            "Source": "https://github.com/phetdam/c_npy_demo"
        },
        python_requires = ">=3.6",
        packages = [_PACKAGE_NAME, _PACKAGE_NAME + ".tests"],
        # adds implied vol shared object, data files, and data README.rst
        package_data = {
            _PACKAGE_NAME: ["_ivlib.so", "data/*.csv", "data/*.rst"]
        },
        # benchmarking scripts
        entry_points = {
            "console_scripts": [
                (
                    _PACKAGE_NAME + ".bench.ext = " + _PACKAGE_NAME +
                    ".bench:bench_ext_main"
                ),
                (
                    _PACKAGE_NAME + ".bench.vol = " + _PACKAGE_NAME +
                    ".bench:bench_vol_main"
                )
              ]
          },
        install_requires = ["numpy>=1.19", "scipy>=1.5"],
        ext_package = _PACKAGE_NAME,
        ext_modules = _get_ext_modules()
    )


if __name__ == "__main__":
    _setup()
