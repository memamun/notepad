import subprocess
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar, QTextEdit, QFileDialog, QTabWidget, QMenu, QFontDialog, QPushButton, QVBoxLayout, QWidget, QTabBar
from PyQt6.QtCore import QFileInfo, QSettings, Qt
import sys


class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()



        # Create a QTabWidget to manage multiple tabs
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # Create initial tab and add it to the tab widget
        self.add_tab()
        # Create a bottom status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)


        self.tab_widget.currentChanged.connect(self.update_status_bar)
        self.tab_widget.currentWidget().selectionChanged.connect(self.update_status_bar)

        # Load font settings from configuration file
        self.settings = QSettings("MyCompany", "NotepadApp")
        saved_font = self.settings.value("font")
        if saved_font:
            self.default_font = QFont(saved_font)
        else:
            self.default_font = QFont("Monospace", 10)
            self.default_font.setWeight(QFont.Weight.Light)

        # Set the default font for the current text edit widget
        self.tab_widget.currentWidget().setFont(self.default_font)

        # Set up the main window properties
        self.setWindowTitle("Notepad")
        self.setGeometry(100, 100, 800, 600)

        # Create actions, menus, and connect them
        self.create_actions()
        self.create_menus()

        # Set the tab bar behavior to close tabs on middle-click
        self.tab_widget.tabBar().setTabsClosable(True)
        self.tab_widget.tabBar().tabCloseRequested.connect(self.close_tab)

        # Create a container widget to hold the tab bar and the "+" button
        tab_container = QWidget()
        tab_layout = QVBoxLayout(tab_container)
        tab_layout.addWidget(self.tab_widget)

        # Set the container widget as the central widget
        self.setCentralWidget(tab_container)


    def create_actions(self):
        # New Instance Action
        self.new_instance_action = QAction("New Instance", self)
        self.new_instance_action.setShortcut("Ctrl+N")
        self.new_instance_action.triggered.connect(self.open_new_instance)


        # # New Action
        # self.new_action = QAction("New", self)
        # self.new_action.triggered.connect(self.new_document)

        # Open Action
        self.open_action = QAction("Open", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_document)

        # Inside the create_actions method:

        # New Tab Action
        self.new_tab_action = QAction("New Tab", self)
        self.new_tab_action.setShortcut("Ctrl+T")
        self.new_tab_action.triggered.connect(self.add_tab)

        # Close Tab Action
        self.close_tab_action = QAction("Close Tab", self)
        self.close_tab_action.setShortcut("Ctrl+W")
        self.close_tab_action.triggered.connect(self.close_current_tab)

        # Save Action
        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_document)


        # Save As Action
        self.save_as_action = QAction("Save As", self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.save_as_action.triggered.connect(self.save_document_as)

        # Exit Action
        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Alt+F4")
        self.exit_action.triggered.connect(self.close)

        # Settings Action
        self.settings_action = QAction("Settings", self)
        self.settings_action.triggered.connect(self.show_settings)

    def create_menus(self):
        # Create a File menu
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.new_instance_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)


        tab_menu = self.menuBar().addMenu("Tab")
        tab_menu.addAction(self.new_tab_action)
        tab_menu.addAction(self.close_tab_action)


        # Create a Settings menu
        settings_menu = self.menuBar().addMenu("Settings")
        settings_menu.addAction(self.settings_action)

    def add_tab(self):
        # Create a new QTextEdit for each tab
        text_edit = QTextEdit(self)

        # Connect the signals to update the status bar
        text_edit.selectionChanged.connect(self.update_status_bar)
        text_edit.textChanged.connect(self.update_status_bar)

        # Add the new tab to the tab widget
        self.tab_widget.addTab(text_edit, "Untitled")

    # Add the method to handle the new instance action
    def open_new_instance(self):
        subprocess.Popen(["python", __file__])

    def open_document(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")

        if file_name:
            with open(file_name, "r") as file:
                content = file.read()

            text_edit = self.tab_widget.currentWidget()
            text_edit.setPlainText(content)
            self.update_tab_title(text_edit, file_name)

    def save_document(self):
        current_text_edit = self.tab_widget.currentWidget()

        if current_text_edit and hasattr(current_text_edit, 'file_name'):
            with open(current_text_edit.file_name, "w") as file:
                file.write(current_text_edit.toPlainText())
        else:
            self.save_document_as()

    def save_document_as(self):
        current_text_edit = self.tab_widget.currentWidget()

        if current_text_edit:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "Text Files (*.txt);;All Files (*)")

            if file_name:
                with open(file_name, "w") as file:
                    file.write(current_text_edit.toPlainText())

                current_text_edit.file_name = file_name
                self.update_tab_title(current_text_edit, file_name)

    # Add the method to handle closing the current tab
    def close_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            self.tab_widget.removeTab(current_index)

    def update_tab_title(self, text_edit, title):
        index = self.tab_widget.indexOf(text_edit)

        # Use QFileInfo to extract the file name
        file_info = QFileInfo(title)
        file_name = file_info.fileName()

        self.tab_widget.setTabText(index, file_name)

    def show_settings(self):
        # Create a context menu for settings
        menu = QMenu(self)

        # Font Action
        font_action = QAction("Change Font", self)
        font_action.triggered.connect(self.change_font)
        menu.addAction(font_action)

        # Show the context menu
        menu.exec(self.mapToGlobal(self.cursor().pos()))

    def change_font(self):
        # Get the current text edit widget
        current_text_edit = self.tab_widget.currentWidget()

        # Open the font dialog to change the font
        font, ok = QFontDialog.getFont(current_text_edit.font(), self, "Select Font")
        if ok:
            current_text_edit.setFont(font)

            # Save the font settings to the configuration file
            self.settings.setValue("font", font.toString())

    def close_tab(self, index):
        # Close the tab when the close button is clicked
        self.tab_widget.removeTab(index)

    def update_status_bar(self):
        # Update the status bar with relevant information
        current_text_edit = self.tab_widget.currentWidget()
        if current_text_edit:
            cursor = current_text_edit.textCursor()
            cursor_position = cursor.position()
            word_count = len(current_text_edit.toPlainText().split())
            tab_count = current_text_edit.toPlainText().count('\t')

            status_text = f"Cursor Position: {cursor_position} | Word Count: {word_count} | Tab Count: {tab_count}"
            self.status_bar.showMessage(status_text)
            print(status_text)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad = NotepadApp()
    notepad.show()
    sys.exit(app.exec())
