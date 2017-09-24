from PyQt5 import QtNetwork, QtCore

class WialonIPSClient(QtCore.QObject):
	def __init__(self, logger_callback):
		super().__init__()
		self.log = logger_callback
		self.ip = '193.193.165.165'
		self.port = 20332
		self.socket = QtNetwork.QTcpSocket()
		self.socket.readyRead.connect(self.read_wialon_answer)
		self.socket.connected.connect(self.handle_connected)
		self.socket.disconnected.connect(self.handle_disconnected)
		self.socket.error.connect(self.handle_error)

	connected = QtCore.pyqtSignal()
	disconnected = QtCore.pyqtSignal()
	data_received = QtCore.pyqtSignal(str)
	error_occured = QtCore.pyqtSignal()


	def set_ip(self, ip):
		self.ip = ip

	def set_port(self, ip):
		self.port = port

	def connect(self):
		if not self.ip or not self.port:
			self.log('Specify host to connect')
			return
		if self.socket.state() != QtNetwork.QAbstractSocket.UnconnectedState:
			self.log('Socket is connected already')
			return
		self.socket.connectToHost(self.ip, self.port)
		self.log('Connecting...')

	def disconnect(self):
		self.socket.disconnectFromHost()

	def abort(self):
		self.socket.abort()

	def login(self, object_id, password):
		if self.socket.isValid():
			if not object_id:
				self.log('Bad object ID')
				return
			object_password = password
			if not object_password:
				object_password = 'NA'
			message = '#L#{};{}\r\n'.format(object_id, object_password)
			self.log(message)
			self.socket.write(message.encode())
		else:
			self.log('Failed to login. Socket state is {}'.format(self.socket.state()))

	def send_short_msg(self, lat, lon, speed, height, course):
		if self.socket.isValid():
			if not object_id:
				return (False, 'Bad object ID')
			object_password = password
			if object_password is None:
				object_password = 'NA'
			self.socket.write('#L#{};{}'.format(id, object_password))
		else:
			self.log('Failed to send message. Socket state is {}'.format(self.socket.state()))
	
	def handle_connected(self):
		log_msg = 'Connected to {}:{}'.format(self.socket.peerAddress().toString(), self.socket.peerPort())
		self.log(log_msg)
		self.connected.emit()

	def handle_disconnected(self):
		log_msg = 'Disconnected from {}:{}'.format(self.socket.peerAddress().toString(), self.socket.peerPort())
		self.log(log_msg)
		self.disconnected.emit()

	def read_wialon_answer(self):
		if self.socket.bytesAvailable():
			answer = self.socket.readAll().data().decode()
			print(answer)
			self.log(answer)

	def handle_error(self):
		self.log(self.socket.errorString())
		self.error_occured.emit()
