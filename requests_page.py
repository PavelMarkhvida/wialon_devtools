from PyQt5 import QtWidgets
import json
import wialon_sdk_client
import devtools_params
import devtools_presets
import devtools_jstable


class RequestsPage(QtWidgets.QWidget):
	def __init__(self, wialon_client):
		super().__init__()
		self.wc = wialon_client
		self.clipboard = QtWidgets.QApplication.clipboard()
		self.request_params = {"spec":{"itemsType":"avl_unit","propName":"*","propValueMask":"*","sortType":""},"force":1,"flags":1,"from":0,"to":0}

		self.target = QtWidgets.QLineEdit('core')
		self.command = QtWidgets.QLineEdit('search_items')
		self.send_btn = QtWidgets.QPushButton('Send')
		self.cancel_btn = QtWidgets.QPushButton('Cancel')
		self.cancel_btn.setEnabled(False)

		self.params_layout = QtWidgets.QVBoxLayout()

		self.copy_btn = QtWidgets.QPushButton('Copy')
		self.paste_btn = QtWidgets.QPushButton('Paste')

		self.response_table = QtWidgets.QTableView()

		self.status_lbl = QtWidgets.QStatusBar()
		self.initPage()

	def initPage(self):
		self.send_btn.clicked.connect(self.executeRequest)
		self.cancel_btn.clicked.connect(self.cancelRequest)
		self.copy_btn.clicked.connect(self.copyParamsToBuffer)
		self.paste_btn.clicked.connect(self.pasteParamsFromBuffer)

		page_lo = QtWidgets.QVBoxLayout()
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
		right_title_lo.addWidget(self.cancel_btn)
		right_lo.addLayout(right_title_lo)
		right_lo.addLayout(self.params_layout)
		
		main_layout.addLayout(left_lo)
		main_layout.addLayout(right_lo)
		main_layout.setStretch(1, 2)

		page_lo.addLayout(main_layout)
		presets_widget = devtools_presets.PresetsWidget('Request presets', self.apply, self.fetch, 'presets/requests.preset', self.render_preset)
		page_lo.addWidget(presets_widget)
		page_lo.addWidget(self.status_lbl)

		self.setLayout(page_lo)
		self.updateParamsWidget()

	def executeRequest(self):
		target = self.target.text()
		if not target:
			self.status_lbl.showMessage('Target is invalid')
			return
		command = self.command.text()
		if not command:
			self.status_lbl.showMessage('Command is invalid')
			return
		self.status_lbl.showMessage('Making request...')
		svc = target + '/' + command
		self.send_btn.setEnabled(False)
		self.cancel_btn.setEnabled(True)
		self.request_rt = self.wc.execute_request(svc, self.request_params, self.handleExecute)

	def cancelRequest(self):
		self.request_rt.cancel()

	def handleExecute(self, error, response):
		if not error:
			self.status_lbl.showMessage('Response received')
			self.updateResponseWidget(response)
		else:
			self.status_lbl.showMessage(str(response))

		self.send_btn.setEnabled(True)
		self.cancel_btn.setEnabled(False)

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

	def updateResponseWidget(self, response_data):
		devtools_jstable.render(self.response_table, response_data)

	def pasteParamsFromBuffer(self):
		clipped = self.clipboard.text()
		self.request_params = json.loads(clipped)
		self.updateParamsWidget()

	def copyParamsToBuffer(self):
		self.clipboard.setText(json.dumps(self.request_params, indent=4))

	# Methods for presets widget

	def apply(self, preset_to_apply):
		self.target.setText('')
		self.command.setText('')
		self.request_params = {}
		self.updateResponseWidget({})

		if not preset_to_apply or 'preset' not in preset_to_apply:
			self.status_lbl.showMessage('Failed to load preset')
			self.updateParamsWidget()
			return
		if 'target' in preset_to_apply['preset']:
			self.target.setText(preset_to_apply['preset']['target'])
		if 'command' in preset_to_apply['preset']:
			self.command.setText(preset_to_apply['preset']['command'])
		if 'request_params' in preset_to_apply['preset']:
			self.request_params = json.loads(preset_to_apply['preset']['request_params'])

		self.updateParamsWidget()
		self.status_lbl.showMessage('Loaded preset {}'.format(preset_to_apply['name']))

	def fetch(self):
		new_preset = {}
		target = self.target.text()
		if target:
			new_preset['target'] = target
		command = self.command.text()
		if command:
			new_preset['command'] = command
		
		new_preset['request_params'] = json.dumps(self.request_params)

		return new_preset

	def render_preset(self, preset):
		target = None
		command = None
		
		if 'target' in preset:
			target = preset['target']
		if 'command' in preset:
			command = preset['command']
		
		return '{}/{}'.format(target, command)


