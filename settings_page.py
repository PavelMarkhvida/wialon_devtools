from PyQt5 import QtWidgets
import wialon_sdk_client
import devtools_preset


class SettingsPage(QtWidgets.QWidget):
	def __init__(self, wialon_client):
		super().__init__()
		self.wc = wialon_client

		# Connection widgets
		self.host_le = QtWidgets.QLineEdit()
		self.port_le = QtWidgets.QLineEdit()
		self.sid_le = QtWidgets.QLineEdit()
		self.secure_chx = QtWidgets.QCheckBox()

		# Credentials widgets
		self.user_le = QtWidgets.QLineEdit()
		self.password_le = QtWidgets.QLineEdit()
		self.password_le.setEchoMode(QtWidgets.QLineEdit.Password)
		self.login_btn = QtWidgets.QPushButton('Login')
		self.login_cancel_btn = QtWidgets.QPushButton('Cancel')
		self.login_cancel_btn.setEnabled(False)

		self.status_lbl = QtWidgets.QStatusBar()
		self.initPage()

	def initPage(self):
		# bind widgets to wialon_sdk_client
		self.host_le.textChanged.connect(self.wc.set_host)
		self.port_le.textChanged.connect(self.wc.set_port)
		self.sid_le.textChanged.connect(self.wc.set_sid)
		self.secure_chx.stateChanged.connect(self.wc.set_secure)
		self.login_btn.clicked.connect(self.try_login)
		self.login_cancel_btn.clicked.connect(self.cancel_login)

		# draw layout
		page_lo = QtWidgets.QVBoxLayout()
		
		settings_gr = QtWidgets.QGroupBox('Settings')
		settings_lo = QtWidgets.QHBoxLayout()

		host_settings_lo = QtWidgets.QFormLayout()
		host_settings_lo.addRow('Host', self.host_le)
		host_settings_lo.addRow('Port', self.port_le)
		host_settings_lo.addRow('SID', self.sid_le)
		host_settings_lo.addRow('Secure', self.secure_chx)

		credentials_lo = QtWidgets.QFormLayout()
		credentials_lo.addRow('User', self.user_le)
		credentials_lo.addRow('Password', self.password_le)
		login_btn_lo = QtWidgets.QHBoxLayout()
		login_btn_lo.addStretch(1)
		login_btn_lo.addWidget(self.login_btn)
		login_btn_lo.addWidget(self.login_cancel_btn)
		credentials_lo.addRow(login_btn_lo)

		settings_lo.addLayout(host_settings_lo)
		settings_lo.addLayout(credentials_lo)
		settings_lo.setStretch(0, 4)
		settings_lo.setStretch(1, 3)
		settings_lo.addStretch(3)

		settings_gr.setLayout(settings_lo)

		page_lo.addWidget(settings_gr)
		presets_widget = devtools_preset.PresetsWidget({
				"name": "Settings presets",
				"path": "presets/settings.preset",
				"widgets": [
					{
						"name": "host",
						"widget": self.host_le
					},
					{
						"name": "port",
						"widget": self.port_le
					},
					{
						"name": "secure",
						"widget": self.secure_chx
					},
					{
						"name": "user",
						"widget": self.user_le
					},
					{
						"name": "password",
						"widget": self.password_le
					}
				]
			})
		page_lo.addWidget(presets_widget)
		page_lo.addStretch(1)
		page_lo.addWidget(self.status_lbl)

		self.setLayout(page_lo)
		# init widgets with wialon_sdk_client state
		self.updatePage()

	def updatePage(self):
		self.host_le.setText(self.wc.get_host())
		self.port_le.setText(str(self.wc.get_port()))
		self.sid_le.setText(self.wc.get_sid())
		self.secure_chx.setChecked(self.wc.is_secure())

	# Login routines

	def try_login(self):
		# Login button clicked - disable some widgets and try to login with sdk client
		self.login_btn.setEnabled(False)
		self.login_cancel_btn.setEnabled(True)
		self.sid_le.setEnabled(False)
		self.status_lbl.showMessage('Trying to login')
		user = self.user_le.text()
		password = self.password_le.text()
		self.login_rt = self.wc.login(user, password, self.finish_login)

	def cancel_login(self):
		self.login_rt.cancel()

	def finish_login(self, error, status):
		# callback called after login attempt
		self.status_lbl.showMessage(status)
		self.updatePage()
		self.sid_le.setEnabled(True)
		self.login_btn.setEnabled(True)
		self.login_cancel_btn.setEnabled(False)
