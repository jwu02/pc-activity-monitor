from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt, pyqtSignal

class TimeoutIntervalSliderWidget(QWidget):
    # Define a signal that emits the new interval value
    timeoutIntervalChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
    
        self.valid_values = [1, 5, 10, 20, 30]
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Timeout Interval: 1 min", self)
        self.layout.addWidget(self.label)

        self.timeout_interval_slider = QSlider(Qt.Horizontal)
        self.timeout_interval_slider.setMinimum(0)
        self.timeout_interval_slider.setMaximum(len(self.valid_values) - 1)
        self.timeout_interval_slider.setTickInterval(1)
        self.timeout_interval_slider.setTickPosition(QSlider.TicksBelow)
        self.timeout_interval_slider.setSingleStep(1)
        self.timeout_interval_slider.valueChanged.connect(self.adjust_value)
        self.layout.addWidget(self.timeout_interval_slider)

        self.setLayout(self.layout)

    def adjust_value(self):
        index = self.timeout_interval_slider.value()
        value = self.valid_values[index]
        self.label.setText(f"Timeout Interval: {value} min")

        self.timeoutIntervalChanged.emit(value)  # Emit the signal with the new interval
