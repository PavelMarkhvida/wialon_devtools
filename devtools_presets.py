from PyQt5 import QtWidgets

class PresetsWidget(QtWidgets.QGroupBox):
	def __init__(self, title, apply_cb, fetch_cb):
		super().__init__(title)
		self.apply_cb = apply_cb
		self.fetch_cb = fetch_cb

		self.save_btn = QtWidgets.QPushButton('Save')
		self.save_btn.clicked.connect(self.save)

		self.load_btn = QtWidgets.QPushButton('Load')
		self.load_btn.clicked.connect(self.load)

		self.initWidget()


	def initWidget(self):
		lo = QtWidgets.QHBoxLayout()
		lo.addWidget(self.load_btn)
		lo.addWidget(self.save_btn)
		lo.addStretch(1)
		self.setLayout(lo)

	def load(self):
		loaded = self.load_all()
		load_dialog = PresetsLoadDialog(loaded)
		load_dialog.exec()
		preset = load_dialog.get_preset()
		self.apply_cb(preset)

	def save(self):
		new_preset = self.fetch_cb()
		new_preset_name = QInputDialog.getText(self, "Name for new preset", "Enter name:", QLineEdit.Normal)
		new_preset[name] = new_preset_name


class PresetsLoadDialog(QtWidgets.QDialog):
	def __init__(self, presets):
		pass