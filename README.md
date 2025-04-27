
Built by https://www.blackbox.ai

---

```markdown
# Future MT5 Trading Panel

## Project Overview
The **Future MT5 Trading Panel** is a graphical user interface (GUI) application developed using Python's Tkinter library. It interfaces with MetaTrader 5 (MT5) to support trading activities via an accessible panel. The application provides real-time monitoring of balance, allows users to select trading assets, define timeframes, and set lot sizes, while displaying logs of activities and errors within the system.

## Installation

To run this project, you need to have Python installed on your system. The application uses several external libraries, which can be installed via pip. Here’s how to set up the project:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/future-mt5-trading-panel.git
   cd future-mt5-trading-panel
   ```

2. **Install Required Libraries:**
   You need to install the following libraries using pip:
   ```bash
   pip install MetaTrader5
   pip install tk
   ```

3. **Make Sure MetaTrader 5 is Installed:**
   Ensure you have MetaTrader 5 installed on your machine. You will need to configure it for automated trading.

## Usage
1. **Launch the Application:**
   Run the application using Python:
   ```bash
   python painel_app.py
   ```

2. **Using the Panel:**
   - Select the trading asset from the **Trading Options** dropdown.
   - Choose a **timeframe** from the available options.
   - Enter the **lot size** for trading.
   - Click **"Atualizar Ativos"** to refresh the list of tradable assets.
   - Click **"Iniciar Análise com o Robô"** to begin trading analysis.
   - Click **"Parar Análise"** to stop the operations.

## Features
- Modern and responsive UI built with Tkinter.
- Real-time balance monitoring connected to MetaTrader 5.
- Supporting multiple assets with the ability to select trading timeframes.
- Logging system integrated to track activities and errors.
- Adjustable lot sizes for trades.
- Threads to manage background processing for balance updates and trading strategy execution.

## Dependencies
The following dependencies are required:
- `MetaTrader5`: For interfacing with the MT5 trading platform.
- `tkinter`: Provides the GUI capabilities for the application.

Make sure to install these libraries via pip as indicated in the installation section.

## Project Structure
```
future-mt5-trading-panel/
│
├── painel_app.py          # Main application file launching the GUI
├── utils.py               # Contains utility functions, such as balance retrieval
├── estrategia.py          # Contains the trading strategy logic
└── log_system.py          # Implements logging for the application
```

### Note
Make sure to run this application in an environment where MetaTrader 5 is properly configured and running, with appropriate permissions enabled for automated trading.

---

Enjoy trading with the Future MT5 Trading Panel!
```