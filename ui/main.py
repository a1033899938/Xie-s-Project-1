import sys
import os
import io
import pprint
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QWidget, QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)
from PyQt5.QtWidgets import (QLabel, QLineEdit, QTextEdit, QPushButton)
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import (QTreeView, QFileSystemModel)
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QSizePolicy
import json
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5 import (QtWidgets, QtCore, QtGui)
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QSlider
from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtCore import QRect
# for figure
import numpy as np
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
# for read file
import spe_loader as sl
from matplotlib.ticker import MaxNLocator

matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes
from PyQt5.QtWidgets import QGraphicsView, QGraphicsWidget, QGraphicsScene, QGraphicsProxyWidget
from PyQt5.QtGui import QTransform
from PyQt5.QtCore import QRectF


class MyMainWindow(QMainWindow):

    def __init__(self):
        print("MyMainWindow is instantiating...")
        super().__init__()
        """Objects"""
        self.menubar = None
        self.fileMenu = None
        self.cacheMenu = None

        # left_hbox1
        self.spectrum_file_label = None
        self.spectrum_file_textedit = None

        # left_hbox2
        self.spectra_folder_label = None
        self.spectra_folder_textedit = None

        # tree
        self.treeView = None
        self.treeManager = None

        # list
        self.listWidget = None
        self.listManager = None

        # menuActions
        self.menuActions = None

        # left_hbox3
        self.treeCollapseButton = None
        self.allItemUncheckButton = None

        # left_hbox4
        self.toggleShowTreeButton = None
        self.importCheckedFilesButton = None

        # right_hbox1
        self.histogramWidget = None
        self.roiManager = None
        self.figureWidget = None
        self.figureManager = None

        """Initialize ui"""
        self.initUI()

    def initUI(self):
        """ Set main window parameters"""
        print("Initializing UI")
        # set window position, title and so on...
        self.setGeometry(200, 200, 2400, 1200)
        self.setWindowTitle('SpectraPro')
        self.statusBar().showMessage('Ready')

        """Create menubar objects"""
        # create objects
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        self.cacheMenu = self.menubar.addMenu('&Cache')

        """Create main window objects"""
        # left_hbox1
        self.spectrum_file_label = QLabel('File path')
        self.spectrum_file_textedit = QTextEdit()
        self.spectrum_file_textedit.setReadOnly(True)  # Set to read-only for file path display
        self.spectrum_file_textedit.setFixedHeight(30)  # Set height for QTextEdit

        # left_hbox2
        self.spectra_folder_label = QLabel('File folder')
        self.spectra_folder_textedit = QTextEdit()
        self.spectra_folder_textedit.setReadOnly(True)  # Set to read-only for file path display
        self.spectra_folder_textedit.setFixedHeight(30)  # Set height for QTextEdit

        # tree
        self.treeView = TreeManager.CustomTreeView()
        self.treeView.setMinimumWidth(1000)
        self.treeManager = TreeManager(self, self.treeView)  # Manage the tree actions and slots by self.treeManager

        """Add custom actions to menu and connect to slots."""
        self.menuActions = MenuActions(self, self.treeManager)
        self.fileMenu.addAction(self.menuActions.select_spectrum_file_action())  # add a custom action instant
        self.fileMenu.addAction(self.menuActions.select_spectra_file_folder_action())
        self.cacheMenu.addAction(self.menuActions.save_cache_action())
        self.cacheMenu.addAction(self.menuActions.load_cache_action())

        # right_hbox1
        self.histogramWidget = HistogramWidget(width=8, height=2, dpi=100)
        self.roiManager = RoiManager(self.histogramWidget, width=250, height=850)
        self.figureWidget = FigureWidget(self.histogramWidget, width=12, height=8, dpi=100)
        self.figureManager = FigureManager(self.figureWidget, width=1250, height=850)

        # list
        self.listWidget = ListManager.CustomListWidget(self.figureWidget)
        self.listWidget.setMinimumWidth(1000)
        self.listManager = ListManager(self, self.listWidget, self.treeManager, self.figureWidget)

        # left_hbox3
        self.treeCollapseButton = QPushButton('Collapse All')  # add a button to collapse all nodes
        self.treeCollapseButton.clicked.connect(self.treeManager.collapse_tree)
        self.allItemUncheckButton = QPushButton('Uncheck All')  # add a button to uncheck all items
        self.allItemUncheckButton.clicked.connect(self.treeManager.uncheck_all_items)

        # left_hbox4
        self.toggleShowTreeButton = QPushButton("Show tree")  # add a button to show/hide treeview
        self.toggleShowTreeButton.setChecked(True)  # Set initial status
        self.toggleShowTreeButton.clicked.connect(self.treeManager.toggle_show_tree)
        self.importCheckedFilesButton = QPushButton("Import checked files")  # add a button to show/hide checked files
        self.importCheckedFilesButton.clicked.connect(self.listManager.import_checked_files)

        """box manager"""
        # left box
        left_hbox1 = QHBoxLayout()
        left_hbox1.addWidget(self.spectrum_file_label)
        left_hbox1.addWidget(self.spectrum_file_textedit)

        left_hbox2 = QHBoxLayout()
        left_hbox2.addWidget(self.spectra_folder_label)
        left_hbox2.addWidget(self.spectra_folder_textedit)

        left_hbox3 = QHBoxLayout()
        left_hbox3.addWidget(self.treeCollapseButton)
        left_hbox3.addWidget(self.allItemUncheckButton)

        left_hbox4 = QHBoxLayout()
        left_hbox4.addWidget(self.toggleShowTreeButton)
        left_hbox4.addWidget(self.importCheckedFilesButton)

        left_vbox = QVBoxLayout()
        left_vbox.addLayout(left_hbox1)
        left_vbox.addLayout(left_hbox2)
        left_vbox.addWidget(self.treeView)
        left_vbox.addWidget(self.listWidget)
        left_vbox.addLayout(left_hbox3)
        left_vbox.addLayout(left_hbox4)

        # right box
        right_hbox = QHBoxLayout()
        right_hbox.addWidget(self.figureManager)
        # right_hbox.addWidget(self.sliderManager)
        right_hbox.addWidget(self.roiManager)

        main_hbox = QHBoxLayout()
        main_hbox.addLayout(left_vbox)
        main_hbox.addLayout(right_hbox)

        central_widget = QWidget()
        central_widget.setLayout(main_hbox)
        self.setCentralWidget(central_widget)

        self.show()


class GeneralMethods:
    """General methods"""

    @staticmethod
    def select_spectrum_file_through_dialog():
        """Select spectrum file through a dialog, and return (1)file path"""
        print("Select spectrum file through a dialog.")
        try:
            # Open a file dialog to select a file and display the filename in the text edit.
            spectrum_file_path, _ = QFileDialog.getOpenFileName(parent=None, caption='Select spectrum file',
                                                                directory='',
                                                                filter='Spectrum file (*.txt *.spe *.h5 *.wxd)')
        except Exception as e:
            print(f"Error select_spectrum_file_through_dialog:\n  |--> {e}")
        return spectrum_file_path

    @staticmethod
    def select_spectra_file_folder_through_dialog():
        """Select spectra file folder through a dialog, and return (1)file folder path"""
        print("Select spectra file folder through a dialog.")
        try:
            spectra_file_folder_path = QFileDialog.getExistingDirectory(parent=None,
                                                                        caption='Select directory of files',
                                                                        directory='')
        except Exception as e:
            print(f"Error select_spectra_file_folder_through_dialog:\n  |--> {e}")
        return spectra_file_folder_path

    @staticmethod
    def input_dialog(parent, title='', property_name=''):
        text, okPressed = QInputDialog.getText(parent, f"{title}.", f"{property_name.title()}:", QLineEdit.Normal, "")
        return text, okPressed

    @staticmethod
    def select_json_file_through_dialog():
        json_file_path, _ = QFileDialog.getOpenFileName(parent=None, caption='Select json file', directory='cache',
                                                        filter='Json file (*.json)')
        return json_file_path

    @staticmethod
    def read_file(file_path):
        if file_path.endswith('spe'):
            sp = sl.load_from_files([file_path])
            data = {}
            data['xdim'] = sp.xdim[0]
            data['ydim'] = sp.ydim[0]
            data['intensity'] = np.squeeze(np.array(sp.data))
            data['wavelength'] = sp.wavelength
            data['strip'] = range(data['ydim'])
            print(data)
        elif file_path.endswith('txt'):
            pass
        else:
            pass
        return data

    @staticmethod
    def rotate_view(graphicsView, angle):
        # 创建一个 QTransform 对象
        transform = QTransform()

        # 在变换矩阵上应用旋转
        transform.rotate(angle)

        # 将变换应用到视图
        graphicsView.setTransform(transform)


class MenuActions:
    """Handles menu actions and their corresponding slots."""

    def __init__(self, main_window, treeManager):
        print("MenuActions is instantiating...")
        self.parent = main_window
        self.treeManager = treeManager
        self.model = self.treeManager.model

    def select_spectrum_file_action(self):
        """Create a custom action for file selection."""
        action = QAction('Select Spectrum File', self.parent)
        action.triggered.connect(self.select_spectrum_file_slot)
        return action

    def select_spectrum_file_slot(self):
        """A slot to handle: 'select_spectrum_file_action."""
        """Select spectrum file and show it's path in textedit."""
        print("#################################")
        print("You click 'select spectrum file'.")
        print("Selecting spectrum file and show it's path in textedit...")
        self.parent.spectrum_file_path = GeneralMethods.select_spectrum_file_through_dialog()
        if self.parent.spectrum_file_path:
            print(f"  |--> Select spectrum file: {self.parent.spectrum_file_path}")
            self.parent.spectrum_file_textedit.setText(self.parent.spectrum_file_path)

    def select_spectra_file_folder_action(self):
        """Create a custom action for file folder selection."""
        action = QAction('Select Spectra File Folder', self.parent)
        action.triggered.connect(self.select_spectra_file_folder_slot)
        return action

    def select_spectra_file_folder_slot(self):
        """A slot to handle: 'select_spectra_file_folder_action."""
        """Select spectra file folder and show it's path in textedit."""
        print("#################################")
        print("You click 'select spectra file folder'.")
        print("Selecting spectra file folder and show it's path in textedit.")
        try:
            self.parent.spectra_file_folder_path = GeneralMethods.select_spectra_file_folder_through_dialog()
            if self.parent.spectra_file_folder_path:
                print(f"  |--> Select spectra file folder: {self.parent.spectra_file_folder_path}")
                self.parent.spectra_folder_textedit.setText(self.parent.spectra_file_folder_path)
                self.treeManager.loadDirectory(self.parent.spectra_file_folder_path)
        except Exception as e:
            print(f"Error select_spectra_file_folder_slot:\n  |--> {e}")

    def save_cache_action(self):
        action = QAction('Save cache', self.parent)
        action.triggered.connect(self.treeManager.input_name_head_and_save_cache)
        return action

    def load_cache_action(self):
        action = QAction('Load cache', self.parent)
        action.triggered.connect(self.treeManager.select_json_file_and_load_cache)
        return action


class TreeManager:
    """Tree Actions"""

    def __init__(self, main_window, treeView):
        """Initialization"""
        print("TreeManager is instantiating...")
        self.parent = main_window
        self.treeView = treeView
        self.model = None
        self.folder_dir = QDir()
        self.fileFilters = None

        self.initTree()

    def initTree(self):
        print("Initializing tree...")
        self.model = QStandardItemModel()  # Manage the item in self.treeView through a model
        self.treeView.setModel(self.model)  # Manage the tree actions and slots
        self.treeView.setHeaderHidden(False)  # show header
        # Set custom delegate for the 1st row of tree view
        self.treeView.setItemDelegateForColumn(0, self.CustomDelegate())

    def loadDirectory(self, spectra_file_folder_path):
        """Load directory and show in tree view"""
        print("Loading directory...")
        self.spectra_file_folder_path = spectra_file_folder_path
        try:
            # initialize model
            self.model.clear()  # Clear existing items
            self.model.setHorizontalHeaderLabels(['File Name', '✔', 'Type', 'File Path'])

            # set header of the tree view
            header = self.parent.treeView.header()  # Set the first column to be resizable but with a default width
            header.setSectionResizeMode(0, QHeaderView.Interactive)  # Set the first column to be resizable
            header.resizeSection(0, 700)  # Set width of the second column to 700 pixels
            header.setSectionResizeMode(1, QHeaderView.Interactive)  # Set the second column to be resizable
            header.resizeSection(1, 10)  # Set width of the first column to 700 pixels
            header.setSectionResizeMode(2, QHeaderView.Interactive)  # Set the third column to be resizable
            header.resizeSection(2, 80)  # Set width of the third column to 700 pixels

            # add items to model
            self.addFolderItems(self.spectra_file_folder_path, self.model.invisibleRootItem())
        except Exception as e:
            print(f"  |--> Error loading directory: {e}")

    def addFolderItems(self, spectra_file_folder_path, parent_item):
        try:
            self.folder_dir.setPath(spectra_file_folder_path)
            self.fileFilters = ['*.txt', '*.spe', '*.h5', '*.wxd']  # Select the file types to show
            self.folder_dir.setNameFilters(self.fileFilters)

            # Add files with filters
            files = self.folder_dir.entryList(QDir.Files | QDir.NoDotAndDotDot)

            for file_name in files:
                item = QStandardItem(file_name)
                item.setEditable(False)

                item_check = QStandardItem()
                item_check.setCheckable(True)
                item_check.setEditable(False)

                file_path = self.folder_dir.filePath(file_name)
                item_file_path = QStandardItem(file_path)
                item_file_path.setEditable(False)

                item_type = QStandardItem('File')
                item_type.setEditable(False)
                parent_item.appendRow([item, item_check, item_type, item_file_path])

            # Add directories without filters
            dirs = QDir(spectra_file_folder_path).entryList(QDir.Dirs | QDir.NoDotAndDotDot)

            for folder_name in dirs:
                item = QStandardItem(folder_name)
                item.setEditable(False)
                item.setIcon(QIcon.fromTheme('folder'))

                item_check = QStandardItem()
                item_check.setCheckable(True)
                item_check.setEditable(False)

                file_path = self.folder_dir.filePath(folder_name)
                item_file_path = QStandardItem(file_path)
                item_file_path.setEditable(False)

                item_type = QStandardItem('Folder')
                item_type.setEditable(False)
                parent_item.appendRow([item, item_check, item_type, item_file_path])

                # Recursively add subfolders
                self.addFolderItems(self.folder_dir.filePath(folder_name), item)
            # If iterate through all elements, return to previous directory
            self.folder_dir.cdUp()
        except Exception as e:
            print(f"Error addFolderItems: {e}")

    class CustomTreeView(QTreeView):
        """Rewrite some slots for double left-clicking, right press and slot: 'check/uncheck all item'."""

        def __init__(self, parent=None):
            super().__init__(parent)

        # rewrite the mouse double click event inherit from parent
        def mouseDoubleClickEvent(self, event):
            # get index of double click position
            index = self.indexAt(event.pos())
            if not index.isValid() or event.button() == Qt.RightButton:
                return

            # get item from model
            item_index = index.siblingAtColumn(0)
            item_check_index = index.siblingAtColumn(1)
            item = self.model().itemFromIndex(item_index)
            item_check = self.model().itemFromIndex(item_check_index)
            # Toggle check state for the clicked item
            new_state_is_check = not item_check.checkState()

            if item_check is not None:
                # exchange check state
                item_check.setCheckState(Qt.Checked if new_state_is_check else Qt.Unchecked)

            # Check if item is a folder
            if item.hasChildren():
                self.toggle_check_state_for_children(item, new_state_is_check)

            # other logic of double clicking
            super().mouseDoubleClickEvent(event)

        def toggle_check_state_for_children(self, parent_item, check):
            for row in range(parent_item.rowCount()):
                child_item = parent_item.child(row, 0)
                child_item_check = parent_item.child(row, 1)
                child_item_check.setCheckState(Qt.Checked if check else Qt.Unchecked)
                if child_item.hasChildren():
                    self.toggle_check_state_for_children(child_item, check)

        def mousePressEvent(self, event):
            if event.button() == Qt.RightButton:
                index = self.indexAt(event.pos())
                if not index.isValid():
                    return

                item_index = index.siblingAtColumn(0)
                item = self.model().itemFromIndex(item_index)
                new_state_is_expand = not self.isExpanded(item_index)
                if item.hasChildren():  # 检查是否是文件夹
                    if new_state_is_expand:
                        self.expand(item_index)  # 展开这一级文件夹
                    else:
                        self.collapse(item_index)
            super().mousePressEvent(event)

    class CustomDelegate(QStyledItemDelegate):
        def paint(self, painter, option, index):
            # Call base class paint method
            super().paint(painter, option, index)

            # Get the item and its check state
            item_index = index.siblingAtColumn(0)
            item = index.model().itemFromIndex(item_index)
            item_check_index = index.siblingAtColumn(1)
            item_check = index.model().itemFromIndex(item_check_index)

            item_type_index = index.siblingAtColumn(2)
            item_type = index.model().itemFromIndex(item_type_index)
            if item_type:
                item_type = item_type.text()

            if not item_check:
                return

            if item_check.checkState() == Qt.Checked:
                # Setting item's color according to item_type
                painter.save()
                if item_type == 'File':
                    painter.fillRect(option.rect, QColor(144, 238, 144, alpha=100))  # light green
                elif item_type == 'Folder':
                    painter.fillRect(option.rect, QColor(128, 0, 128, alpha=80))  # light purple
                    # painter.fillRect(option.rect, QColor(173, 216, 230, alpha=150))  # light blue
                else:
                    painter.fillRect(option.rect, QColor(255, 0, 0, alpha=150))  # light red
                painter.restore()

    def collapse_tree(self):
        """Define a slot to collapse all nodes in the tree view."""
        print("Collapsing all nodes in the tree view...")
        self.treeView.collapseAll()

    def uncheck_all_items(self):
        """Define a slot to uncheck all items in 2nd column(item_check) in the tree view."""
        print("Unchecking all items in the tree view...")
        parent_item = self.model.invisibleRootItem()
        self.childItemUncheck(parent_item)

    def childItemUncheck(self, parent_item):
        """To uncheck all child items, grandchild items..."""
        for row in range(parent_item.rowCount()):
            child_item = parent_item.child(row, 0)
            child_item_check = parent_item.child(row, 1)
            child_item_check.setCheckState(False)
            if child_item.hasChildren():
                self.childItemUncheck(child_item)

    def toggle_show_tree(self):
        print("Toggling tree view visibility...")
        try:
            if self.treeView.isVisible():
                self.treeView.hide()
            else:
                self.treeView.show()
        except Exception as e:
            print(f"  |--> Error toggle_show_tree: {e}")

    def input_name_head_and_save_cache(self):
        try:
            ask_flag = 0
            save_flag = 0
            cache_name_head, ok = GeneralMethods.input_dialog(self.parent, title='Input name head of cache',
                                                              property_name='name head')

            if ok:
                if cache_name_head:
                    if (os.path.exists(os.path.join('cache', cache_name_head + '_tree_state.json'))
                            or os.path.exists(os.path.join('cache', cache_name_head + '_filefolder.json'))):
                        ask_flag = 1
                    else:
                        save_flag = 1
                else:
                    if (os.path.exists(os.path.join('cache', 'tree_state.json'))
                            or os.path.exists(os.path.join('cache', 'filefolder.json'))):
                        ask_flag = 1
                    else:
                        save_flag = 1

                if ask_flag:
                    reply = QMessageBox.question(self.parent, "Confirmation", 'The file is exist, continue?',
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        save_flag = 1

                if save_flag:
                    self.save_cache(cache_name_head)
            else:
                print("You cancel inputting name head.")

        except Exception as e:
            print(f'  |--> Error input name head and save cache: {e}')

    def save_cache(self, cache_name_head):
        self.save_spectra_file_folder(cache_name_head=cache_name_head)
        self.save_tree_state(cache_name_head=cache_name_head)

    def save_tree_state(self, cache_name_head=''):
        """A method to save tree items' and their check status to a json file."""
        print("Saving the tree states!")
        if cache_name_head:
            self.tree_state_name = cache_name_head + '_tree_state.json'
        else:
            self.tree_state_name = 'tree_state.json'
        # Save the root path and check states of all items
        root_item = self.model.invisibleRootItem()
        data = self.get_item_data(root_item)

        # Save data to a json file
        try:
            with open(os.path.join('cache', self.tree_state_name), 'w') as f:  # if not exist, create one
                json.dump(data, f, indent=4)
            print("  |--> Json: 'tree_state.json' has been saved.")
        except Exception as e:
            print(f'  |--> Error save_tree_state: {e}')

    def get_item_data(self, item):
        """Get all tree items' state data."""
        try:
            item_index = item.index()
            item_check_index = item_index.siblingAtColumn(1)
            item_check = item.model().itemFromIndex(item_check_index)
            item_check_data = Qt.Checked if item_check and item_check.checkState() == Qt.Checked else False

            item_type_index = item_index.siblingAtColumn(2)
            item_type = item.model().itemFromIndex(item_type_index)
            item_type = item_type.text() if item_type else ''

            item_file_path_index = item_index.siblingAtColumn(3)
            item_file_path = item.model().itemFromIndex(item_file_path_index)
            file_path = item_file_path.text() if item_file_path else ''

            data = {
                'text': item.text(),
                'checked': item_check_data,
                'type': item_type,
                'file_path': file_path,
                'children': []
            }

            for row in range(item.rowCount()):
                child_item = item.child(row, 0)
                child_item_check = item.child(row, 1)

                if child_item:
                    child_item_data = self.get_item_data(child_item)
                    data['children'].append(child_item_data)
        except Exception as e:
            print(f"Error get_item_data: {e}")
        return data

    def select_json_file_and_load_cache(self):
        try:
            json_file_path = GeneralMethods.select_json_file_through_dialog()
            json_file_name = os.path.basename(json_file_path)
            if '_tree_state.json' in json_file_name or '_filefolder.json' in json_file_name:
                if '_tree_state.json' in json_file_name:
                    cache_name_head = json_file_name.replace('_tree_state.json', '')
                else:
                    cache_name_head = json_file_name.replace('_filefolder.json', '')
                self.load_file_folder(cache_name_head + '_filefolder.json')
                self.load_tree_state(cache_name_head + '_tree_state.json')
            elif 'tree_state.json' in json_file_name or 'filefolder.json' in json_file_name:
                self.load_file_folder('filefolder.json')
                self.load_tree_state('tree_state.json')
            else:
                print("Error input json file.")
        except Exception as e:
            print(f"  |--> Error select json file and load cache: {e}")

    def load_tree_state(self, tree_state_json_file_name):
        """A method to load tree items from a json file."""
        print("Loading tree state from json...")
        self.tree_state_json_file_name = tree_state_json_file_name

        # Load data from a json file
        try:
            with open(os.path.join('cache', self.tree_state_json_file_name), 'r') as f:
                print("  |--> Opening 'tree_state.json'...")
                data = json.load(f)
                self.set_item_data(self.model.invisibleRootItem(), data)
        except FileNotFoundError:
            print("  |--> Do not found 'tree_state.json'...")

    def set_item_data(self, item, data):
        """Recursively set the item data from JSON to the tree."""
        for row in range(item.rowCount()):
            # get child item's check item
            child_item = item.child(row, 0)
            child_item_check = item.child(row, 1)
            child_item_data = data['children'][row]

            child_item_check.setCheckState(child_item_data['checked'])

            # if child_item has at least one child, repeat.
            if child_item.rowCount():
                self.set_item_data(child_item, child_item_data)

    def save_spectra_file_folder(self, cache_name_head=''):
        if cache_name_head:
            self.file_folder_json_file_name = cache_name_head + '_filefolder.json'
        else:
            self.file_folder_json_file_name = 'filefolder.json'
        print(self.parent.spectra_file_folder_path)
        try:
            data = {
                'text': self.parent.spectra_file_folder_path,
            }
            with open(os.path.join('cache', self.file_folder_json_file_name), 'w') as f:  # if not exist, create one
                json.dump(data, f, indent=4)
            print("  |--> Json: 'filefolder.json' has been saved")
        except Exception as e:
            print(f'  |--> Error saving spectra file folder: {e}')

    def load_file_folder(self, file_folder_json_file_name):
        try:
            with open(os.path.join('cache', file_folder_json_file_name), 'r') as f:
                print("  |--> Opening 'filefolder.json'...")
                data = json.load(f)
                file_folder_path = data['text']
                self.loadDirectory(file_folder_path)
                self.parent.spectra_file_folder_path = file_folder_path
        except Exception as e:
            print(f"  |--> Error loading file folder: {e}")


class ListManager:
    def __init__(self, main_window, list_widget, treeManager, figureWidget):
        """Initialization"""
        print("ListManager is instantiating...")
        self.parent = main_window
        self.listWidget = list_widget
        self.treeManager = treeManager
        self.model = self.treeManager.model
        self.figureWidget = figureWidget

        self.checked_files_data = None

    def import_checked_files(self):
        try:
            self.checked_files_data = []  # clear cache every time
            self.listWidget.clear()
            root_item = self.model.invisibleRootItem()
            get_checked_files_data = self.get_checked_files_data(root_item)
            for file_data in get_checked_files_data:
                file_name = QtWidgets.QListWidgetItem(file_data['text'])
                file_name.setData(1, file_data['file_path'])
                self.listWidget.addItem(file_name)
        except Exception as e:
            print(f"  |--> Error importing checked files: {e}")

    def get_checked_files_data(self, item):
        for row in range(item.rowCount()):
            # get child item's check item
            child_item = item.child(row, 0)
            child_item_check = item.child(row, 1)
            chile_item_type = item.child(row, 2)
            child_item_file_path = item.child(row, 3)
            if chile_item_type:
                chile_item_type = chile_item_type.text()
            if child_item_check.checkState() and chile_item_type == 'File':
                data = {
                    'text': child_item.text(),
                    'file_path': child_item_file_path.text(),
                }
                self.checked_files_data.append(data)
            if child_item.hasChildren():
                self.get_checked_files_data(child_item)
        return self.checked_files_data

    class CustomListWidget(QtWidgets.QListWidget):
        def __init__(self, figureWidget):
            super().__init__()
            # enable dragging
            self.setDragEnabled(True)
            self.setDropIndicatorShown(True)
            self.setDefaultDropAction(QtCore.Qt.MoveAction)
            self.setAcceptDrops(True)

            self.figureWidget = figureWidget

        def mouseDoubleClickEvent(self, event):
            print("You are clicking the list widget:", end=' ')
            print(self.item(0).text())

        def mousePressEvent(self, event):
            try:
                if event.button() == Qt.LeftButton:
                    index = self.indexAt(event.pos())
                    if not index.isValid():
                        return
                list_item = self.itemAt(event.pos())
                if list_item:
                    self.figureWidget.deal_with_this_file(list_item)
            except Exception as e:
                print(f"  |--> Error mousePressEvent: {e}")


class FigureManager(QGraphicsView):
    def __init__(self, figureWidget, width=400, height=300):
        super().__init__()
        self.figureWidget = figureWidget

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.figureWidget)
        proxy.setGeometry(QRectF(0, 0, self.figureWidget.width(), self.figureWidget.height()))
        self.scene.addItem(proxy)

        self.setFixedSize(1250, 850)


class FigureWidget(QWidget):
    def __init__(self, histogramWidget, width=6, height=4, dpi=100, parent=None):
        super().__init__(parent)
        self.histogramWidget = histogramWidget

        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        # self.canvas.setFixedSize(800, 600)

        self.initFig()

        self.lastx = 0  # 获取鼠标按下时的坐标X
        self.lasty = 0  # 获取鼠标按下时的坐标Y
        self.press = False

    def initFig(self):
        try:
            # self.fig.canvas.toolbar.pan()
            self.setFocusPolicy(Qt.StrongFocus)  # Enable focus to receive mouse events

            self.fig.canvas.mpl_connect('scroll_event', self.call_back)
            self.fig.canvas.mpl_connect("button_press_event", self.on_press)
            self.fig.canvas.mpl_connect("button_release_event", self.on_release)
            self.fig.canvas.mpl_connect("motion_notify_event", self.on_move)
        except Exception as e:
            print(f"  |--> Error initFig: {e}")

    def deal_with_this_file(self, list_item):
        list_item_name = list_item.data(0)
        list_item_path = list_item.data(1)
        data = GeneralMethods.read_file(list_item_path)
        self.plotfig(list_item_name, data)
        self.histogramWidget.updateHist(self.data)

    def plotfig(self, list_item_name, data):
        x = data['wavelength']
        y = data['strip']
        z = data['intensity']

        # Ensure x and y are 1D arrays and z is a 2D array
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        self.data = z

        self.ax.clear()
        self.ax.imshow(z, aspect='auto', extent=[x.min(), x.max(), y.min(), y.max()], origin='lower')
        # self.ax.pcolor(x, y, z)
        self.ax.set_title(list_item_name)
        self.canvas.draw()

    def on_press(self, event):
        if event.inaxes:  # if mouse in axes
            if event.button == 1:  # click left equals 1, while right equals 2
                self.press = True
                self.lastx = event.xdata  # get X coordinate of mouse
                self.lasty = event.ydata  # get Y coordinate of mouse

    def on_move(self, event):
        try:
            if event.inaxes and self.press:
                x = event.xdata - self.lastx
                y = event.ydata - self.lasty

                x_min, x_max = event.inaxes.get_xlim()
                y_min, y_max = event.inaxes.get_ylim()

                x_min -= x
                x_max -= x
                y_min -= y
                y_max -= y

                event.inaxes.set_xlim(x_min, x_max)
                event.inaxes.set_ylim(y_min, y_max)
                self.fig.canvas.draw_idle()  # Draw immediately
        except Exception as e:
            print(f"  |--> Error on_move: {e}")

    def on_release(self, event):
        if self.press:
            self.press = False  # 鼠标松开，结束移动

    def call_back(self, event):
        try:
            if event.inaxes:
                x_min, x_max = event.inaxes.get_xlim()
                y_min, y_max = event.inaxes.get_ylim()

                x_range = (x_max - x_min) / 10
                y_range = (y_max - y_min) / 10

                if event.button == 'up':
                    event.inaxes.set_xlim(x_min + x_range, x_max - x_range)
                    event.inaxes.set_ylim(y_min + y_range, y_max - y_range)
                elif event.button == 'down':
                    event.inaxes.set_xlim(x_min - x_range, x_max + x_range)
                    event.inaxes.set_ylim(y_min - y_range, y_max + y_range)

                self.fig.canvas.draw_idle()  # Redraw the canvas
        except Exception as e:
            print(f"  |--> Error call_back: {e}")


# class SilderManager(QSlider):
#     def __init__(self, parent):
#         super().__init__(Qt.Vertical, parent)
#         self.setRange(0, 100)
#         self.setTickPosition(QSlider.TicksBelow)
#         self.setTickInterval(1)
#
#         self.low_handle = 20
#         self.high_handle = 80
#         self.dragging = None
#         self.handle_width = 20
#         self.handle_height = 10
#
#         # Invert slider values
#         self.setInvertedAppearance(True)
#
#     def paintEvent(self, event):
#         super().paintEvent(event)
#         painter = QPainter(self)
#         rect = self.rect()
#
#         # Draw the low handle
#         low_rect = QRect(0, self.low_handle, self.handle_width, self.handle_height)
#         painter.setBrush(QColor(0, 255, 0))
#         painter.drawRect(low_rect)
#
#         # Draw the high handle
#         high_rect = QRect(0, self.high_handle, self.handle_width, self.handle_height)
#         painter.setBrush(QColor(255, 0, 255))
#         painter.drawRect(high_rect)
#
#         # # Draw the range between handles
#         # painter.setBrush(QColor(200, 200, 200))
#         # range_rect = QRect(0, (self.low_handle + self.handle_width)/2, self.handle_width*1.5,
#         #                    self.high_handle - self.low_handle - self.handle_height)
#         # painter.drawRect(range_rect)
#
#     def mousePressEvent(self, event):
#         pos = event.pos().y()
#         if self.low_handle <= pos <= self.low_handle + self.handle_height:
#             self.dragging = 'low'
#             print("low")
#         elif self.high_handle <= pos <= self.high_handle + self.handle_height:
#             self.dragging = 'high'
#             print("high")
#         else:
#             self.dragging = None
#         super().mousePressEvent(event)
#
#     def mouseMoveEvent(self, event):
#         if self.dragging:
#             pos = event.pos().y()
#             if self.dragging == 'low':
#                 self.low_handle = max(0, min(pos, self.high_handle - self.handle_height))
#                 print(pos)
#             elif self.dragging == 'high':
#                 self.high_handle = min(100, max(pos, self.low_handle + self.handle_height))
#                 print(pos)
#             self.update()
#         super().mouseMoveEvent(event)
#
#     def mouseReleaseEvent(self, event):
#         self.dragging = None
#         super().mouseReleaseEvent(event)


class RoiManager(QGraphicsView):
    def __init__(self, histogramWidget, width=400, height=300):
        super().__init__()
        self.histogramWidget = histogramWidget

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.histogramWidget)
        proxy.setGeometry(QRectF(0, 0, self.histogramWidget.width(), self.histogramWidget.height()))
        self.scene.addItem(proxy)

        self.setFixedSize(width, height)
        GeneralMethods.rotate_view(self, 270)


class HistogramWidget(QWidget):
    def __init__(self, width=6, height=4, dpi=100, parent=None):
        super().__init__(parent)
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def initHist(self):
        self.ax.tick_params(axis='both', which='major', labelsize=8)  # 设置主刻度字体大小
        self.ax.tick_params(axis='both', which='minor', labelsize=8)  # 设置次刻度字体大小
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=6))  # 设置x轴刻度的最大数量为6
        self.ax.yaxis.set_major_locator(MaxNLocator(nbins=6))  # 设置y轴刻度的最大数量为6
        self.ax.set_xlabel('Intensity', fontsize=8)
        self.ax.set_ylabel('Frequency', fontsize=8)
        self.ax.set_title(f'Histogram', fontsize=10)

    def updateHist(self, data):
        try:
            self.data = data.flatten()
            self.ax.clear()
            self.ax.hist(self.data, bins=30, color='blue', density=False)
            self.initHist()

            x_min, x_max = min(self.data), max(self.data)
            x_span = x_max - x_min
            self.ax.set_xlim(x_min - x_span * 0.1, x_max + x_span * 0.1)

            hist, _ = np.histogram(self.data, bins=30)
            y_max = max(hist) * 1.1
            self.ax.set_ylim(0, y_max)

            # self.fig.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"  |--> Error initHistogram: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    sys.exit(app.exec_())
