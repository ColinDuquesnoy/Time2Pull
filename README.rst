Time2Pull (Git repository monitor)
==================================

Time2Pull is small application that monitor your local git repositories and warn you when the remote changed (e.g. one of your colleague just pushed to the repository).

This is particularly useful if you're working with a centralised workflow where all developpers pull and push from a central repository.


How does it work?
=================

First you add the paths to the local repositories you would like to monitor.

Then, every minutes, the application will execute the two following git commands to detect remote status changes on every
repositories you've added::

  $ git remote update
  $ git status -uno
  
If one the repository is behind remote/origin, the application will warn you by displaying a message in the system tray
and by playing an alert sound. 

The application also display the repository status (uncommitted changes, pushable commits,...) as an icon.

See the screeshots:

  

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

*Note: the directives are given for a debian based distribution, you should adapt the commands to suit your distribution.*

1) install dependencies using your distribution's pacakge manager::

    sudo apt-get install python3-pyqt5 git
  
2) install the package from source or from pypi (a desktop entry will be created so that the app appears in your menu)::

    sudo pip3 install Time2Pull
    

   or (from source)::
   

    sudo pip3 install .
  
  
Known issues
-------------

1) Tray icon does not show on gnome shell:

 Yes, this is a PyQt5 bug. You will need the top icons shell extension to view the tray icon.







