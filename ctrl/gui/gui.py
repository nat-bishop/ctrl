import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QMessageBox, QDialog, QInputDialog
from ctrl.backup.backup_implementation import backup
from ctrl.sync.sync_implementation import sync
from ctrl.search.search_project_implementation import search as search_project_impl
from ctrl.search.search_asset_implementation import search_asset as search_asset_impl
from ctrl.search.search_user_implementation import search_user
from ctrl.edit.edit_project_implementation import edit
from ctrl.new.new_project_implementation import new as new_project_impl
from ctrl.new.new_user_implementation import new_user
from ctrl.new.new_file_implementation import new_file
from ctrl.new.new_asset_implementation import new_asset
from ctrl.open.open_implementation import open as open_impl
from ctrl.save.save_implementation import save
from ctrl.delete.delete_user_implementation import delete_user
from ctrl.delete.delete_project_implementation import delete_project
import ctrl.database.utils as utils


class ArtProjectManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Art Project Manager")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Create buttons for each CLI command
        search_project_button = QPushButton("Search Project")
        search_project_button.clicked.connect(self.search_project)
        layout.addWidget(search_project_button)
        """
        # Create buttons for each CLI command
        backup_button = QPushButton("Backup")
        backup_button.clicked.connect(self.backup)
        layout.addWidget(backup_button)

        sync_button = QPushButton("Sync")
        sync_button.clicked.connect(self.sync)
        layout.addWidget(sync_button)

        search_asset_button = QPushButton("Search Asset")
        search_asset_button.clicked.connect(self.search_asset)
        layout.addWidget(search_asset_button)

        search_user_button = QPushButton("Search User")
        search_user_button.clicked.connect(self.search_user)
        layout.addWidget(search_user_button)

        edit_project_button = QPushButton("Edit Project")
        edit_project_button.clicked.connect(self.edit_project)
        layout.addWidget(edit_project_button)

        new_project_button = QPushButton("New Project")
        new_project_button.clicked.connect(self.new_project)
        layout.addWidget(new_project_button)

        new_user_button = QPushButton("New User")
        new_user_button.clicked.connect(self.new_user)
        layout.addWidget(new_user_button)

        new_file_button = QPushButton("New File")
        new_file_button.clicked.connect(self.new_file)
        layout.addWidget(new_file_button)

        new_asset_button = QPushButton("New Asset")
        new_asset_button.clicked.connect(self.new_asset)
        layout.addWidget(new_asset_button)

        open_project_button = QPushButton("Open Project")
        open_project_button.clicked.connect(self.open_project)
        layout.addWidget(open_project_button)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)
        layout.addWidget(save_button)

        delete_user_button = QPushButton("Delete User")
        delete_user_button.clicked.connect(self.delete_user)
        layout.addWidget(delete_user_button)

        delete_project_button = QPushButton("Delete Project")
        delete_project_button.clicked.connect(self.delete_project)
        layout.addWidget(delete_project_button)
        """

        central_widget.setLayout(layout)

    def backup(self):
        backup()
        QMessageBox.information(self, "Backup", "Backup completed successfully.")

    def sync(self):
        sync_direction = "remote_to_source"  # or get from user input
        delete = False  # or get from user input
        sync(sync_direction, delete)
        QMessageBox.information(self, "Sync", "Sync completed successfully.")

    def search_project(self):
        self.show_search_project_dialog()

    def search_asset(self):
        self.show_search_asset_dialog()

    def search_user(self):
        user_name = self.get_text_input("Search User", "Enter user name:")
        if user_name:
            search_user(user_name)

    def edit_project(self):
        self.show_edit_project_dialog()

    def new_project(self):
        self.show_new_project_dialog()

    def new_user(self):
        self.show_new_user_dialog()

    def new_file(self):
        self.show_new_file_dialog()

    def new_asset(self):
        self.show_new_asset_dialog()

    def open_project(self):
        project_name = self.get_text_input("Open Project", "Enter project name:")
        tool = self.get_text_input("Open Project", "Enter tool (optional):")
        file = self.get_text_input("Open Project", "Enter file (optional):")
        open_impl(project_name, tool, file)

    def save(self):
        tool = self.get_text_input("Save", "Enter tool:")
        name = self.get_text_input("Save", "Enter new name (optional):")
        file_type = self.get_text_input("Save", "Enter file type (optional):")
        save(tool, name, file_type)

    def delete_user(self):
        name = self.get_text_input("Delete User", "Enter user name:")
        if name:
            utils.perform_db_op(delete_user, name)

    def delete_project(self):
        name = self.get_text_input("Delete Project", "Enter project name:")
        if name:
            utils.perform_db_op(delete_project, name)

    def get_text_input(self, title, label):
        text, ok = QInputDialog.getText(self, title, label)
        if ok:
            return text
        return None

    def show_search_project_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Search Project")

        layout = QVBoxLayout()

        project_name_label = QLabel("Project Name:")
        self.project_name_input = QLineEdit()
        layout.addWidget(project_name_label)
        layout.addWidget(self.project_name_input)

        creators_label = QLabel("Creators (comma-separated):")
        self.creators_input = QLineEdit()
        layout.addWidget(creators_label)
        layout.addWidget(self.creators_input)

        tags_label = QLabel("Tags (comma-separated):")
        self.tags_input = QLineEdit()
        layout.addWidget(tags_label)
        layout.addWidget(self.tags_input)

        from_date_label = QLabel("From Date (YYYY-MM-DD):")
        self.from_date_input = QLineEdit()
        layout.addWidget(from_date_label)
        layout.addWidget(self.from_date_input)

        to_date_label = QLabel("To Date (YYYY-MM-DD):")
        self.to_date_input = QLineEdit()
        layout.addWidget(to_date_label)
        layout.addWidget(self.to_date_input)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_search_project)
        layout.addWidget(submit_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def submit_search_project(self):
        project_name = self.project_name_input.text()
        creators = self.creators_input.text().split(',')
        tags = self.tags_input.text().split(',')
        from_date = self.from_date_input.text()
        to_date = self.to_date_input.text()
        gui = False
        search_project_impl(project_name, creators, tags, from_date, to_date, gui)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ArtProjectManagerApp()
    main_window.show()
    sys.exit(app.exec_())