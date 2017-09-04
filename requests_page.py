from PyQt5 import QtWidgets
import json
import wialon_sdk_client
import devtools_params
import devtools_jstable


class RequestsPage(QtWidgets.QWidget):
	def __init__(self, wialon_client):
		super().__init__()
		self.wc = wialon_client
		self.request_params = {"spec":{"itemsType":"avl_unit","propName":"*","propValueMask":"*","sortType":""},"force":1,"flags":1,"from":0,"to":0}

		self.target = QtWidgets.QLineEdit('core')
		self.command = QtWidgets.QLineEdit('search_items')
		self.send_btn = QtWidgets.QPushButton('Send')
		self.send_btn.clicked.connect(self.executeRequest)

		self.response_table = QtWidgets.QTableView()

		self.clipboard = QtWidgets.QApplication.clipboard()

		self.params_layout = QtWidgets.QVBoxLayout()
		self.paste_btn = QtWidgets.QPushButton('Paste')
		self.paste_btn.clicked.connect(self.pasteParamsFromBuffer)

		self.copy_btn = QtWidgets.QPushButton('Copy')
		self.copy_btn.clicked.connect(self.copyParamsToBuffer)

		self.status_label = QtWidgets.QStatusBar()
		self.initPage()

	def initPage(self):
		page_layout = QtWidgets.QVBoxLayout()
		main_layout = QtWidgets.QHBoxLayout()

		left_lo = QtWidgets.QVBoxLayout()

		command_lo = QtWidgets.QVBoxLayout()
		command_lo.addWidget(QtWidgets.QLabel('<b>Service</b>'))

		target = QtWidgets.QVBoxLayout()
		target.addWidget(QtWidgets.QLabel("Target"))
		target.addWidget(self.target)

		command = QtWidgets.QVBoxLayout()
		command.addWidget(QtWidgets.QLabel("Command"))
		command.addWidget(self.command)

		sdk_command_lo = QtWidgets.QHBoxLayout()
		sdk_command_lo.addLayout(target)
		sdk_command_lo.addLayout(command)

		command_lo.addLayout(sdk_command_lo)
		command_lo.addWidget(QtWidgets.QLabel('<b>Response</b>'))
		command_lo.addWidget(self.response_table)

		left_lo.addLayout(command_lo)

		right_lo = QtWidgets.QVBoxLayout()
		right_title_lo = QtWidgets.QHBoxLayout()
		right_title_lo.addWidget(QtWidgets.QLabel('<b>Service parameters</b>'))
		right_title_lo.addWidget(self.copy_btn)
		right_title_lo.addWidget(self.paste_btn)
		right_title_lo.addStretch(1)
		right_title_lo.addWidget(self.send_btn)
		right_lo.addLayout(right_title_lo)
		right_lo.addLayout(self.params_layout)
		
		main_layout.addLayout(left_lo)
		main_layout.addLayout(right_lo)
		main_layout.setStretch(0, 1)
		main_layout.setStretch(1, 2)

		page_layout.addLayout(main_layout)
		page_layout.addWidget(self.status_label)

		self.setLayout(page_layout)
		self.updateParamsWidget()

	def executeRequest(self):
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
		self.send_btn.setEnabled(False)
		self.wc.execute_request(svc, self.request_params, self.handleExecute)

	def handleExecute(self, error, response):
		if not error:
			self.status_label.showMessage('Response received')
			devtools_jstable.render(self.response_table, response)
		else:
			self.status_label.showMessage(str(response))

		self.send_btn.setEnabled(True)

	def updateParamsWidget(self):
		# delete old params widget
		if self.params_layout.itemAt(0):
			self.params_layout.itemAt(0).widget().setParent(None)

		# render new params widget
		params_scrl_area = QtWidgets.QScrollArea()
		params_scrl_area.setStyleSheet("background-color: #e7fcca; opacity: 0.5");
		params_widget = QtWidgets.QWidget()
		rendered_params = QtWidgets.QVBoxLayout()
		devtools_params.render(rendered_params, self.request_params, self.updateParamsWidget)
		params_widget.setLayout(rendered_params)
		params_scrl_area.setWidget(params_widget)

		self.params_layout.addWidget(params_scrl_area)

	def pasteParamsFromBuffer(self):
		clipped = self.clipboard.text()
		self.request_params = json.loads(clipped)
		self.updateParamsWidget()

	def copyParamsToBuffer(self):
		self.clipboard.setText(json.dumps(self.request_params, indent=4))

