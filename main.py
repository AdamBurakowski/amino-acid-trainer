import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow
)
from database import amino_acids
from main_menu import MainMenu
from mode_name_to_code import (
    NameToCodeModeSetup, NameToCodeMode
)
from random import choice

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Amino Acid Trainer")

        self.menu = MainMenu(self.start_name_to_code_mode)
        self.setCentralWidget(self.menu)

    def start_name_to_code_mode(self, lang):
        self.name_mode_setup = NameToCodeModeSetup(self.back_to_menu, self.play_name_to_code_mode, lang)
        self.setCentralWidget(self.name_mode_setup)

    def play_name_to_code_mode(self, quiz_data):
        self.name_mode = NameToCodeMode(self.back_to_menu, quiz_data)
        self.setCentralWidget(self.name_mode)

    def back_to_menu(self):
        self.menu = MainMenu(self.start_name_to_code_mode)
        self.setCentralWidget(self.menu)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
