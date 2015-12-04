import sys
from datetime import datetime

LONG = 'long'
SHORT = 'short'
OPEN = 'open'
CLOSE = 'close'

class Position: 
    def __init__(self):
        self.state = None

    def open_pos(self, pair, open_price, direction, units):
        self.pair = pair
        self.open_price = open_price
	self.direction = direction
        self.units = units
	self.state = OPEN
        print "OPEN: Direction: %s Price: %f Units: %f" % (self.direction, self.open_price, self.units)

    def close_pos(self, close_price):
	self.close_price = close_price
	if self.direction == LONG:
           self.pips = self.close_price - self.open_price
        if self.direction == SHORT:
           self.pips =  self.open_price - self.close_price
        self.profit = self.pips*self.units
        self.state = CLOSE
        print "CLOSE: Direction: %s Price: %f Pips: %f Profit: %f" % (self.direction, self.close_price, self.pips, self.profit)

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

class Signal():
    def __init__(self, pair, order_type, direction):
        self.pair = pair
        self.order_type = order_type
        self.direction = direction
    def __str__(self):
        return "Signal: %s %s %s" % (self.order_type, self.direction, self.pair)

'''
class Order()
    def __init__(self, signal):
        self.signal
'''

class Data():
    def __init__(self, length):
        self.data = []
        self.length = length
    def add(self, bar): 
        self.data.append(bar)
        if len(self.data) > self.length:
            self.data.pop(0)

class Bar():
    def __init__(self, datetime_, open_, high, low, close):
        self.datetime_ = datetime_
        self.open_ = open_
        self.high = high
        self.low = low
        self.close = close
    def __str__(self):
        return "%f %f %f %f" % (self.open_, self.high, self.low, self.close)
        
    
def main():
    feed = Data(100)
    account = Account(1000,0.02)
    signals = []

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

        #open
        if signal.order_type == OPEN:
            pos = Position()
            account.positions.append(pos)
            units = account.risk()
            pos.open_pos(signal.pair , bar.close, signal.direction, units)
            signals.remove(signal)
            
        #close
        if signal.order_type == CLOSE:
            for pos in account.positions:
                if signal.pair == pos.pair and signal.direction == pos.direction:
                    pos.close_pos(bar.close)
                    account.settle(pos)
                    account.positions.remove(pos)
                    signals.remove(signal)
                    print account
        
    return signals

if __name__ == '__main__':
    main()
