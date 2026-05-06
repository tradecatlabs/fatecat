from setuptools import setup
import os
import codecs
from lunarcalendar import __version__


def read(fname):
    """Loads the contents of a file, returning it as a string"""
    filepath = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(filepath, 'r', 'utf8').read()


setup(
    name='LunarCalendar',
    version=__version__,
    description='A lunar calendar converter, including a number of lunar and solar holidays, mainly from China.',
    long_description=read("README.rst"),
    author='wolfhong',
    author_email='hongxucai1991@gmail.com',
    url='https://github.com/wolfhong/LunarCalendar',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    keywords=[
        'lunar calendar', 'festival', 'Chinese festivals', '24 solar terms',
        'solar calendar',  'lunar solar converter', 'lunisolar calendar',
    ],
    license='MIT',
    packages=["lunarcalendar", ],
    install_requires=[
        'python-dateutil>=2.6.1',
        'ephem>=3.7.5.3',  # basic astronomical computations for Python
        'pytz',  # timezone support
    ],
    python_requires='>=2.7, <4',
    entry_points={
        'console_scripts': [
            'lunar-find=lunarcalendar.command:find',
        ],
    },
)
