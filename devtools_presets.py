from PyQt5 import QtWidgets, QtCore
import json


class PresetsWidget(QtWidgets.QGroupBox):
	def __init__(self, title, apply_cb, fetch_cb, path, preset_renderer=None):
		if not path:
			return
		super().__init__(title)
		self.path = path
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

	def load(self, silent=False):
		loaded_presets = self.load_presets()
		if not loaded_presets:
			return
		loaded_preset = None

		if silent:
			if len(loaded_presets):
				loaded_preset = loaded_presets[0]
		else:
			load_dlg = PresetsLoadDialog(loaded_presets, self.preset_renderer)
			load_dlg.exec()
			loaded_preset = load_dlg.getLoadedPreset()
			finish_presets = load_dlg.getFinishPresets()
			self.save_presets(finish_presets)

		if loaded_preset:
			self.apply_cb(loaded_preset)

	def save(self):
		new_preset = dict()
		preset_name = QtWidgets.QInputDialog.getText(self, "Name for new preset", "Enter name:", QtWidgets.QLineEdit.Normal)
		if preset_name[1]:
			new_preset['name'] = preset_name[0]
			new_preset['preset'] = self.fetch_cb()
			loaded_presets = self.load_presets()
			if loaded_presets == None:
				return
			loaded_presets.append(new_preset)
			self.save_presets(loaded_presets)

	def load_presets(self):
		presets = None
		with open(self.path, 'r') as presets_file:
			presets = json.load(presets_file)
		return presets

	def save_presets(self, updated_presets):
		with open(self.path, 'w') as presets_file:
			json.dump(updated_presets, presets_file, indent=4)



class PresetsLoadDialog(QtWidgets.QDialog):
	def __init__(self, presets, preset_renderer):
		super().__init__()
		self.loaded_preset = None
		self.presets_model = PresetsCollection(presets, preset_renderer)

		self.presets_view = QtWidgets.QTableView()
		self.presets_view.setFocusPolicy(QtCore.Qt.NoFocus)
		self.presets_view.horizontalHeader().hide()
		self.presets_view.verticalHeader().hide()
		self.presets_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.presets_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
		self.presets_view.setModel(self.presets_model)

		self.buttonBox = QtWidgets.QDialogButtonBox()
		self.delete_btn = QtWidgets.QPushButton('Delete')
		self.delete_btn.clicked.connect(self.deletePreset)
		self.delete_btn.setEnabled(False)
		self.load_btn = QtWidgets.QPushButton('Load')
		self.load_btn.clicked.connect(self.loadPreset)
		self.load_btn.setEnabled(False)
		self.buttonBox.addButton(QtWidgets.QDialogButtonBox.Cancel)
		self.buttonBox.addButton(self.delete_btn, QtWidgets.QDialogButtonBox.ActionRole)
		self.buttonBox.addButton(self.load_btn, QtWidgets.QDialogButtonBox.AcceptRole)
		self.presets_view.selectionModel().currentRowChanged.connect(self.presetSelected)

		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)

		self.dialog_lo = QtWidgets.QVBoxLayout()
		self.dialog_lo.addWidget(self.presets_view)
		self.dialog_lo.addWidget(self.buttonBox)


		# play around table view display settings
		# self.presets_view.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		# self.presets_view.resizeColumnsToContents()
		# self.presets_view.adjustSize()
		# self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
		# print(self.sizePolicy().horizontalPolicy())

		self.setLayout(self.dialog_lo)

	def deletePreset(self):
		selected = self.presets_view.selectionModel().selectedRows()
		if selected:
			self.presets_model.removeRows(selected[0].row(), 1, None)

	def loadPreset(self):
		selected = self.presets_view.selectionModel().selectedRows()
		if selected:
			self.loaded_preset = self.presets_model.data(selected[0], QtCore.Qt.UserRole)

	def getFinishPresets(self):
		return self.presets_model.presets

	def getLoadedPreset(self):
		return self.loaded_preset

	def presetSelected(self):
		self.load_btn.setEnabled(True)
		self.delete_btn.setEnabled(True)


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
				if self.renderer:
					return self.renderer(self.presets[index.row()]['preset'])

		if role == QtCore.Qt.UserRole:
			return self.presets[index.row()]

	def removeRows(self, position, count, parent):
		self.beginRemoveRows(QtCore.QModelIndex(), position, position)
		del self.presets[position]
		self.endRemoveRows()
