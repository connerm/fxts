import sys
from datetime import datetime, timedelta

from account import Account
from price import Tick, Bar, Signal
from position import Position
from data import Data

LONG = 'LONG'
SHORT = 'SHORT'
OPEN = 'OPEN'
CLOSE = 'CLOSE'
    
def main():
    feed = Data(60*30)
    account = Account(1000,0.02)
    signals = []

    with open(sys.argv[1]) as f:
        
        #price loop    
        for line in f:
            line = line.split(";")
            date = datetime.strptime(line[0], "%Y%m%d %H%M%S")
            line = [float(x) for x in line[1:]]

            #get tick
            tick = Tick('EURUSD', date, line[3],line[3])

            #update data 
            feed.add(tick.bid)

            #execute
            signals = execute(tick, account, signals)
            
            #strategy
            signals = generate_signals(tick, account, feed, signals)
            
def generate_signals(tick, account, feed, signals):
    
    #entery
    if account.positions == []:
        sig = Signal('EURUSD', OPEN, LONG, tick.datetime)
        signals.append(sig)
        print sig

        sig2 = Signal('EURUSD', OPEN, SHORT, tick.datetime)
        signals.append(sig2)
        print sig2

    #exit
    for pos in account.positions:
        #stop loss
        if (pos.direction == LONG and tick.bid < (pos.open_ask - .005)) or \
           (pos.direction == SHORT and tick.ask > (pos.open_bid + .005)):
            sig = Signal(pos.pair, CLOSE, pos.direction, tick.datetime)
            signals.append(sig)
            print sig
        #take profit
        if (pos.direction == LONG and tick.bid > (pos.open_ask + .005)) or \
           (pos.direction == SHORT and tick.ask < (pos.open_bid - .005)):
            sig = Signal(pos.pair, CLOSE, pos.direction, tick.datetime)
            signals.append(sig)
            print sig
    
    return signals


def execute(tick, account, signals):

    #create positions
    for signal in signals:

        #open
        if signal.order_type == OPEN:
            units = account.risk()
            pos = Position(signal.pair, signal.direction, tick.datetime, units)
            pos.open(tick.datetime, tick.bid, tick.ask)
            account.positions.append(pos)
            
        #close
        if signal.order_type == CLOSE:
            for pos in account.positions:
                if signal.pair == pos.pair and signal.direction == pos.direction:
                    pos.close(tick.datetime, tick.bid, tick.ask)
                    pos.calculate_profit()
                    print pos
                    account.settle(pos)
                    print account 
    return []

if __name__ == '__main__':
    main()
