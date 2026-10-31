import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import sys
import unittest
from unittest.mock import patch

from PySide6 import QtWidgets
import qtpy
from maya_umbrella_launcher.launcher_view import MainUI, SettingDialog, DownloadTask, create_application
from maya_umbrella_launcher.core import UserSetting, PluginManager
from maya_umbrella_launcher.filesystem import MayaSystem


class Qt6Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication.instance() or create_application([])

    def test_widgets_and_signal_callbacks(self):
        self.assertEqual(qtpy.API_NAME, "PySide6")
        settings = {}
        errors = []
        with patch.object(UserSetting, "get", side_effect=lambda key, default=None: settings.get(key, default)), \
             patch.object(UserSetting, "set", side_effect=settings.__setitem__), \
             patch.object(MayaSystem, "get_installed_maya_versions", return_value=[]), \
             patch.object(sys, "excepthook", side_effect=lambda *args: errors.append(args)):
            window = MainUI()
            icon = self.app.windowIcon()
            self.assertFalse(icon.isNull())
            self.assertEqual({size.width() for size in icon.availableSizes()}, {16, 24, 32, 48, 64, 128, 256})
            self.assertEqual(window.windowIcon().cacheKey(), icon.cacheKey())
            children = [SettingDialog(parent=window), QtWidgets.QDialog(window),
                        QtWidgets.QMessageBox(window), QtWidgets.QFileDialog(window)]
            for child in children:
                self.assertEqual(child.windowIcon().cacheKey(), icon.cacheKey())
                child.deleteLater()
            window.show()
            self.app.processEvents()
            window.theme_bt.click()
            self.assertEqual(settings["theme"], "light")
            window.theme_bt.click()
            self.assertEqual(settings["theme"], "dark")
            dialog = SettingDialog()
            self.assertEqual(dialog.windowIcon().cacheKey(), icon.cacheKey())
            dialog.show()
            self.app.processEvents()
            dialog.proxy_ckb.click()
            self.assertTrue(dialog.proxy_line.isEnabled())
            self.assertEqual(settings["proxy_on"], "1")
            dialog.close()
            window.close()
            self.assertEqual(errors, [])

    def test_download_signal(self):
        task = DownloadTask(proxies=None)
        results = []
        task.is_success_sig.connect(results.append)
        with patch.object(PluginManager, "download_plugin", return_value=True):
            task.run()
        self.assertEqual(results, [True])


if __name__ == "__main__":
    unittest.main()
