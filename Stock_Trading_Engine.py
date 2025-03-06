# Limits for our trading system
MAX_TICKERS = 1024  # We can have 1024 different stocks
MAX_ORDERS = 10000  # We can handle up to 10,000 orders

# Order types (just numbers)
BUY = 1    # 1 means Buy
SELL = 2   # 2 means Sell

# A box to hold one order’s info
class OrderNode:
    def __init__(self, order_type, ticker, quantity, price):
        self.type = order_type    # 1 for Buy, 2 for Sell
        self.ticker = ticker      # Stock number (0-1023)
        self.quantity = quantity  # How many shares
        self.price = price        # Price per share
        self.next = 0             # Next order in line (0 means none)

# The main trading system
class StockTradingEngine:
    def __init__(self):
        # Big list with 1024 slots, one for each stock
        # Each slot holds Buy and Sell lists
        self.tickers = [0] * MAX_TICKERS
        self.order_count = 0    # Total number of orders
        self.busy = 0           # 0 means free, 1 means in use

    # Add a new order
    def addOrder(self, order_type, ticker, quantity, price):
        # Check if the order is okay
        if ticker >= MAX_TICKERS:
            print("Error: Stock number too high!")
            return 0
        if quantity <= 0:
            print("Error: Need more than 0 shares!")
            return 0
        if price <= 0:
            print("Error: Price must be more than 0!")
            return 0
        if self.order_count >= MAX_ORDERS:
            print("Error: Too many orders!")
            return 0

        # Wait if someone else is using it
        while self.busy == 1:
            pass  # Just wait
        self.busy = 1  # Our turn now

        # Get the Buy and Sell lists for this stock
        slot = self.tickers[ticker]
        if slot == 0:
            buy_list = 0
            sell_list = 0
        else:
            buy_list = slot[0]
            sell_list = slot[1]

        # Make the new order
        new_order = OrderNode(order_type, ticker, quantity, price)

        # Add it to the right list
        if order_type == BUY:
            # Put Buy orders with highest price first
            if buy_list == 0 or buy_list.price < price:
                new_order.next = buy_list
                buy_list = new_order
            else:
                last = buy_list
                next_one = buy_list.next
                while next_one != 0 and next_one.price >= price:
                    last = next_one
                    next_one = next_one.next
                new_order.next = next_one
                last.next = new_order
        else:  # SELL
            # Put Sell orders with lowest price first
            if sell_list == 0 or sell_list.price > price:
                new_order.next = sell_list
                sell_list = new_order
            else:
                last = sell_list
                next_one = sell_list.next
                while next_one != 0 and next_one.price <= price:
                    last = next_one
                    next_one = next_one.next
                new_order.next = next_one
                last.next = new_order

        # Save the updated lists
        self.tickers[ticker] = (buy_list, sell_list)
        self.order_count = self.order_count + 1

        # Try to match it with other orders
        self.matchOrder(ticker)

        # Done, let others use it
        self.busy = 0
        return 1

    # Match Buy and Sell orders for a stock
    def matchOrder(self, ticker):
        slot = self.tickers[ticker]
        if slot == 0:
            return  # Nothing to match

        buy_list = slot[0]  # Buy orders
        sell_list = slot[1] # Sell orders

        # Match as long as we have both Buy and Sell
        while buy_list != 0 and sell_list != 0:
            if buy_list.price >= sell_list.price:  # Good deal?
                shares = buy_list.quantity
                if sell_list.quantity < shares:
                    shares = sell_list.quantity  # Use smaller amount
                print("Match:", shares, "shares of stock", ticker, "at", sell_list.price)
                buy_list.quantity = buy_list.quantity - shares
                sell_list.quantity = sell_list.quantity - shares
                if buy_list.quantity == 0:
                    buy_list = buy_list.next  # Move to next Buy
                if sell_list.quantity == 0:
                    sell_list = sell_list.next  # Move to next Sell
                self.tickers[ticker] = (buy_list, sell_list)
            else:
                break  # No more matches possible

# Simple manual simulation with clear examples
def run_simulation():
    engine = StockTradingEngine()
    print("Starting a simple trading example...")

    # Add some easy-to-follow orders
    print("Adding: Buy 10 shares of stock 0 at 50")
    engine.addOrder(BUY, 0, 10, 50)  # Someone wants to buy 10 shares at $50

    print("Adding: Sell 5 shares of stock 0 at 45")
    engine.addOrder(SELL, 0, 5, 45)  # Someone sells 5 shares at $45 (matches with Buy at 50)

    print("Adding: Buy 8 shares of stock 1 at 60")
    engine.addOrder(BUY, 1, 8, 60)  # Buy for a different stock

    print("Adding: Sell 10 shares of stock 1 at 55")
    engine.addOrder(SELL, 1, 10, 55)  # Sell that matches the Buy at 60

    print("Adding: Sell 15 shares of stock 0 at 48")
    engine.addOrder(SELL, 0, 15, 48)  # Sell more of stock 0, matches remaining Buy

    print("Simulation done! All matches are shown above.")

# Run the simple example
run_simulation()