import sys
import yfinance as yf
import pandas as pd
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem

class TradingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NIFTY Trading Signals")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("Press 'Fetch Data' to get buy/sell signals", self)
        self.layout.addWidget(self.label)

        self.fetch_button = QPushButton("Fetch Data", self)
        self.fetch_button.clicked.connect(self.fetch_data)
        self.layout.addWidget(self.fetch_button)

        self.buy_list_widget = QListWidget()
        self.layout.addWidget(self.buy_list_widget)

        self.sell_list_widget = QListWidget()
        self.layout.addWidget(self.sell_list_widget)

        self.setLayout(self.layout)

    def fetch_data(self):
        # Fetch NIFTY data
        nifty_data = yf.download("^NSEI", interval="2m", period="1d")

        # Calculate EMA
        nifty_data['EMA_5'] = nifty_data['Close'].ewm(span=5, adjust=False).mean()

        # Get buy and sell signals
        buy_signals, sell_signals = self.buy_sell_signals(nifty_data)

        # Update lists with signals
        self.update_signal_list(self.buy_list_widget, buy_signals, "Buy Signal")
        self.update_signal_list(self.sell_list_widget, sell_signals, "Sell Signal")

        # Update label with signal counts
        self.label.setText(f"Buy Signals: {len(buy_signals)}\nSell Signals: {len(sell_signals)}")

    def buy_sell_signals(self, data):
        buy_signals = []
        sell_signals = []
        for i in range(1, len(data)):
            if data['Close'][i] > data['EMA_5'][i] and data['Close'][i-1] <= data['EMA_5'][i-1]:
                buy_signals.append(data.index[i])
            elif data['Close'][i] < data['EMA_5'][i] and data['Close'][i-1] >= data['EMA_5'][i-1]:
                sell_signals.append(data.index[i])
        return buy_signals, sell_signals

    def update_signal_list(self, list_widget, signals, signal_type):
        list_widget.clear()
        for signal in signals:
            item = QListWidgetItem(f"{signal_type} at {signal}")
            list_widget.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    trading_app = TradingApp()
    trading_app.show()

    sys.exit(app.exec())
