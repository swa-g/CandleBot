from PySide6.QtWidgets import (QApplication, 
                               QWidget, 
                               QVBoxLayout, 
                               QHBoxLayout,
                               QLabel,
                               QPushButton,
                               QSizePolicy)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt

from auth import LoginPage, RegisterPage

class CandleBot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CandleBot")
        self.setFixedSize(1280, 720)
        
        

        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        "LOGO IMAGE"
        logo_label = QLabel()
        logo_pixmap = QPixmap("resources/CandleBot_dark.png")
        logo_label.setPixmap(logo_pixmap)
        logo_label.setScaledContents(True)
        logo_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        "BUTTONS"
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(30)
        buttons_layout.setContentsMargins(200, 0, 200, 100)
        
        self.login_button = QPushButton("LOGIN")
        self.login_button.setFont(QFont("Roboto", 12, QFont.Bold))
        self.login_button.pressed.connect(self.show_loginpage)

        self.register_button = QPushButton("REGISTER")
        self.register_button.setFont(QFont("Roboto", 12, QFont.Bold))
        self.register_button.pressed.connect(self.show_registerpage)

        buttons_layout.addWidget(self.login_button)
        buttons_layout.addWidget(self.register_button)
        
        layout.addLayout(buttons_layout)

        self.applystyles()

    def applystyles(self):
        #self.setStyleSheet("background-color: white")

        self.login_button.setStyleSheet(""" QPushButton {background-color: limegreen;
                                                        color: white;
                                                        border-radius: 10px;
                                                        padding: 10px;
                                                    }
                                            QPushButton:hover {background-color: lightseagreen;}
                                            QPushButton:pressed {background-color: teal;}""")
        self.register_button.setStyleSheet("""  QPushButton {background-color: crimson;
                                                            color: white;
                                                            border-radius: 10px;
                                                            padding: 10px;
                                                        }
                                                QPushButton:hover {background-color: mediumvioletred;}
                                                QPushButton:pressed {background-color: darkred;}""")
        
    def show_loginpage(self):
        self.login_page = LoginPage()
        self.login_page.show()
    
    def show_registerpage(self):
        self.register_page = RegisterPage()
        self.register_page.show()


if __name__ == "__main__":
    app = QApplication([])
    cb = CandleBot()
    cb.show()
    app.exec()