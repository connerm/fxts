import sys
import time

LONG = 'long'
SHORT = 'short'

class Position: 
    def __init__(self):
        self.state = None

    def open_pos(self, bid, ask, direction, units):
	self.open_bid = bid
	self.open_ask = ask
	self.direction = direction
        self.units = units
	self.state = "open"

    def close_pos(self, bid, ask):
	self.close_bid = bid
	self.close_ask = ask
	if self.direction == LONG:
           self.pips = self.close_bid - self.open_ask
        if self.direction == SHORT:
           self.pips = self.open_bid - self.close_ask
        self.profit = self.pips*self.units
        self.state = "closed"

    def __str__(self):
        return "Position | Direction: %s Pips: %f Profit: %f" % (self.direction, self.pips, self.profit)

class Account():
    positions = []

    def __init__(self, balance, risk_percent):
        self.balance = self.initial = self.high = self.low = balance
        self.risk_percent = risk_percent

    def settle(self, position):
        self.balance += position.profit
        if self.balance > self.high: self.high = self.balance
        if self.balance < self.low: self.low = self.balance

    def risk(self):
        stop_loss = 0.005
        trade_risk = self.balance * self.risk_percent
        units = trade_risk/stop_loss
        return units

    def __str__(self):
        return "Account balance: %s" % (self.balance)

class Signal():
    def __init__(self, position, order, direction):
        self.position = position
        self.order = order
        self.direction = direction
    def __str__(self):
        return "Signal: %s %s" % (self.order, self.direction)

class Data():
    def __init__(self, length):
        self.data = []
        self.length = length
    def update(self, bid, ask): 
        self.data.append((bid,ask))
        if len(self.data) > self.length:
            self.data.pop(0)
    
def main():
    feed = Data(100)
    account = Account(1000,0.02)
    signals = []

    with open(sys.argv[1]) as f:
        
        #price loop    
        for line in f:
            line = line.split(",")

            #bid and ask
            bid = float(line[1])
            ask = float(line[2])

            #update data 
            feed.update(bid, ask)

            #execute
            for signal in signals:
                execute(bid, ask, account, signal)
            signals = []
            
            #strategy
            signals = strategy(bid, ask, account, feed)

def strategy(bid, ask, account, feed):
    signals = []
    
    #calculate     
    sma10 = sum(feed.data[:10][0])/10
    sma100 = sum(feed.data[0])/100

    #entery
    if sma10 > sma100:

        pos1 = Position()
        account.positions.append(pos1)
        sig1 = Signal(pos1, 'open', LONG)
        print sig1
        signals.append(sig1)

    if sma10 < sma100:
        pos2 = Position()
        account.positions.append(pos2)
        sig2 = Signal(pos2, 'open', SHORT)
        print sig2
        signals.append(sig2)

    #exit
    for pos in account.positions:
        if pos.state == 'open':
            #check take and stops
            sig = Signal(pos, 'close', pos.direction)
            print sig
            signals.append(sig)

    return signals


def execute(bid, ask, account, signal):
    #open
    if signal.order == 'open':
        units = account.risk()
        signal.position.open_pos(bid, ask, signal.direction, units)

    #close
    if signal.order == 'close':
        signal.position.close_pos(bid, ask)
        account.settle(signal.position)
        print signal.position
        account.positions.remove(signal.position)
        print account
        
if __name__ == '__main__':
    main()