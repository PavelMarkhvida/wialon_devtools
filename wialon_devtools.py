#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Wialon Devtools
"""

import sys
import wialon_sdk_client
import settings_page
import requests_page
import wialon_ips_page
from PyQt5 import QtWidgets, QtGui


class DevtoolsWidget(QtWidgets.QTabWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle('Wialon Devtools')
		self.setWindowIcon(QtGui.QIcon('images/wialon.png'))
		self.setGeometry(300, 300, 800, 620)

		remote_api_tabs = QtWidgets.QTabWidget()
		wialon_client = wialon_sdk_client.WialonSDKClient()
		remote_api_tabs.addTab(settings_page.SettingsPage(wialon_client), "Settings")
		remote_api_tabs.addTab(requests_page.RequestsPage(wialon_client), "Requests")

		self.addTab(remote_api_tabs, 'Remote API')
		self.addTab(wialon_ips_page.WialonIPSPage(), "Wialon IPS")

		self.show()


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	devtools_widget = DevtoolsWidget()
	sys.exit(app.exec_())
