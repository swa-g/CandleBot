from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu, 
                               QStatusBar, QPushButton, QTabWidget, 
                               QWidget, QDateEdit, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit,QComboBox,QCalendarWidget)
from PySide6.QtGui import QFont, QAction
from PySide6.QtCore import Qt
from PySide6.QtCharts import QChart, QChartView, QCandlestickSeries,QCandlestickSet

import yfinance as yf
import sys

import sys
import yfinance as yf
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
import pyqtgraph as pg
from PyQt5.QtCore import Qt

class Graph(QWidget):
    def __init__(self):
        super().__init__()
        #self.setWindowTitle("Interactive Stock Graph")
        #self.setGeometry(100, 100, 800, 600)

        # Fetch data using yfinance
        self.data = yf.download("AAPL", start="2023-01-01", end="2024-01-01", multi_level_index=False, progress=False)
        self.candlesticks = []  # Store candlestick information for hover
        self.tooltip_label = None  # Label for showing current coordinates
        self.ohlc_label = None  # Label for OHLC and Volume data
        self.plot_data()
        
    def plot_data(self):
        # Create a central widget and layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a label for the tooltip
        self.tooltip_label = QLabel("Coordinates: ")
        layout.addWidget(self.tooltip_label)

        # Create a label for OHLC and Volume data
        self.ohlc_label = QLabel("OHLC & Volume: ")
        layout.addWidget(self.ohlc_label)

        # Plot candlesticks
        self.candlestick_plot = pg.PlotWidget()
        layout.addWidget(self.candlestick_plot)

        # Plot volume on a separate subplot
        self.volume_plot = pg.PlotWidget()
        layout.addWidget(self.volume_plot)
        self.volume_plot.setFixedHeight(200)

        # Plot candlesticks and volume
        self.plot_candlesticks()
        self.plot_volume()

        # Enable dragging and zooming
        self.candlestick_plot.setMouseEnabled(x=True, y=True)  # Enable mouse interaction
        self.volume_plot.setMouseEnabled(x=True, y=True)  # Enable mouse interaction

        # Install an event filter to capture mouse movements
        self.candlestick_plot.scene().sigMouseMoved.connect(self.mouseMoved)

        # Synchronize x-axis ranges
        self.candlestick_plot.sigXRangeChanged.connect(self.sync_x_range_vol)
        self.volume_plot.sigXRangeChanged.connect(self.sync_x_range_candle)

    def plot_candlesticks(self):
        # Set the width of the candlestick
        candle_width = 0.5
        wick_width = 0.02

        # Get the dates from the DataFrame
        dates = self.data.index.to_numpy()

        for i in range(1, len(self.data)):
            open_price = self.data['Open'].to_numpy()[i]
            close_price = self.data['Close'].to_numpy()[i]
            high_price = self.data['High'].to_numpy()[i]
            low_price = self.data['Low'].to_numpy()[i]
            x = i  # x position of the candlestick

            # Determine color based on price movement
            if close_price >= open_price:
                color = 'g'  # Green for up
                lower = open_price
                upper = close_price
            else:
                color = 'r'  # Red for down
                lower = close_price
                upper = open_price

            # Draw the candlestick body
            candlestick_body = pg.BarGraphItem(x0=x - candle_width / 2, x1=x + candle_width / 2, y0=lower, y1=upper, pen=color, brush=color)
            self.candlestick_plot.addItem(candlestick_body)

            # Draw the wick
            wick = pg.BarGraphItem(x0=x - wick_width / 2, x1=x + wick_width / 2, y0=low_price, y1=high_price, pen=color, brush=color)
            self.candlestick_plot.addItem(wick)

            # Store candlestick information for hover
            self.candlesticks.append((x, open_price, close_price, high_price, low_price))

        # Set axis labels
        self.candlestick_plot.setLabel('left', 'Price')
        self.candlestick_plot.setLabel('bottom', 'Date')

        # Set the x-axis ticks to the actual dates dynamically
        self.candlestick_plot.setXRange(0, len(self.data) - 1)
        self.candlestick_plot.setYRange(self.data['Low'].min(), self.data['High'].max())

        # Set dynamic x-axis ticks
        self.update_date_ticks()

        # Enable grid lines
        self.candlestick_plot.showGrid(x=True, y=True)

    def update_date_ticks(self):
        """Update the x-axis ticks based on the current view range."""
        ticks = self.get_date_ticks()
        self.candlestick_plot.getAxis('bottom').setTicks(ticks)
        self.volume_plot.getAxis('bottom').setTicks(ticks)
        

    def sync_x_range_vol(self):
        # Get the current x-range of the candlestick plot
        x_range = self.candlestick_plot.viewRange()[0]
        # Set the x-range of the volume plot to match
        self.volume_plot.setXRange(x_range[0], x_range[1], padding=0)
        self.volume_plot.setYRange(0, self.data['Volume'].to_numpy().max())
        self.update_date_ticks()  # Update ticks when syncing

    def sync_x_range_candle(self):
        # Get the current x-range of the volume plot
        x_range = self.volume_plot.viewRange()[0]
        # Set the x-range of the candlestick plot to match
        self.candlestick_plot.setXRange(x_range[0], x_range[1], padding=0)
        self.update_date_ticks()  # Update ticks when syncing

    def plot_volume(self):
        # Set the volume data
        volume_data = self.data['Volume'].to_numpy()
        x = range(len(volume_data))

        # Create the volume bar graph
        volume_bars = pg.BarGraphItem(x0=x, x1=x, y0=0, y1=volume_data, pen='b', brush='b', width=0.5)
        self.volume_plot.addItem(volume_bars)

        # Set the volume axis label on the right
        self.volume_plot.setLabel('left', 'Volume')
        self.volume_plot.setYRange(0, volume_data.max())
        self.volume_plot.getAxis('bottom').setTicks(self.get_date_ticks())

        # Enable grid lines
        self.volume_plot.showGrid(x=True, y=True)

    def get_date_ticks(self):
        """Generate dynamic date ticks for the x-axis based on the current view range."""
        x_range = self.candlestick_plot.viewRange()[0]  # Get current x-range
        visible_points = int(x_range[1] - x_range[0])  # Calculate number of visible points
        
        # Determine the number of ticks based on the number of visible points
        num_ticks = max(1, min(visible_points // 10, len(self.data) // 10))  # Adjust this divisor as needed

        ticks = []
        for i in range(0, len(self.data), num_ticks):
            date_str = self.data.index[i].strftime('%Y-%m-%d')
            ticks.append((i, date_str))
        return [ticks]

    def mouseMoved(self, evt):
        pos = evt  # using signal from scene
        if self.candlestick_plot.sceneBoundingRect().contains(pos):
            mouse_point = self.candlestick_plot.plotItem.vb.mapSceneToView(pos)
            index = int(mouse_point.x())

            if 0 <= index < len(self.candlesticks):
                x, open_price, close_price, high_price, low_price = self.candlesticks[index]
                # Update the tooltip label with current coordinates
                tooltip_text = "Date: %s | Price: Rs. %.2f" % (self.data.index[x].date(), mouse_point.y())
                self.tooltip_label.setText(tooltip_text)

                # Update the OHLC and Volume label
                volume = self.data['Volume'].to_numpy()[x]
                ohlc_text = f"Open: Rs. {open_price:.2f} | High: Rs. {high_price:.2f} | Low: Rs. {low_price:.2f} | Close: Rs. {close_price:.2f} | Volume: {volume}"
                self.ohlc_label.setText(ohlc_text)
            else:
                self.tooltip_label.setText("Coordinates: ")  # Clear label if not over any candlestick
                self.ohlc_label.setText("OHLC & Volume: ")  # Clear label if not over any candlestick
        else:
            self.tooltip_label.setText("Coordinates: ")  # Clear label if outside the plot area
            self.ohlc_label.setText("OHLC & Volume: ")  # Clear label if outside the plot area

class GraphTab(QWidget):
    def __init__(self):
        super().__init__()
        
        searchbar = QLineEdit("Search any Stock from NSE andd BSE")

        period = QComboBox()
        period.setMinimumWidth(70)
        period.addItems(["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"])

        interval = QComboBox()
        interval.setMinimumWidth(70)
        interval.addItems(["1m", "2m", "5m", "15m", "30m", "1h", "1d", "5d", "1wk", "1mo", "3mo"])

        start_date = QDateEdit()
        start_date.setCalendarPopup(True)
        start_date.setDisplayFormat("yyyy-MM-dd")
        
        end_date = QDateEdit()
        start_date.setCalendarPopup(True)
        start_date.setDisplayFormat("yyyy-MM-dd")

        graph_type = QComboBox()
        graph_type.addItems(['line', 'candle'])
        
        top_bar = QHBoxLayout()
        top_bar.addWidget(searchbar)
        top_bar.addWidget(QLabel("Period"))
        top_bar.addWidget(period)
        top_bar.addWidget(QLabel("Interval"))
        top_bar.addWidget(interval)
        top_bar.addWidget(QLabel("Start Date"))
        top_bar.addWidget(start_date)
        top_bar.addWidget(QLabel("End Date"))
        top_bar.addWidget(end_date)
        top_bar.addWidget(QLabel("Graph Type"))
        top_bar.addWidget(graph_type)

        graph = Graph()

        tab_layout=QVBoxLayout()
        tab_layout.addLayout(top_bar)
        tab_layout.addWidget(graph) 

        self.setLayout(tab_layout)


    def get_graph(self, df):
        graph = QCandlestickSeries()
        graph.setDecreasingColor(Qt.red)
        graph.setIncreasingColor(Qt.green)
        dates = []
        for index, row in df.iterrows():
            o = row['Open']
            h = row['High']
            l = row['Low']
            c = row['Close']
            graph.append(QCandlestickSet(o, h, l, c))
            dates.append(index.strftime('%Y-%m-%d'))  # Format 
        chart = QChart()
        chart.addSeries(graph)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.createDefaultAxes()
        chart.legend().hide()
        chart.axes(Qt.Horizontal)[0].setCategories(dates)
        chartview = QChartView(chart)
        return chartview

if __name__ == "__main__":
    myapp = QApplication(sys.argv)
    gt = GraphTab()
    gt.show()
    myapp.exec()
