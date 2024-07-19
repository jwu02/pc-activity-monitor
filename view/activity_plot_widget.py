from pyqtgraph import PlotWidget, DateAxisItem, InfiniteLine, mkPen, TextItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

import time

class ActivityPlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # List to store click counts for plotting
        self.key_presses = []
        self.left_clicks = []
        self.right_clicks = []
        self.mouse_movements = []
        self.timestamps = []

        self.layout = QVBoxLayout(self)

        # Setup the plot widget
        self.plt = PlotWidget()
        # https://stackoverflow.com/questions/29385868/plotting-datetime-objects-with-pyqtgraph
        axis = DateAxisItem()
        self.plt.setAxisItems({'bottom':axis})
        self.plt.setLimits(xMin=time.time(), yMin=0)
        self.plt.addLegend()

        # Disable interactions
        self.plt.setMouseEnabled(False)
        self.plt.getViewBox().setMouseEnabled(False, False)
        self.plt.setMenuEnabled(False)

        self.layout.addWidget(self.plt)
        
        # Plot data
        self.key_press_curve = self.plt.plot(pen='r', name='Key Presses')
        self.left_click_curve = self.plt.plot(pen='g', name='Left Clicks')
        self.right_click_curve = self.plt.plot(pen='b', name='Right Clicks')
        self.mouse_movement_curve = self.plt.plot(pen='w', name='Mouse Movements')
    

    def update_plot(self) -> None:
        self.key_press_curve.setData(self.timestamps, self.key_presses)
        self.left_click_curve.setData(self.timestamps, self.left_clicks)
        self.right_click_curve.setData(self.timestamps, self.right_clicks)
        self.mouse_movement_curve.setData(self.timestamps, self.mouse_movements)
