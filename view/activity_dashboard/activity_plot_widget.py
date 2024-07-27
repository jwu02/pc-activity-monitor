from pyqtgraph import PlotWidget, DateAxisItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout

import time

class ActivityPlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.data = {
            'activities': {
                'key-presses': [],
                'left-clicks': [],
                'right-clicks': [],
                'mouse-movements': []
            },
            'timestamps': []
        }

        self.layout = QVBoxLayout(self)

        # Setup the plot widget
        self.plt = PlotWidget()
        # https://stackoverflow.com/questions/29385868/plotting-datetime-objects-with-pyqtgraph
        axis = DateAxisItem()
        self.plt.setAxisItems({'bottom': axis})
        self.plt.setLimits(xMin=time.time(), yMin=0)
        self.plt.addLegend()

        # Disable interactions
        self.plt.setMouseEnabled(False)
        self.plt.getViewBox().setMouseEnabled(False, False)
        self.plt.setMenuEnabled(False)
        
        self.layout.addWidget(self.plt)

        self.curves = {}
        plot_configs = {
            'key-presses': {'pen-color': 'r', 'label': 'Key Presses'},
            'left-clicks': {'pen-color': 'g', 'label': 'Left Clicks'},
            'right-clicks': {'pen-color': 'b', 'label': 'Right Clicks'},
            'mouse-movements': {'pen-color': 'w', 'label': 'Mouse Movements'},
        }

        for k, v in self.data['activities'].items():
            self.curves[k] = self.plt.plot(pen=plot_configs[k]['pen-color'], 
                name=plot_configs[k]['label'])

    def set_data(self, data) -> None:
        self.data = data
        # after settings the data update the plot
        self.update_plot()

    def update_plot(self) -> None:
        for k, curve in self.curves.items():
            curve.setData(self.data['timestamps'], self.data['activities'][k])
    