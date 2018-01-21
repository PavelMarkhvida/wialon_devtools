from PyQt5 import QtWidgets
import wialon_sdk_client
import settings_page
import requests_page

class RemoteAPIPage(QtWidgets.QTabWidget):
	def __init__(self):
		super().__init__()
		self.wialon_client = wialon_sdk_client.WialonSDKClient()

		self.initPage()

	def initPage(self):
		self.addTab(settings_page.SettingsPage(self.wialon_client), "Settings")
		self.addTab(requests_page.RequestsPage(self.wialon_client), "Requests")
