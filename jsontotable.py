from PyQt5 import QtWidgets, QtCore
import sys

class TablesManager():
	def __init__(self, table_view, data):
		table_view.setFocusPolicy(QtCore.Qt.NoFocus)
		table_view.horizontalHeader().hide()
		table_view.verticalHeader().hide()
		if type(data) is list or type(data) is dict:
			self.data = data
		else:
			self.data = {}
		self.table_view = table_view

	def render(self):
		self.show_table([])

	def show_table(self, path):
		target = self.data
		
		nested = False
		if len(path):
			nested = True

		for e in path:
			target = target[e]

		new_model = TableModel(target, nested)
		self.table_view.setModel(new_model)
		self.table_view.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

		# apply navigation widgets to view

		if nested:
			# first row is 'Up' button
			new_path = list(path)
			del new_path[-1]
			cur_index = new_model.index(0, 1)
			ctrl_widget = NavigationButton('..', self, new_path)
			self.table_view.setIndexWidget(cur_index, ctrl_widget)

		# element is key in case if target is dict
		# element is index in case if target is list
		target_is_list = (type(target) is list)

		# apply widgets for navigation to child objects
		target_index = 0
		for child in target:

			# in case if we render list we must access it's childs by index
			if target_is_list:
				child = target_index

			child_is_object = type(target[child]) is list or type(target[child]) is dict

			if child_is_object:
				model_row = target_index
				if nested:
					model_row = target_index + 1

				cur_index = new_model.index(model_row, 1)
				new_path = list(path)
				new_path.append(child)

				ctrl_widget = NavigationButton(str(len(target[child])), self, new_path)
				self.table_view.setIndexWidget(cur_index, ctrl_widget)

			target_index = target_index + 1


class TableModel(QtCore.QAbstractTableModel):
	def __init__(self, data, has_parent):
		super().__init__()
		self.table_data = data
		self.has_parent = has_parent

	def rowCount(self, index):
		if self.has_parent:
			return len(self.table_data) + 1
		else:
			return len(self.table_data)

	def columnCount(self, index):
		return 2

	def flags(self, index):
		flags = QtCore.Qt.ItemIsEnabled
		return flags

	def data(self, index, role):
		row = index.row()
		get_key = (index.column() == 0)

		if role == QtCore.Qt.DisplayRole:
			if self.has_parent and row == 0:
				return '..'

			if self.has_parent:
				row = row - 1

			requested_key = None

			if type(self.table_data) is list:
				requested_key = row
			elif type(self.table_data) is dict:
				requested_key = list(self.table_data.keys())[row]

			if get_key:
				return requested_key
			else:
				elem_type = type(self.table_data[requested_key])
				if elem_type is not dict and elem_type is not list:
					return self.table_data[requested_key]
				else:
					return 'obj place'


class NavigationButton(QtWidgets.QPushButton):
	def __init__(self, label, tables_manager, path):
		super().__init__(label)
		self.tables_manager = tables_manager
		self.path = path

	def mousePressEvent(self, event):
		self.tables_manager.show_table(self.path)


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	test_widget = QtWidgets.QWidget()
	l = QtWidgets.QHBoxLayout()

	tv = QtWidgets.QTableView()
	tv.setFocusPolicy(QtCore.Qt.NoFocus)
	tv.horizontalHeader().hide()
	tv.verticalHeader().hide()
	# data = {'k1': 5, 'k2': 'shse', 'k3': {'kd1': '4'}, 'k4': ['one', 'two', {'deep': 'inside'}]}
	# data = {'svc_error': 6}
	data = {"glossary":{"title":"exampleglossary","GlossDiv":{"title":"S","GlossList":{"GlossEntry":{"ID":"SGML","SortAs":"SGML","GlossTerm":"StandardGeneralizedMarkupLanguage","Acronym":"SGML","Abbrev":"ISO8879:1986","GlossDef":{"para":"Ameta-markuplanguage,usedtocreatemarkuplanguagessuchasDocBook.","GlossSeeAlso":["GML","XML"]},"GlossSee":"markup"}}}}}
	# data = None
	# data = [5, 'sss', 6]
	# data = 3
	tm = TablesManager(tv, data)
	tm.render()
	l.addWidget(tv)


	test_widget.setLayout(l)
	test_widget.show()
	sys.exit(app.exec_())
