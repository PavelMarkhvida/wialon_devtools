#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Wialon Devtools
"""

import sys
import wialon_sdk_client
import settings_page
import requests_page
from PyQt5 import QtWidgets, QtGui


class DevtoolsWidget(QtWidgets.QTabWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle('Wialon Devtools')
		self.setWindowIcon(QtGui.QIcon('images/wialon.png'))
		self.setGeometry(300, 300, 650, 450)

		wialon_client = wialon_sdk_client.WialonSDKClient()
		self.addTab(settings_page.SettingsPage(wialon_client), "Settings")
		self.addTab(requests_page.RequestsPage(wialon_client), "SDK")

		self.show()


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	devtools_widget = DevtoolsWidget()
	sys.exit(app.exec_())
