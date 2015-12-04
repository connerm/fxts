import sys
from datetime import datetime

LONG = 'long'
SHORT = 'short'
OPEN = 'open'
CLOSE = 'close'

class Account():
    positions = []

    def __init__(self, balance, risk_percent):
        self.balance = balance
        self.risk_percent = risk_percent

    def settle(self, position):
        self.balance += position.profit

    def risk(self):
        stop_loss = 0.0050
        trade_risk = self.balance * self.risk_percent
        units = trade_risk/stop_loss
        return units

    def __str__(self):
        return "Account balance: %s" % (self.balance)

class Position: 
    def __init__(self, pair, datetime, direction, units, open_price):
        self.pair = pair
        self.datetime = datetime
	self.direction = direction
        self.units = units
        self.open_price = open_price
        print "OPEN: Direction: %s Price: %f Units: %f" % (self.direction, self.open_price, self.units)

    def close(self, datetime, close_price):
        self.datetime = datetime
	self.close_price = close_price
	if self.direction == LONG:
           self.pips = self.close_price - self.open_price
        if self.direction == SHORT:
           self.pips =  self.open_price - self.close_price
        self.profit = self.pips*self.units
        print "CLOSE: Direction: %s Price: %f Pips: %f Profit: %f" % (self.direction, self.close_price, self.pips, self.profit)

class Signal():
    def __init__(self, pair, datetime, order_type, direction):
        self.pair = pair
        self.datetime = datetime
        self.order_type = order_type
        self.direction = direction
    def __str__(self):
        return "Signal: %s %s %s" % (self.order_type, self.direction, self.pair)

class Order()
    def __init__(self, datetime, signal, price, account):
        self.pair = signal.pair
        self.datetime = datetime
        self.order_type = signal.order_type
        self.price = price
        self.direction = signal.direction
        self.units = account.risk()

    def execute(self):
        #exectue Order
        #return pos
        
class Bar():
    def __init__(self, datetime_, open_, high, low, close):
        self.datetime_ = datetime_
        self.open_ = open_
        self.high = high
        self.low = low
        self.close = close
    def __str__(self):
        return "%s %f %f %f %f" % (self.datetime_, self.open_, self.high, self.low, self.close)
        
class Tick()
    def __init__(self, datetime, bid, ask):
        self.datetime = datetime
        self.bid = bid
        self.ask = ask

class Data():
    def __init__(self, length):
        self.data = []
        self.length = length
    def add(self, bar): 
        self.data.append(bar)
        if len(self.data) > self.length:
            self.data.pop(0)

def main():
    feed = Data(100)
    account = Account(1000,0.02)
    signals = []
    orders = []

    with open(sys.argv[1]) as f:
        
        #price loop    
        for line in f:
            line = line.split(";")
            datetime_ = datetime.strptime(line[0], "%Y%m%d %H%M%S")
            line = [float(x) for x in line[1:]]

            #get bar
            bar = Bar(datetime_, line[0],line[1], line[2], line[3])

            #update data 
            feed.add(bar)

            #execute
            signals = execute(bar, account, signals)
            
            #strategy
            signals = strategy(bar, account, signals)
            
def strategy(bar, account, signals):
    
    #entery
    if account.positions == []:
        sig = Signal('EURUSD', OPEN, LONG)
        signals.append(sig)
        print sig

        sig2 = Signal('EURUSD', OPEN, SHORT)
        signals.append(sig2)
        print sig2

    #exit
    for pos in account.positions:
        #check take and stops
        if (pos.direction == LONG and bar.close < (pos.open_price - .005)) or \
           (pos.direction == SHORT and bar.close > (pos.open_price + .005)):
            sig = Signal(pos.pair, CLOSE, pos.direction)
            signals.append(sig)
            print sig
        if (pos.direction == LONG and bar.close > (pos.open_price + .005)) or \
           (pos.direction == SHORT and bar.close < (pos.open_price - .005)):
            sig = Signal(pos.pair, CLOSE, pos.direction)
            signals.append(sig)
            print sig
    
    return signals


def execute(bar, account, signals):

    for signal in signals:
        #make order
        order = Order( datetime, signal, price, account)
    return []

if __name__ == '__main__':
    main()
