import sys
from datetime import datetime

LONG = 'LONG'
SHORT = 'SHORT'
OPEN = 'OPEN'
CLOSE = 'CLOSE'

class Position: 

    def __init__(self, pair, direction, datetime, price, units):
        self.pair = pair
	self.direction = direction
        self.open_time = datetime
        self.open_price = price
        self.units = units
	self.state = OPEN
        print "OPEN@   %s: Direction: %5s Price: %.4f Units: %.0f" % (self.open_time, self.direction, self.open_price, self.units)

    def close(self, datetime, price):
        self.close_time = datetime
        self.duration = self.close_time - self.open_time
	self.close_price = price
	if self.direction == LONG:
           self.pips = self.close_price - self.open_price
        if self.direction == SHORT:
           self.pips =  self.open_price - self.close_price
        self.profit = self.pips*self.units
        self.state = CLOSE
        print "CLOSE@  %s: Direction: %5s Price: %1.4f Pips: %2.4f Profit: %3.2f" % (self.close_time, self.direction, self.close_price, self.pips, self.profit)

class Account():
    positions = []

    def __init__(self, balance, risk_percent):
        self.balance = balance
        self.risk_percent = risk_percent

    def settle(self, position):
        self.balance += position.profit
        self.positions.remove(position)

    def risk(self):
        stop_loss = 0.0050
        trade_risk = self.balance * self.risk_percent
        units = trade_risk/stop_loss
        return units

    def __str__(self):
        return "Account balance: %s" % (self.balance)

class Signal():
    def __init__(self, pair, order_type, direction, datetime):
        self.pair = pair
        self.order_type = order_type
        self.direction = direction
        self.datetime = datetime
    def __str__(self):
        return "SIGNAL@ %s: %5s %5s %6s" % (self.datetime, self.order_type, self.direction, self.pair)

class Data():
    def __init__(self, length):
        self.data = []
        self.length = length
    def add(self, bar): 
        self.data.append(bar)
        if len(self.data) > self.length:
            self.data.pop(0)

class Bar():
    def __init__(self, datetime, open_, high, low, close):
        self.datetime = datetime
        self.open_ = open_
        self.high = high
        self.low = low
        self.close = close
    def __str__(self):
        return "%s %f %f %f %f" % (self.datetime, self.open_, self.high, self.low, self.close)
        
    
def main():
    feed = Data(100)
    account = Account(1000,0.02)
    signals = []

    with open(sys.argv[1]) as f:
        
        #price loop    
        for line in f:
            line = line.split(";")
            date = datetime.strptime(line[0], "%Y%m%d %H%M%S")
            line = [float(x) for x in line[1:]]

            #get bar
            bar = Bar(date, line[0],line[1], line[2], line[3])

            #update data 
            feed.add(bar)

            #execute
            signals = execute(bar, account, signals)
            
            #strategy
            signals = strategy(bar, account, signals)
            
def strategy(bar, account, signals):
    
    #entery
    if account.positions == []:
        sig = Signal('EURUSD', OPEN, LONG, bar.datetime)
        signals.append(sig)
        print sig

        sig2 = Signal('EURUSD', OPEN, SHORT, bar.datetime)
        signals.append(sig2)
        print sig2

    #exit
    for pos in account.positions:
        #stop loss
        if (pos.direction == LONG and bar.close < (pos.open_price - .005)) or \
           (pos.direction == SHORT and bar.close > (pos.open_price + .005)):
            sig = Signal(pos.pair, CLOSE, pos.direction, bar.datetime)
            signals.append(sig)
            print sig
        #take profit
        if (pos.direction == LONG and bar.close > (pos.open_price + .005)) or \
           (pos.direction == SHORT and bar.close < (pos.open_price - .005)):
            sig = Signal(pos.pair, CLOSE, pos.direction, bar.datetime)
            signals.append(sig)
            print sig
    
    return signals


def execute(bar, account, signals):

    for signal in signals:

        #open
        if signal.order_type == OPEN:
            units = account.risk()
            pos = Position(signal.pair, signal.direction, bar.datetime, bar.close, units)
            account.positions.append(pos)
            
        #close
        if signal.order_type == CLOSE:
            for pos in account.positions:
                if signal.pair == pos.pair and signal.direction == pos.direction:
                    pos.close(bar.datetime, bar.close)
                    account.settle(pos)
                    print account 
    return []

if __name__ == '__main__':
    main()
