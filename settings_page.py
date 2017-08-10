from PyQt5 import QtCore, QtWidgets
import wialon_sdk_client

class SettingsPage(QtWidgets.QWidget):
	def __init__(self, wialon_client):
		super().__init__()
		self.wc = wialon_client

		self.hst = QtWidgets.QLineEdit()
		self.port = QtWidgets.QLineEdit()
		self.sid = QtWidgets.QLineEdit()

		self.login = QtWidgets.QLineEdit()

		self.password = QtWidgets.QLineEdit()
		self.password.setEchoMode(QtWidgets.QLineEdit.Password)

		self.login_btn = QtWidgets.QPushButton('Login')
		self.login_btn.clicked.connect(self.try_login)

		self.secure = QtWidgets.QCheckBox()
		self.secure.stateChanged.connect(self.change_secure)

		self.status_label = QtWidgets.QStatusBar()
		self.initPage()

	def initPage(self):
		page_layout = QtWidgets.QVBoxLayout()
		settings_layout = QtWidgets.QHBoxLayout()

		self.hst.textChanged.connect(self.wc.set_ip)
		self.port.textChanged.connect(self.wc.set_port)
		self.sid.textChanged.connect(self.wc.set_sid)
		self.login.textChanged.connect(self.wc.set_login)
		self.password.textChanged.connect(self.wc.set_password)

		host_settings_layout = QtWidgets.QFormLayout()
		host_settings_layout.addRow('Host', self.hst)
		host_settings_layout.addRow('Port', self.port)
		host_settings_layout.addRow('SID', self.sid)
		host_settings_layout.addRow('Secure', self.secure)

		credentials_layout = QtWidgets.QFormLayout()
		credentials_layout.addRow('Login', self.login)
		credentials_layout.addRow('Password', self.password)
		credentials_layout.addRow(self.login_btn)


		settings_layout.addLayout(host_settings_layout)
		settings_layout.addLayout(credentials_layout)

		page_layout.addLayout(settings_layout)
		page_layout.addStretch(1)
		page_layout.addWidget(self.status_label)

		self.setLayout(page_layout)
		self.updatePage()

	def change_secure(self, secure):
		self.wc.set_secure(secure)
		self.updatePage()

	def try_login(self):
		self.login_btn.setEnabled(False)
		self.sid.setEnabled(False)
		self.status_label.showMessage('Trying to login')
		login_result = self.wc.do_login(self.handle_login)

	def handle_login(self, error, status):
		self.status_label.showMessage(status)
		self.updatePage()
		self.sid.setEnabled(True)
		self.login_btn.setEnabled(True)


	def updatePage(self):
		self.hst.setText(self.wc.get_ip())
		self.port.setText(str(self.wc.get_port()))
		self.login.setText(self.wc.get_login())
		self.password.setText(self.wc.get_password())
		self.sid.setText(self.wc.get_sid())
		self.secure.setChecked(self.wc.is_secure())
