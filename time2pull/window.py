"""
This module contains the main window implementation.
"""
import os
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
import sys
from time2pull import __version__
from time2pull.constants import RemoteStatus, TrayIconType
from time2pull.icons import get_status_icon, get_tray_icon
from time2pull.forms.main_window_ui import Ui_MainWindow
from time2pull.settings import Settings
from time2pull.worker import WorkerThread


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self._quitting = False
        self._user_warned_about_tray = False
        # configure refresh timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(60000)
        self.setupUi(self)
        # setup worker thread
        self.worker_thread = WorkerThread()
        self.worker_thread.start()
        self.worker_thread.finished.connect(self.on_refresh_finished)
        self.worker_thread.status_available.connect(self.on_status_available)
        # load repositories
        self.listWidgetRepos.clear()
        self.listWidgetRepos.setIconSize(QtCore.QSize(64, 64))
        settings = Settings()
        for file in settings.repositories:
            item = QtWidgets.QListWidgetItem()
            item.setText(file)
            item.setIcon(get_status_icon())
            item.setData(QtCore.Qt.UserRole, (False, RemoteStatus.up_to_date))
            self.listWidgetRepos.addItem(item)
        # refresh ui
        self.pushButtonRemove.setEnabled(
            bool(len(self.listWidgetRepos.selectedItems())))
        self.pushButtonRefresh.setEnabled(bool(self.listWidgetRepos.count()))
        # run status refresh
        self.on_refresh_requested()

    def setup_tray_icon(self):
        self.tray_icon_menu = QtWidgets.QMenu(self)
        self.tray_icon_menu.addAction(self.actionRestore)
        self.tray_icon_menu.addSeparator()
        self.actionIconGroup = QtWidgets.QActionGroup(self)
        self.actionIconGroup.triggered.connect(self.on_tray_icon_style_triggered)
        for title in ['Light icon', 'Dark icon']:
            action = QtWidgets.QAction(title, self)
            action.setCheckable(True)
            self.actionIconGroup.addAction(action)
        self.actionIconGroup.actions()[int(TrayIconType.light)].setChecked(
            Settings().tray_icon_type == TrayIconType.light)
        self.actionIconGroup.actions()[int(TrayIconType.dark)].setChecked(
            Settings().tray_icon_type == TrayIconType.dark)
        mnu = QtWidgets.QMenu(self)
        mnu.setTitle('Tray icon')
        mnu.addActions(self.actionIconGroup.actions())
        self.tray_icon_menu.addMenu(mnu)
        self.tray_icon_menu.addSeparator()
        self.tray_icon_menu.addAction(self.actionHelp)
        self.tray_icon_menu.addAction(self.actionAbout)
        self.actionHelp.setShortcut(QtGui.QKeySequence.HelpContents)
        self.tray_icon_menu.addSeparator()
        self.tray_icon_menu.addAction(self.actionQuit)
        if sys.platform != 'darwin':
            self.actionQuit.setShortcut(QtGui.QKeySequence.Quit)
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(get_tray_icon(False))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.messageClicked.connect(self.on_message_clicked)
        self.tray_icon.activated.connect(self.on_icon_activated)
        self.tray_icon.show()
        self.actionQuit.triggered.connect(self.quit)

    def setup_icons(self):
        icon = QtGui.QIcon.fromTheme('add', QtGui.QIcon(':/time2pull/icons/add.png'))
        self.pushButtonAdd.setIcon(icon)
        self.actionAdd.setIcon(icon)
        icon = QtGui.QIcon.fromTheme('remove', QtGui.QIcon(':/time2pull/icons/remove.png'))
        self.pushButtonRemove.setIcon(icon)
        self.actionRemove.setIcon(icon)
        icon = QtGui.QIcon.fromTheme('view-refresh', QtGui.QIcon(':/time2pull/icons/view-refresh.png'))
        self.pushButtonRefresh.setIcon(icon)
        self.actionRefresh.setIcon(icon)
        icon = QtGui.QIcon.fromTheme('help', QtGui.QIcon(':/time2pull/icons/help.png'))
        self.actionHelp.setIcon(icon)
        icon = QtGui.QIcon.fromTheme('info', QtGui.QIcon(':/time2pull/icons/info.png'))
        self.actionAbout.setIcon(icon)
        icon = QtGui.QIcon.fromTheme('exit', QtGui.QIcon(':/time2pull/icons/exit.png'))
        self.actionQuit.setIcon(icon)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        # setup icons, try to use theme if possible
        self.setup_icons()
        # window properties
        icon = QtGui.QIcon(':/time2pull/icons/git-light.png')
        self.setWindowIcon(icon)
        self.setWindowTitle("Time2Pull")
        # refresh label movie
        self.movie = QtGui.QMovie(':/time2pull/icons/loader.gif')
        self.labelRefresh.setMovie(self.movie)
        # Tray icon
        self.setup_tray_icon()
        # connect slots to signals
        self.timer.timeout.connect(self.on_refresh_requested)
        self.pushButtonRefresh.clicked.connect(self.on_refresh_requested)
        self.listWidgetRepos.itemSelectionChanged.connect(
            self.on_selection_changed)
        self.actionRestore.triggered.connect(self.restore)

    def closeEvent(self, event):
        if not self._quitting:
            if not self._user_warned_about_tray:
                QtWidgets.QMessageBox.information(
                    self, "Time2Pull",
                    "The program will keep running in the system tray.\n"
                    "To terminate the program, choose Quit in the context menu"
                    " of the system tray entry.")
                self._user_warned_about_tray = True
            self.hide()
            event.ignore()

    def _get_repositories_to_refresh(self):
        return Settings().repositories

    @QtCore.pyqtSlot()
    def on_refresh_requested(self):
        repos = self._get_repositories_to_refresh()
        if repos:
            self.timer.stop()
            self.pushButtonRefresh.setEnabled(False)
            self.pushButtonAdd.setEnabled(False)
            self.pushButtonRemove.setEnabled(False)
            self.listWidgetRepos.setEnabled(False)
            self.labelRefresh.setVisible(True)
            self.movie.start()
            self.worker_thread.set_repositories_to_refresh(repos)
            self.worker_thread.wake_up()

    def update_tray_icon(self):
        is_behind = False
        for i in range(self.listWidgetRepos.count()):
            item = self.listWidgetRepos.item(i)
            _, remote_status = item.data(QtCore.Qt.UserRole)
            if remote_status == RemoteStatus.behind:
                is_behind = True
                break
        self.tray_icon.setIcon(get_tray_icon(is_behind))

    @QtCore.pyqtSlot()
    def on_refresh_finished(self):
        self.timer.start()
        self.pushButtonRefresh.setEnabled(bool(self.listWidgetRepos.count()))
        self.pushButtonAdd.setEnabled(True)
        self.pushButtonRemove.setEnabled(
            bool(len(self.listWidgetRepos.selectedItems())))
        self.listWidgetRepos.setEnabled(True)
        self.labelRefresh.setVisible(False)
        self.movie.stop()
        self.update_tray_icon()

    @QtCore.pyqtSlot()
    def on_pushButtonAdd_clicked(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select a repository')
        settings = Settings()
        if path and path not in settings.repositories:
            if os.path.exists(os.path.join(path, '.git')):
                repos = settings.repositories
                repos.append(path)
                settings.repositories = repos
                item = QtWidgets.QListWidgetItem()
                item.setText(path)
                item.setIcon(get_status_icon())
                item.setData(QtCore.Qt.UserRole, (False, RemoteStatus.up_to_date))
                self.listWidgetRepos.addItem(item)
                self.on_refresh_requested()
            else:
                QtWidgets.QMessageBox.warning(
                    self, 'Not a git repository',
                    'The chosen directory is not a git repository')

    @QtCore.pyqtSlot()
    def on_pushButtonRemove_clicked(self):
        repo = self.listWidgetRepos.currentItem().text()
        self.listWidgetRepos.takeItem(self.listWidgetRepos.currentRow())
        settings = Settings()
        repos = settings.repositories
        try:
            repos.remove(repo)
        except ValueError:
            pass
        settings.repositories = repos

    @QtCore.pyqtSlot()
    def on_selection_changed(self):
        self.pushButtonRemove.setEnabled(
            bool(len(self.listWidgetRepos.selectedItems())))

    def alert(self, repo):
        repo_name = QtCore.QFileInfo(repo).fileName()
        self.tray_icon.showMessage(
            repo_name,
            "Remote repository has been updated. It's time to pull!")
        QtMultimedia.QSound.play(':/time2pull/sounds/sonar.wav')

    @QtCore.pyqtSlot(str, bool, object)
    def on_status_available(self, repo, dirty, remote_status):
        for i in range(self.listWidgetRepos.count()):
            item = self.listWidgetRepos.item(i)
            if item.text() == repo:
                item.setIcon(get_status_icon(dirty, remote_status))
                old_dirty_flg, old_remote_status = item.data(
                    QtCore.Qt.UserRole)
                item.setData(QtCore.Qt.UserRole, (dirty, remote_status))
                if(remote_status == RemoteStatus.behind and
                        old_remote_status != RemoteStatus.behind):
                    self.alert(repo)
        self.update_tray_icon()

    def restore(self):
        self.show()
        QtWidgets.QApplication.instance().setActiveWindow(self)

    @QtCore.pyqtSlot(object)
    def on_icon_activated(self, reason):
        if sys.platform == 'darwin':
            reasons = []
        else:
            reasons = (QtWidgets.QSystemTrayIcon.Trigger,
                       QtWidgets.QSystemTrayIcon.DoubleClick)
        if reason in reasons:
            self.restore()
        elif reason == QtWidgets.QSystemTrayIcon.MiddleClick:
            self.showMessage()

    @QtCore.pyqtSlot()
    def on_message_clicked(self):
        self.restore()

    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        QtWidgets.QMessageBox.about(
            self, 'About Time2Pull',
            'Time2Pull is small application that monitors your local git '
            'repositories and warns you when a remote got updated.'
            '\n'
            '\n'
            'Time2Pull is a free open source software licensed under the GPL '
            'v3. The application is written in Python using the PyQt5 GUI '
            'toolkit.'
            '\n'
            '\n'
            'Author: Colin Duquesnoy\n'
            'Version: %s' % __version__)

    def on_tray_icon_style_triggered(self, action):
        ltext = action.text().lower()
        settings = Settings()
        settings.tray_icon_type = (
            TrayIconType.dark if 'dark' in ltext else TrayIconType.light)
        self.update_tray_icon()

    def quit(self):
        self._quitting = True
        QtWidgets.QApplication.instance().quit()
