import sys
from datetime import datetime

LONG = 'long'
SHORT = 'short'

class Position: 
    def __init__(self):
        self.state = None

    def open_pos(self, symbol, open_price, direction, units):
        self.symbol = symbol
        self.open_price = open_price
	self.direction = direction
        self.units = units
	self.state = "open"

    def close_pos(self, close_price):
	self.close_price = close_price
	if self.direction == LONG:
           self.pips = self.close_price - self.open_price
        if self.direction == SHORT:
           self.pips =  self.open_price - self.close_price
        self.profit = self.pips*self.units
        self.state = "closed"

    def __str__(self):
        return "Position | Direction: %s Pips: %f Profit: %f" % (self.direction, self.pips, self.profit)

class Account():
    positions = []

    def __init__(self, balance, risk_percent):
        self.balance = balance
        self.risk_percent = risk_percent

    def settle(self, position):
        self.balance += position.profit

    def risk(self):
        stop_loss = 0.005
        trade_risk = self.balance * self.risk_percent
        units = trade_risk/stop_loss
        return units

    def __str__(self):
        return "Account balance: %s" % (self.balance)

class Signal():
    def __init__(self, order, direction, position):
        self.order = order
        self.direction = direction
        self.position = position
    def __str__(self):
        return "Signal: %s %s" % (self.order, self.direction)

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
    def __init__(self, _datetime, _open, _high, _low, _close):
        self._datetime = _datetime
        self._open = _open
        self._high = _high
        self._low = _low
        self._close = _close
    def __str__(self):
        return "%f %f %f %f" % (self._open, self._high, self._low, self._close)
        
    
def main():
    feed = Data(100)
    account = Account(1000,0.02)
    signals = []

    with open(sys.argv[1]) as f:
        
        #price loop    
        for line in f:
            line = line.split(";")
            _datetime = datetime.strptime(line[0], "%Y%m%d %H%M%S")
            line = [float(x) for x in line[1:]]

            #get bar
            bar = Bar(_datetime, line[0],line[1], line[2], line[3])
            print bar

            #update data 
            feed.add(bar)

            #execute
            execute(bar, account)
            
            #strategy
            strategy(bar, account)

        #print account.balances
        #print account.trades
            
def strategy(bar, account):
        
    #entery
    if account.positions == []:
        pos= Position
        sig1 = Signal('open', LONG, pos)
        print sig1
        account.signals.append(sig1)
        account.positions.append(pos)

    #exit
    for pos in account.positions:
        #check take and stops
        if pos.direction == LONG and pos.open_price > (bar._close - .005):
            sig = Signal('close', pos.direction, pos)
            print sig
            account.signals.append(sig)
            account.positions.remove(pos)
        if pos.direction == SHORT and pos.open_price < (bar._close - .005):
            sig = Signal('close', pos.direction)
        sig.position = pos
        account.signals.append(sig)


    return signals


def execute(bar, account):

    for signal in account.signals:

        #open
        if signal.order == 'open':
            pos = Position()
            account.positions.append(pos)
            units = account.risk()
            pos.open_pos(bar._close, signal.direction, units)
            signal.position = pos
            
        #close
        if signal.order == 'close':
            signal.position.close_pos(bar._close)
            account.settle(signal.position)
            print signal.position
            account.positions.remove(signal.position)
            print account
        
        account.signals.remove(signal)

if __name__ == '__main__':
    main()
