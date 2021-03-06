import os
import re
import sys

if sys.version_info[:2] < (2, 7):
    sys.exit("virtualenv requires Python 2.7 or higher.")
try:
    from setuptools import setup, find_packages
    from setuptools.command.test import test as TestCommand

    class PyTest(TestCommand):
        user_options = [("pytest-args=", "a", "Arguments to pass to py.test")]

        def initialize_options(self):
            TestCommand.initialize_options(self)
            self.pytest_args = []

        def finalize_options(self):
            TestCommand.finalize_options(self)
            # self.test_args = []
            # self.test_suite = True

        def run_tests(self):
            # import here, because outside the eggs aren't loaded
            import pytest

            sys.exit(pytest.main(self.pytest_args))

    setup_params = {
        "entry_points": {"console_scripts": ["virtualenv=virtualenv:main"]},
        "zip_safe": False,
        "cmdclass": {"test": PyTest},
        "tests_require": ["pytest", "mock"],
    }
except ImportError:
    from distutils.core import setup

    if sys.platform == "win32":
        print("Note: without Setuptools installed you will " 'have to use "python -m virtualenv ENV"')
        setup_params = {}
    else:
        script = "scripts/virtualenv"
        setup_params = {"scripts": [script]}


def read_file(*paths):
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, *paths)) as f:
        return f.read()


# Get long_description from index.rst:
long_description_full = read_file("docs", "index.rst")
long_description = long_description_full.strip().split("split here", 1)[0]
long_description += "\n\n`Read the changelog here <https://virtualenv.pypa.io/en/latest/changes.html>`_."


def get_version():
    version_file = read_file(os.path.realpath(os.path.join(".", "virtualenv.py")))
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Hack to prevent stupid TypeError: 'NoneType' object is not callable error on
# exit of python setup.py test # in multiprocessing/util.py _exit_function when
# running python setup.py test (see
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing  # noqa
except ImportError:
    pass

setup(
    name="virtualenv",
    version=get_version(),
    description="Virtual Python Environment builder",
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="setuptools deployment installation distutils",
    author="Ian Bicking",
    author_email="ianb@colorstudy.com",
    maintainer="Jannis Leidel, Carl Meyer and Brian Rosner",
    maintainer_email="python-virtualenv@groups.google.com",
    url="https://virtualenv.pypa.io/",
    license="MIT",
    package_dir={"": "."},
    py_modules=["virtualenv"],
    packages=find_packages("."),
    package_data={"virtualenv_support": ["*.whl"]},
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
    extras_require={
        "testing": [
            'mock;python_version<"3.3"',
            "pytest >= 4.0.0, <5",
            "coverage >= 4.5.0, <5",
            'pytest-timeout >= 1.3.0, <2; platform_python_implementation!="Jython"',
            'xonsh; python_version>="3.4"',
            "six >= 1.10.0, < 2",
        ],
        "docs": ["sphinx >= 1.8.0, < 2", "towncrier >= 18.5.0", "sphinx_rtd_theme >= 0.4.2, < 1"],
    },
    **setup_params
)
