from PySide6.QtWidgets import (QDialog,
                               QVBoxLayout,
                               QLabel,
                               QMessageBox,
                               QLineEdit,
                               QPushButton,
                               QFormLayout)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from app import MainApp

import pandas as pd
import os

class LoginPage(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(360, 480)
        self.setStyleSheet("background-color: white")
        
        layout = QVBoxLayout(self)
        label= QLabel('Login')
        layout.addWidget(label)

class LoginPage(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(360, 480)

        self.auth_database_path = "database/auth_data.pkl"
        
        if os.path.exists(self.auth_database_path):
            self.auth_data = pd.read_pickle(self.auth_database_path)
        else:
            QMessageBox.warning(self, "Warning", "No Authentication Database Found\nPlease register first.")
            self.auth_data = pd.DataFrame(columns=["username", "password", "full_name"])

        layout = QVBoxLayout(self)

        # Title Label
        self.mainlabel = QLabel('LOGIN')
        self.mainlabel.setFont(QFont("Arial", 16, QFont.Bold))
        self.mainlabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mainlabel)

        # Form layout for input fields
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Username Field
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Enter your username")
        self.username_label = QLabel("Username")
        form_layout.addRow(self.username_label, self.username_field)

        # Password Field
        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Enter your password")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_label = QLabel("Password")
        form_layout.addRow(self.password_label, self.password_field)

        layout.addLayout(form_layout)

        # Warning label for validation messages
        self.warning_label = QLabel("")
        self.warning_label.setFont(QFont("Roboto", 10, QFont.Bold))
        self.warning_label.setStyleSheet("color: red")
        self.warning_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.warning_label)

        # Login Button
        self.login_button = QPushButton("LOGIN")
        self.login_button.setFont(QFont("Roboto", 12, QFont.Bold))
        self.login_button.clicked.connect(self.login_user)
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        self.applystyles()

    def applystyles(self):
        """Applies additional styles for button and form elements."""
        self.login_button.setStyleSheet(
            """ 
            QPushButton {background-color: deepskyblue;
                         color: white;
                         border-radius: 10px;
                         padding: 10px 20px;
                         font-weight: bold;
                         font-size: 14px;}
            QPushButton:hover {background-color: dodgerblue;}
            QPushButton:pressed {background-color: royalblue;}
            """
        )

    def login_user(self):
        """
        Handles user login. Checks if the username and password are correct.
        """
        username = self.username_field.text().strip()
        password = self.password_field.text().strip()

        # Validation checks
        if not username or not password:
            self.warning_label.setText("Both fields are required!")
            return

        # Check if the username exists in the database
        if username not in self.auth_data["username"].values:
            self.warning_label.setText("Username does not exist!")
            return

        # Check if the password matches the username
        stored_password = self.auth_data.loc[self.auth_data["username"] == username, "password"].values[0]
        if password != stored_password:
            self.warning_label.setText("Incorrect password!")
            return
        full_name = self.auth_data.loc[self.auth_data["username"] == username, "full_name"].values[0]

        QMessageBox.information(self, "Success", f"Welcome back, {full_name}!")
        app = MainApp(username)
        app.show()
        self.parent().close()
        self.close()

class RegisterPage(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setFixedSize(360, 480)

        self.auth_database_path = "database/auth_data.pkl"
        
        if os.path.exists(self.auth_database_path):
            self.auth_data = pd.read_pickle(self.auth_database_path)
        else:
            QMessageBox.warning(self, "Warning", "No Authentication Database Found\nCreating Fresh Database")
            self.auth_data = pd.DataFrame(columns=["username", "password", "full_name"])

        layout = QVBoxLayout(self)

        # Title Label
        self.mainlabel = QLabel('REGISTER')
        self.mainlabel.setFont(QFont("Arial", 16, QFont.Bold))
        self.mainlabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mainlabel)

        # Form layout for input fields
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Full Name
        self.full_name_field = QLineEdit()
        self.full_name_field.setPlaceholderText("Enter your full name")
        self.full_name_label = QLabel("Full Name")
        form_layout.addRow(self.full_name_label, self.full_name_field)

        # Username
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Enter a unique username")
        self.username_label = QLabel("Username")
        form_layout.addRow(self.username_label, self.username_field)

        # Password
        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Enter your password")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_label = QLabel("Password")
        form_layout.addRow(self.password_label, self.password_field)

        # Confirm Password
        self.confirm_password_field = QLineEdit()
        self.confirm_password_field.setPlaceholderText("Confirm your password")
        self.confirm_password_field.setEchoMode(QLineEdit.Password)
        self.confirm_password_label = QLabel("Confirm Password")
        form_layout.addRow(self.confirm_password_label, self.confirm_password_field)

        layout.addLayout(form_layout)

        # Warning label for validation messages
        self.warning_label = QLabel("")
        self.warning_label.setFont(QFont("Roboto", 10, QFont.Bold))
        self.warning_label.setStyleSheet("color: red")
        self.warning_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.warning_label)

        # Register Button
        self.register_button = QPushButton("REGISTER")
        self.register_button.setFont(QFont("Roboto", 12, QFont.Bold))
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        self.applystyles()

    def applystyles(self):
        """Applies additional styles for button and form elements."""
        self.register_button.setStyleSheet(
            """ 
            QPushButton {background-color: limegreen;
                         color: white;
                         border-radius: 10px;
                         padding: 10px 20px;
                         font-weight: bold;
                         font-size: 14px;}
            QPushButton:hover {background-color: lightseagreen;}
            QPushButton:pressed {background-color: teal;}
            """
        )

    def register_user(self):
        """
        Handles user registration. Checks for valid input, matching passwords, and uniqueness of the username.
        """
        full_name = self.full_name_field.text().strip()
        username = self.username_field.text().strip()
        password = self.password_field.text().strip()
        confirm_password = self.confirm_password_field.text().strip()

        # Validation checks
        if not full_name or not username or not password or not confirm_password:
            self.warning_label.setText("All fields are required!")
            return

        if password != confirm_password:
            self.warning_label.setText("Passwords do not match!")
            return

        if username in self.auth_data["username"].values:
            self.warning_label.setText("This username is already taken!")
            return

        # Add the new user to the authentication data
        new_user = {"username": username, "password": password, "full_name": full_name}
        self.auth_data = pd.concat([self.auth_data, pd.DataFrame([new_user])], ignore_index=True)

        # Save the updated authentication data
        self.auth_data.to_pickle(self.auth_database_path)

        QMessageBox.information(self, "Success", "Registration successful!")
        self.close()   