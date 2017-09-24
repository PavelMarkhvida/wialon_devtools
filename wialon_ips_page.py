from PyQt5 import QtWidgets
import wialon_ips_client
import datetime


class WialonIPSPage(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

		self.wc_connected = False

		self.ip_le = QtWidgets.QLineEdit('193.193.165.165')
		self.port_le = QtWidgets.QLineEdit('20332')
		self.obj_id_le = QtWidgets.QLineEdit()
		self.obj_id_le.textChanged.connect(self.obj_id_le_handler)
		self.obj_password_le = QtWidgets.QLineEdit()
		
		self.connect_btn = QtWidgets.QPushButton('Connect')
		self.connect_btn.clicked.connect(self.connectToWialonIPSServer)
		self.login_btn = QtWidgets.QPushButton('Login')
		self.login_btn.setEnabled(True if self.obj_id_le.text() else False)
		self.login_btn.clicked.connect(self.loginToWialonIPSServer)
		self.disconnect_btn = QtWidgets.QPushButton('Disconnect')
		# self.disconnect_btn.setEnabled(False)
		self.disconnect_btn.clicked.connect(self.disconnectFromWialonIPSServer)

		self.lat_le = QtWidgets.QLineEdit()
		self.lon_le = QtWidgets.QLineEdit()
		self.speed_le = QtWidgets.QLineEdit()
		self.course_le = QtWidgets.QLineEdit()
		self.height_le = QtWidgets.QLineEdit()

		self.send_btn = QtWidgets.QPushButton('Send')
		self.send_btn.clicked.connect(self.sendMessage)

		self.log_te = QtWidgets.QTextEdit()
		self.log_te.setReadOnly(True)

		self.status_lbl = QtWidgets.QStatusBar()

		self.wc = wialon_ips_client.WialonIPSClient(self.logger)
		self.wc.connected.connect(self.handle_connected)
		self.wc.disconnected.connect(self.handle_disconnected)
		self.wc.error_occured.connect(self.handle_error)

		self.ip_le.textChanged.connect(self.wc.set_ip)
		self.port_le.textChanged.connect(self.wc.set_port)

		self.initPage()

	def initPage(self):
		page_lo = QtWidgets.QVBoxLayout()

		connection_gr = QtWidgets.QGroupBox('Connection')
		connection_lo = QtWidgets.QHBoxLayout()

		left_lo = QtWidgets.QVBoxLayout()

		host_lo = QtWidgets.QFormLayout()
		host_lo.addRow('IP', self.ip_le)
		host_lo.addRow('Port', self.port_le)

		connection_btn_lo = QtWidgets.QHBoxLayout()
		connection_btn_lo.addWidget(self.connect_btn)
		connection_btn_lo.addWidget(self.disconnect_btn)

		left_lo.addLayout(host_lo)
		left_lo.addLayout(connection_btn_lo)

		right_lo = QtWidgets.QVBoxLayout()

		obj_credentials_lo = QtWidgets.QFormLayout()
		obj_credentials_lo.addRow('Object ID', self.obj_id_le)
		obj_credentials_lo.addRow('Object password', self.obj_password_le)

		login_btn_lo = QtWidgets.QHBoxLayout()
		login_btn_lo.addStretch(1)
		login_btn_lo.addWidget(self.login_btn)

		right_lo.addLayout(obj_credentials_lo)
		right_lo.addLayout(login_btn_lo)
		
		connection_lo.addLayout(left_lo)
		connection_lo.addLayout(right_lo)
		connection_lo.setStretch(0, 2)
		connection_lo.setStretch(1, 5)
		connection_gr.setLayout(connection_lo)

		msg_gr = QtWidgets.QGroupBox('Message')
		msgs_lo = QtWidgets.QHBoxLayout()
		short_msg_lo = QtWidgets.QFormLayout()
		short_msg_lo.addRow('Lat', self.lat_le)
		short_msg_lo.addRow('Lon', self.lon_le)
		short_msg_lo.addRow('Speed', self.speed_le)
		short_msg_lo.addRow('Height', self.height_le)
		short_msg_lo.addRow('Course', self.course_le)
		msgs_lo.addLayout(short_msg_lo)
		msgs_lo.addStretch(1)
		msg_gr.setLayout(msgs_lo)

		log_gr = QtWidgets.QGroupBox('Log')
		log_lo = QtWidgets.QVBoxLayout()
		log_lo.addWidget(self.log_te)
		log_gr.setLayout(log_lo)

		page_lo.addWidget(connection_gr)
		page_lo.addWidget(msg_gr)
		page_lo.addWidget(log_gr)
		page_lo.addStretch(1)
		page_lo.addWidget(self.status_lbl)

		self.setLayout(page_lo)

	def connectToWialonIPSServer(self):
		self.connect_btn.setEnabled(False)
		connect_res = self.wc.connect()

	def disconnectFromWialonIPSServer(self):
		self.wc.disconnect()

	def handle_connected(self):
		self.wc_connected = True
		self.obj_id_le_handler()

	def handle_disconnected(self):
		self.wc_connected = False
		self.connect_btn.setEnabled(True)
		self.obj_id_le_handler()

	def handle_error(self):
		self.wc_connected = False
		self.connect_btn.setEnabled(True)

	def loginToWialonIPSServer(self):
		object_id = self.obj_id_le.text()
		object_password = self.obj_password_le.text()
		self.wc.login(object_id, object_password)

	def logger(self, msg):
		current_time = datetime.datetime.now().strftime("<i>[%H:%M:%S.%f]</i> ... ")
		msg_to_print = msg

		if msg[-2:] == '\r\n':
			msg_to_print = msg[:-2]
		elif msg[-1:] == '\n':
			msg_to_print = msg[:-1]
		self.log_te.append(current_time + msg)

	def sendMessage(self):
		pass

	def obj_id_le_handler(self):
		if self.wc_connected and self.obj_id_le.text():
			self.login_btn.setEnabled(True)
		else:
			self.login_btn.setEnabled(False)
