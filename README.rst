Time2Pull (Git repository monitor)
==================================

Time2Pull is small application that monitor your git repositories and warn you when the remote changed. This
is particularly useful if you're working with a centralised workflow where all developpers pull from a central repository.


Monitoring, how do we do?
=========================

Every minutes, the application will execute the two following git commands to detect remote status changes on every
repositories you've added::

  $ git remote update
  $ git status -uno
  

License
=======

Time2Pull is an open source application licensed under the GPL v3.


Requirements
============

Time2Pull uses the following softwares:

  - git
  - python 3
  - PyQt5


Installation
=============

Windows
-------

Use the windows installer available in the release section.


Mac OSX
-------

Use the dmg installer available in the release section


GNU/Linux
---------

There is no binary packages for linux yet, and I won't make them myself but I am open to help packagers who would like to package the application.

You will need to install from source (or from pypi).

*Note: the directives are given for a debian based distribution, adapts the commands to suit your distribution.*

1) install dependencies using your distribution's pacakge manager::

    sudo apt-get install python3-pyqt5 git
  
2) install the package from source or from pypi (a desktop entry will be created so that the app appears in your menu)::

    sudo pip3 install Time2Pull
    

   or (from source)::
   

    sudo pip3 install .
  







