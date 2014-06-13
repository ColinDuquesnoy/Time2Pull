# -*- coding: utf-8 -*-
"""
This module contains the worker thread implementation.
"""
import locale
from PyQt5 import QtCore
from time2pull.constants import RemoteStatus


class WorkerThread(QtCore.QThread):
    #: Signal emitted when the refresh operation completed
    finished = QtCore.pyqtSignal()

    #: Signal emitted when a status for a repository is available.
    #: Parameters:
    #:      - path: repository path
    #:      - dirty: True if the repo has uncommited changed
    #:      - remote_status: constans.RepoStatus
    status_available = QtCore.pyqtSignal(str, bool, object)

    def __init__(self):
        super().__init__()
        # list of files to parse
        self._repositories = []
        self._sleep = True
        self._mutex = QtCore.QMutex()

    def set_repositories_to_refresh(self, repositories):
        _ = QtCore.QMutexLocker(self._mutex)
        self._repositories = repositories

    def get_repositories(self):
        _ = QtCore.QMutexLocker(self._mutex)
        return list(self._repositories)

    def wake_up(self, wake_up=True):
        """
        Wake up the thread and performs a status refresh for all repositories
        in the repositories list.
        """
        _ = QtCore.QMutexLocker(self._mutex)
        self._sleep = not wake_up

    def is_sleeping(self):
        """
        Checks if the thread is sleeping (waiting for wake up/refresh requests)
        :return:
        """
        _ = QtCore.QMutexLocker(self._mutex)
        return self._sleep

    def run(self):
        while True:
            if self.is_sleeping():
                self.sleep(1)
            else:
                self._refresh_all_status()

    def _refresh_all_status(self):
        repositories = self.get_repositories()
        for repo in repositories:
            self._refresh_repo(repo)
        self._sleep = True
        self.finished.emit()

    def _refresh_repo(self, repo):
        # git remote update
        process = QtCore.QProcess()
        process.setWorkingDirectory(repo)
        process.start('git', ['remote', 'update'])
        process.waitForFinished()

        # git
        process = QtCore.QProcess()
        process.setWorkingDirectory(repo)
        process.start('git', ['status', '-uno'])
        process.waitForFinished()
        output = process.readAllStandardOutput().data().decode(
            locale.getpreferredencoding())
        # print(output)
        if 'behind' in output:
            status = RemoteStatus.behind
        elif 'ahead' in output:
            status = RemoteStatus.ahead
        elif 'diverged' in output:
            status = RemoteStatus.diverged
        else:
            status = RemoteStatus.up_to_date
        dirty = ('Changes not staged' in output or
                 'Changes to be committed' in output)
        self.status_available.emit(repo, dirty, status)
