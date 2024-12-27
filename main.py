import sys
from PyQt6.QtWidgets import QApplication, QDialog
from GUITASK import Ui_Dialog


class MainApp(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
