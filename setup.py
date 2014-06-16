"""
Setup script for Time2Pull

You will need to install Python 3 and PyQt5
"""
import os
import sys
from setuptools import setup, find_packages


def read_version():
    """
    Reads the version without self importing
    """
    with open("time2pull/__init__.py") as f:
        lines = f.read().splitlines()
        for l in lines:
            if "__version__" in l:
                return l.split("=")[1].strip().replace('"', "").replace("'", '')


def run_as_root():
    return os.getuid() == 0


# get long description
with open('README.rst', 'r') as readme:
    long_desc = readme.read()


# install requirements
requirements = []

data_files = []
if (sys.platform == "linux" and
        ('install' in sys.argv or 'develop' in sys.argv) and
        run_as_root()):
    data_files.append(('/usr/share/applications', ['share/Time2Pull.desktop']))
    data_files.append(('/usr/share/pixmaps', ['time2pull/forms/icons/Time2Pull.png']))


setup(
    name='Time2Pull',
    version=read_version(),
    packages=find_packages(),
    keywords=["Git; Pull; Time to pull; pull notification"],
    package_dir={'time2pull': 'time2pull'},
    data_files=data_files,
    url='https://github.com/ColinDuquesnoy/Time2Pull',
    license='GPL v3',
    author='Colin Duquesnoy',
    author_email='colin.duquesnoy@gmail.com',
    description='Get notified when your remote git repository got updated!',
    long_description=long_desc,
    zip_safe=False,
    install_requires=requirements,
    entry_points={'gui_scripts': ['Time2Pull = time2pull.app:main']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Qt',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later '
        '(GPLv3+)',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',]
)

