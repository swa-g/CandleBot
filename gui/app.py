from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu, 
                               QStatusBar, QPushButton, QTabWidget, 
                               QWidget, QVBoxLayout, QLabel, QHBoxLayout)
from PySide6.QtGui import QFont, QAction
from PySide6.QtCore import Qt

from tabs import GraphTab
import pandas as pd

class MainApp(QMainWindow):
    def __init__(self,username):
        super().__init__()
        
        self.auth_database_path = "database/auth_data.pkl"
        self.auth_data = pd.read_pickle(self.auth_database_path)
        full_name = self.auth_data.loc[self.auth_data["username"] == username, "full_name"].values[0]
        
        self.setWindowTitle(f"Hi {full_name} - Welcome to CandleBot")
        self.setMinimumSize(1280,768)


        self.menubar = self.menuBar()
        profile_menu = self.menubar.addMenu("Profile")
        
        edit_profile_action = QAction("Edit Profile", self)
        edit_profile_action.triggered.connect(self.edit_profile)
        profile_menu.addAction(edit_profile_action)

        remove_profile_action = QAction("Remove Profile", self)
        remove_profile_action.triggered.connect(self.remove_profile)
        profile_menu.addAction(remove_profile_action)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.tabs = QTabWidget(self.central_widget)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.tabs)

        # Add some tabs
        tab1 = GraphTab()
        self.tabs.addTab(tab1, "Search")

        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)
        tab2_layout.addWidget(QLabel("Tab 2 Content"))
        self.tabs.addTab(tab2, "Tab 2")
        
        # 3. StatusBar with LogOut Button
        self.statusbar = self.statusBar()
        logout_button = QPushButton("Log Out", self)
        logout_button.clicked.connect(self.logout)
        self.statusbar.addPermanentWidget(logout_button)

    def edit_profile(self):
        # Logic for editing the profile
        print("Edit Profile clicked")

    def remove_profile(self):
        # Logic for removing the profile
        print("Remove Profile clicked")

    def logout(self):
        # Logic to log out and show the home page
        print("Logout Button clicked")

        pass

if __name__ == "__main__":
    cbapp = QApplication([])
    window = MainApp('swg')
    window.show()
    cbapp.exec()
