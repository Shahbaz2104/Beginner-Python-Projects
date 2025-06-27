import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt

class StockPortfolio:
    def __init__(self, api_key):
        self.api_key = api_key
        self.portfolio = {}
        self.load_portfolio()
        
    def load_portfolio(self):
        try:
            with open('portfolio.json', 'r') as f:
                self.portfolio = json.load(f)
        except FileNotFoundError:
            self.portfolio = {}
    
    def save_portfolio(self):
        with open('portfolio.json', 'w') as f:
            json.dump(self.portfolio, f, indent=4)
    
    def get_stock_data(self, symbol):
        base_url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if "Global Quote" in data:
                quote = data["Global Quote"]
                return {
                    'symbol': symbol,
                    'price': float(quote['05. price']),
                    'change': float(quote['09. change']),
                    'change_percent': quote['10. change percent']
                }
            else:
                print(f"Error fetching data for {symbol}: {data.get('Note', 'Unknown error')}")
                return None
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def add_stock(self, symbol, shares):
        if symbol in self.portfolio:
            print(f"{symbol} already in portfolio. Updating shares.")
            self.portfolio[symbol]['shares'] += shares
        else:
            stock_data = self.get_stock_data(symbol)
            if stock_data:
                self.portfolio[symbol] = {
                    'shares': shares,
                    'purchase_price': stock_data['price'],
                    'purchase_date': datetime.now().strftime("%Y-%m-%d")
                }
                print(f"Added {shares} shares of {symbol} to portfolio.")
        self.save_portfolio()
    
    def remove_stock(self, symbol, shares=None):
        if symbol in self.portfolio:
            if shares is None or shares >= self.portfolio[symbol]['shares']:
                del self.portfolio[symbol]
                print(f"Removed {symbol} from portfolio.")
            else:
                self.portfolio[symbol]['shares'] -= shares
                print(f"Removed {shares} shares of {symbol} from portfolio.")
            self.save_portfolio()
        else:
            print(f"{symbol} not found in portfolio.")
    
    def portfolio_summary(self):
        total_value = 0
        total_investment = 0
        print("\nPortfolio Summary:")
        print("-" * 50)
        print(f"{'Symbol':<10}{'Shares':<10}{'Price':<15}{'Value':<15}{'Gain/Loss':<15}")
        print("-" * 50)
        
        for symbol, data in self.portfolio.items():
            stock_data = self.get_stock_data(symbol)
            if stock_data:
                current_price = stock_data['price']
                value = data['shares'] * current_price
                investment = data['shares'] * data['purchase_price']
                gain_loss = value - investment
                gain_loss_pct = (gain_loss / investment) * 100 if investment != 0 else 0
                
                print(f"{symbol:<10}{data['shares']:<10}{current_price:<15.2f}"
                      f"{value:<15.2f}{gain_loss_pct:<15.2f}%")
                
                total_value += value
                total_investment += investment
        
        print("-" * 50)
        total_gain_loss = total_value - total_investment
        total_gain_loss_pct = (total_gain_loss / total_investment) * 100 if total_investment != 0 else 0
        
        print(f"\nTotal Portfolio Value: ${total_value:.2f}")
        print(f"Total Investment: ${total_investment:.2f}")
        print(f"Total Gain/Loss: ${total_gain_loss:.2f} ({total_gain_loss_pct:.2f}%)")
        
        return {
            'total_value': total_value,
            'total_investment': total_investment,
            'total_gain_loss': total_gain_loss,
            'total_gain_loss_pct': total_gain_loss_pct
        }
    
    def plot_portfolio(self):
        symbols = []
        values = []
        
        for symbol, data in self.portfolio.items():
            stock_data = self.get_stock_data(symbol)
            if stock_data:
                symbols.append(symbol)
                values.append(data['shares'] * stock_data['price'])
        
        if symbols:
            plt.figure(figsize=(10, 6))
            plt.pie(values, labels=symbols, autopct='%1.1f%%', startangle=140)
            plt.title('Portfolio Allocation')
            plt.axis('equal')
            plt.show()
        else:
            print("No stocks in portfolio to plot.")

def main():
    # Replace with your Alpha Vantage API key
    API_KEY = "YOUR_API_KEY"
    
    portfolio = StockPortfolio(API_KEY)
    
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio Summary")
        print("4. View Portfolio Allocation")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            symbol = input("Enter stock symbol: ").upper()
            try:
                shares = float(input("Enter number of shares: "))
                portfolio.add_stock(symbol, shares)
            except ValueError:
                print("Please enter a valid number for shares.")
        
        elif choice == "2":
            symbol = input("Enter stock symbol to remove: ").upper()
            shares_input = input("Enter number of shares to remove (leave blank to remove all): ")
            try:
                shares = float(shares_input) if shares_input else None
                portfolio.remove_stock(symbol, shares)
            except ValueError:
                print("Please enter a valid number for shares.")
        
        elif choice == "3":
            portfolio.portfolio_summary()
        
        elif choice == "4":
            portfolio.plot_portfolio()
        
        elif choice == "5":
            print("Exiting program.")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()





