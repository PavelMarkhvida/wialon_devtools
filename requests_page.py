from PyQt5 import QtWidgets, QtGui
import wialon_sdk_client
import devtools_helper
import jsontotable
import json

class RequestsPage(QtWidgets.QWidget):
	def __init__(self, wialon_client):
		super().__init__()
		self.wc = wialon_client
		self.request_params = {"spec":{"itemsType":"avl_unit","propName":"*","propValueMask":"*","sortType":""},"force":1,"flags":1,"from":0,"to":0}

		self.target = QtWidgets.QLineEdit('core')
		self.command = QtWidgets.QLineEdit('search_items')
		self.exec_btn = QtWidgets.QPushButton('Execute')
		self.exec_btn.clicked.connect(self.execute)

		self.response_table = QtWidgets.QTableView()
		self.clipboard = QtWidgets.QApplication.clipboard()

		self.params_layout = QtWidgets.QVBoxLayout()
		self.paste_btn = QtWidgets.QPushButton('Paste')
		self.paste_btn.clicked.connect(self.paste_params)

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
		command_layout.addWidget(self.response_table)

		left_layout.addLayout(command_layout)

		right_layout = QtWidgets.QVBoxLayout()
		right_layout.addWidget(QtWidgets.QLabel('<b>Service parameters</b>'))
		right_layout.addLayout(self.params_layout)
		right_layout.addWidget(self.paste_btn)
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
			self.status_label.showMessage('Response received')
			tm = jsontotable.TablesManager(self.response_table, response)
			tm.render()
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


	def paste_params(self):
		clipped = self.clipboard.text()
		self.request_params = json.loads(clipped)
		self.updatePage()

