
.. image:: https://raw.githubusercontent.com/ColinDuquesnoy/Time2Pull/develop/time2pull/forms/icons/Time2Pull_banner.png

Time2Pull is small application that monitors your local git repositories and
warns you when a remote got updated, i.e. *it's time to pull!*

This is particularly useful if you're working with a centralised workflow
(where all developers pull and push from a central repository) and want to
be quickly notified anytime the remote got updated.


How does it work?
=================

First, you add the paths to the local repositories you would like to monitor.

Then, the application will scan the added repositories every minutes to detect remote status changes.

The scan simply consists in calling the two following git commands and parsing their output::

  $ git remote update
  $ git status -uno
  
If the repository is behind its origin, the application will warn you by displaying a message in the system 
tray and by playing an alert sound.


Features
========

- cross platform: run on Windows, Mac OSX and GNU/Linux
- free and open source, built upon FOSS technologies (Python, Qt, Git)
- detects pullable commits and warns you!
- detects pushable commits (just for information)
- detects uncommitted changes (just for information)
- nice and explicit icon overlays for each state
- you can choose between a dark and a white tray icon for a better integration with your desktop

Screenshots
===========

Main Window:

.. image:: https://raw.githubusercontent.com/ColinDuquesnoy/Time2Pull/develop/doc/_static/Time2Pull.png
    :align: center

Overlays and their meanings:


.. image:: https://raw.githubusercontent.com/ColinDuquesnoy/Time2Pull/develop/doc/_static/Time2PullOverlays.png
    :align: center

License
=======

Time2Pull is a free open source application licensed under the GPL v3.


Requirements
============

Time2Pull uses the following softwares:

- Git
- Python 3 (>= 3.4)
- PyQt5


Installation
============

Windows
-------

Use the windows installer available in the release section.


Mac OSX
-------

Use the dmg installer available in the release section


GNU/Linux
---------

There is no binary packages for linux yet. *I won't make them myself but I am ready to help packagers who would like to volunteer, if any.*

You will need to install from source (or from pypi).

*Note: the directives are given for a debian based distribution, you should adapt the commands to suit your distribution.*

1) install dependencies using your distribution's package manager::

    sudo apt-get install python3-pyqt5 git qt5-multimedia


2) install the package, using pip for python3::

    sudo pip3 install Time2Pull


3) run the software from your application menu or from the command line::

    Time2Pull


Known issues
============

- Tray icon does not show on Gnome 3:

  This seems to be a PyQt5 bug. You will need the top icons shell extension to
  view the tray icon.


Credits
=======

- application icon: Céline Thiry <thiry.celi@gmail.com>
- arrow down & up icons: http://kyo-tux.deviantart.com/
- disk icon: http://www.icojoy.com
- tango icon theme: http://tango.freedesktop.org/


Changelog
=========

1.0.2
-----
Fixed bugs
    - fix pip installation due to missing files in source distribution.

1.0.1
-----

Fixed bugs:
    - fix version number in python package.

1.0.0
-----

First public release.
