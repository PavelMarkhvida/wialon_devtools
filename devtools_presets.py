from PyQt5 import QtWidgets, QtCore

presets = list()
presets.append({'name': 'Wialon Devtools', 'preset': {'host': 'hst-api.wialon.com', 'port': 443, 'secure': True, 'user': 'shse_test', 'password': '123'}})
presets.append({'name': 'Wialon Local', 'preset': {'host': '127.0.0.1', 'port': 8021, 'secure': False, 'user': 'wialon'}})

class PresetsWidget(QtWidgets.QGroupBox):
	def __init__(self, title, apply_cb, fetch_cb, preset_renderer=None):
		super().__init__(title)
		self.preset_renderer = preset_renderer
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
		loaded_presets = self.load_presets()
		load_dlg = PresetsLoadDialog(loaded_presets, self.preset_renderer)
		load_dlg.exec()
		loaded_preset = load_dlg.getLoadedPreset()
		finish_presets = load_dlg.getFinishPresets()
		self.save_presets(finish_presets)
		self.apply_cb(loaded_preset)


	def save(self):
		new_preset = dict()
		preset_name = QtWidgets.QInputDialog.getText(self, "Name for new preset", "Enter name:", QLineEdit.Normal)
		new_preset['name'] = preset_name
		new_preset['preset'] = self.fetch_cb()
		loaded_presets = self.load_presets()
		loaded_presets.append(new_preset)
		self.save_presets(loaded_presets)


	def load_presets(self):
		# load from disk
		global presets
		return presets


	def save_presets(self, updated_presets):
		# store to disk
		global presets
		presets = updated_presets


class PresetsLoadDialog(QtWidgets.QDialog):
	def __init__(self, presets, preset_renderer):
		super().__init__()
		self.loaded_preset = None
		self.presets_model = PresetsCollection(presets, preset_renderer)

		self.presets_view = QtWidgets.QTableView()
		self.presets_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.presets_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
		self.presets_view.setModel(self.presets_model)

		self.buttonBox = QtWidgets.QDialogButtonBox()
		delete_btn = QtWidgets.QPushButton('Delete')
		delete_btn.clicked.connect(self.deletePreset)
		load_btn = QtWidgets.QPushButton('Load')
		load_btn.clicked.connect(self.loadPreset)
		self.buttonBox.addButton(delete_btn, QtWidgets.QDialogButtonBox.ActionRole)
		self.buttonBox.addButton(load_btn, QtWidgets.QDialogButtonBox.AcceptRole)

		self.dialog_lo = QtWidgets.QVBoxLayout()
		self.dialog_lo.addWidget(self.presets_view)
		self.dialog_lo.addWidget(self.buttonBox)
		self.setLayout(self.dialog_lo)

	def deletePreset(self):
		selected = self.presets_view.selectionModel().selectedRows()
		if selected:
			self.presets_model.removeRows(selected[0].row(), 1, None)

	def loadPreset(self):
		selected = self.presets_view.selectionModel().selectedRows()
		if selected:
			self.loaded_preset = self.presets_model.data(selected[0], QtCore.Qt.UserRole)
			self.accept()

	def getFinishPresets(self):
		return self.presets_model.presets

	def getLoadedPreset(self):
		return self.loaded_preset


# Model for presets view (used in load dialog)
class PresetsCollection(QtCore.QAbstractTableModel):
	def __init__(self, presets, preset_renderer):
		super().__init__()
		self.presets = presets
		self.renderer = preset_renderer

	def rowCount(self, index):
		return len(self.presets)

	def columnCount(self, index):
		return 2

	def data(self, index, role):
		if role == QtCore.Qt.DisplayRole:
			if index.column() == 0:
				return self.presets[index.row()]['name']
			if index.column() == 1:
				return self.renderer(self.presets[index.row()]['preset'])

		if role == QtCore.Qt.UserRole:
			return self.presets[index.row()]

	def removeRows(self, position, count, parent):
		self.beginRemoveRows(QtCore.QModelIndex(), position, position)
		del self.presets[position]
		self.endRemoveRows()