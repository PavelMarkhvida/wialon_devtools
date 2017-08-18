from PyQt5 import QtWidgets
import wialon_sdk_client
import devtools_helper

class RequestsPage(QtWidgets.QWidget):
	def __init__(self, wialon_client):
		super().__init__()
		self.wc = wialon_client
		self.request_params = {}

		self.target = QtWidgets.QLineEdit()
		self.command = QtWidgets.QLineEdit()
		self.exec_btn = QtWidgets.QPushButton('Execute')
		self.exec_btn.clicked.connect(self.execute)

		self.params_layout = QtWidgets.QVBoxLayout()

		self.status_label = QtWidgets.QStatusBar()
		self.initPage()


	def initPage(self):
		page_layout = QtWidgets.QVBoxLayout()
		main_layout = QtWidgets.QHBoxLayout()

		left_layout = QtWidgets.QVBoxLayout()

		command_layout = QtWidgets.QVBoxLayout()
		command_layout.addWidget(QtWidgets.QLabel('<b>SDK command</b>'))

		target = QtWidgets.QVBoxLayout()
		target.addWidget(QtWidgets.QLabel("Target"))
		target.addWidget(self.target)

		command = QtWidgets.QVBoxLayout()
		command.addWidget(QtWidgets.QLabel("Command"))
		command.addWidget(self.command)

		sdk_command_layout = QtWidgets.QHBoxLayout()
		sdk_command_layout.addLayout(target)
		sdk_command_layout.addLayout(command)

		command_layout.addLayout(sdk_command_layout)
		command_layout.addWidget(self.exec_btn)
		command_layout.addStretch(1)

		left_layout.addLayout(command_layout)

		right_layout = QtWidgets.QVBoxLayout()
		right_layout.addWidget(QtWidgets.QLabel('<b>Service parameters</b>'))
		right_layout.addLayout(self.params_layout)
		right_layout.addStretch(1)
		
		main_layout.addLayout(left_layout)
		main_layout.addLayout(right_layout)

		page_layout.addLayout(main_layout)
		page_layout.addStretch(1)
		page_layout.addWidget(self.status_label)

		self.setLayout(page_layout)
		self.updatePage()


	def execute(self):
		target = self.target.text()
		if not target:
			self.status_label.showMessage('Target is invalid')
			return
		command = self.command.text()
		if not command:
			self.status_label.showMessage('Command is invalid')
			return
		self.status_label.showMessage('Making request...')
		svc = target + '/' + command
		self.exec_btn.setEnabled(False)
		self.wc.execute_request(svc, self.request_params, self.handle_execute)


	def handle_execute(self, error, response):
		if not error:
			self.status_label.showMessage(str(response))
		else:
			self.status_label.showMessage(str(response))

		self.exec_btn.setEnabled(True)


	def updatePage(self):
		if self.params_layout.itemAt(0):
			self.params_layout.itemAt(0).widget().setParent(None)

		params_widget = QtWidgets.QWidget()
		rendered_params = QtWidgets.QVBoxLayout()
		devtools_helper.render(rendered_params, self.request_params, self.updatePage)
		params_widget.setLayout(rendered_params)

		self.params_layout.addWidget(params_widget)


# def getRequestParamsWidget():
# 	req_widget = QWidget()
# 	requests_layout = QVBoxLayout()
# 	requests_layout.addWidget(QLabel('<b>Service parameters</b>'))
# 	devtools_helper.render(requests_layout, request_params, update_main_widget)
# 	requests_layout.addStretch(1)
# 	req_widget.setLayout(requests_layout)
# 	return req_widget


# def getSDKCommandWidget():
# 	sdk_cmd_widget = QWidget()

# 	command_layout = QVBoxLayout()
# 	command_layout.addWidget(QLabel('<b>SDK command</b>'))
	
# 	target = QVBoxLayout()
# 	target.addWidget(QLabel("Target"))
# 	target.addWidget(QLineEdit())

# 	command = QVBoxLayout()
# 	command.addWidget(QLabel("Command"))
# 	command.addWidget(QLineEdit())

# 	sdk_command_layout = QHBoxLayout()
# 	sdk_command_layout.addLayout(target)
# 	sdk_command_layout.addLayout(command)

# 	command_layout.addLayout(sdk_command_layout)
# 	pb = QPushButton('Send')
# 	pb.clicked.connect(send_request)
# 	command_layout.addWidget(pb)
# 	command_layout.addStretch(1)

# 	sdk_cmd_widget.setLayout(command_layout)
# 	return sdk_cmd_widget