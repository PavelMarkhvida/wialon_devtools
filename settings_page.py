from PyQt5 import QtCore, QtWidgets
import wialon_sdk_client
import devtools_presets

class SettingsPage(QtWidgets.QWidget):
	def __init__(self, wialon_client):
		super().__init__()
		self.wc = wialon_client

		self.host_le = QtWidgets.QLineEdit()
		self.port_le = QtWidgets.QLineEdit()
		self.sid_le = QtWidgets.QLineEdit()

		self.user_le = QtWidgets.QLineEdit()
		self.password_le = QtWidgets.QLineEdit()
		self.password_le.setEchoMode(QtWidgets.QLineEdit.Password)
		self.login_btn = QtWidgets.QPushButton('Login')

		self.secure_chx = QtWidgets.QCheckBox()

		self.status_lbl = QtWidgets.QStatusBar()
		self.initPage()

	def initPage(self):
		self.host_le.textChanged.connect(self.wc.set_host)
		self.port_le.textChanged.connect(self.wc.set_port)
		self.sid_le.textChanged.connect(self.wc.set_sid)
		self.secure_chx.stateChanged.connect(self.wc.set_secure)
		self.login_btn.clicked.connect(self.try_login)

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
		credentials_lo.addRow(login_btn_lo)


		settings_lo.addLayout(host_settings_lo)
		settings_lo.addLayout(credentials_lo)

		settings_gr.setLayout(settings_lo)

		page_lo.addWidget(settings_gr)
		page_lo.addWidget(devtools_presets.PresetsWidget('Settings presets', self.apply, self.fetch, self.render_preset))
		page_lo.addStretch(1)
		page_lo.addWidget(self.status_lbl)

		self.setLayout(page_lo)
		self.updatePage()


	def try_login(self):
		self.login_btn.setEnabled(False)
		self.sid_le.setEnabled(False)
		self.status_lbl.showMessage('Trying to login')
		user = self.user_le.text()
		password = self.password_le.text()
		login_result = self.wc.login(user, password, self.handle_login)

	def handle_login(self, error, status):
		self.status_lbl.showMessage(status)
		self.updatePage()
		self.sid_le.setEnabled(True)
		self.login_btn.setEnabled(True)


	def updatePage(self):
		self.host_le.setText(self.wc.get_host())
		self.port_le.setText(str(self.wc.get_port()))
		self.sid_le.setText(self.wc.get_sid())
		self.secure_chx.setChecked(self.wc.is_secure())


	def apply(self, settings):
		if not settings or 'preset' not in settings:
			self.status_lbl.showMessage('Failed to load preset')
			return
		if 'host' in settings['preset']:
			print('Apply host')
			self.host_le.setText(settings['preset']['host'])
		if 'port' in settings['preset']:
			self.port_le.setText(str(settings['preset']['port']))
		if 'user' in settings['preset']:
			self.user_le.setText(settings['preset']['user'])
		if 'password' in settings['preset']:
			self.password_le.setText(settings['preset']['password'])
		if 'secure' in settings['preset']:
			self.secure_chx.setChecked(settings['preset']['secure'])
		self.status_lbl.showMessage('Loaded preset {}'.format(settings['name']))


	def fetch(self):
		settings = {}
		host = self.host_le.text()
		if host:
			settings['host'] = host
		port = self.port_le.text()
		if port:
			settings['port'] = port
		user = self.user_le.text()
		if user:
			settings['user'] = user
		password = self.password_le.text()
		if password:
			settings['password'] = password
		settings['secure'] = self.secure_chx.checkState()

		return settings

	def render_preset(self, preset):
		host = preset['host']
		port = preset['port']
		secure = preset['secure']
		user = preset['user']
		return 'host:{}, port:{}, secure:{}\n user:{}'.format(host, port, secure, user)

