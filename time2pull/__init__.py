# -*- coding: utf-8 -*-
"""
Time2Pull is a small application that monitor git repositories and notify you
when the remote has changed and its time to pull.


How do we check repo status? We simply run the two following commands on each
repository and parse their output to detect the remote status::

    git remote update
    git status -uno

Icons source:
    - app icon : https://www.iconfinder.com/icons/126865/clock_loading_refresh_reload_slow_throbber_time_update_wait_waiting_icon#size=96
    - arrows: http://kyo-tux.deviantart.com/
    - database: http://www.icojoy.com
    - git: https://www.iconfinder.com/icons/83306/git_icon#size=32

"""



__version__ = '1.0.2.1'


