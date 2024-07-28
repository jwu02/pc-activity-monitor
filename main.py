from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont

from view.main_window import MainWindow


def init_ui():
    app = QApplication([])

    # Load the Roboto Mono font
    font_id = QFontDatabase.addApplicationFont("fonts/Roboto_Mono/static/RobotoMono-Regular.ttf")
    if font_id == -1:
        print("Failed to load Roboto Mono font.")
    else:
        roboto_mono = QFont("Roboto Mono", 9)
        QApplication.setFont(roboto_mono)  # Set the global font

    mw = MainWindow()

    # Run the app
    app.exec()


if __name__=="__main__":
    init_ui()