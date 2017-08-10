from PyQt5 import QtWidgets
import wialon_sdk_client

class RequestsPage(QtWidgets.QWidget):
	def __init__(self, wialon_client):
		super().__init__()
		self.wialon_client = wialon_client

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