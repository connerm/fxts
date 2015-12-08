class Position:

    def __init__(self, pair, direction, datetime, units):
        self.pair = pair
        self.direction = direction
        self.units = units

    def open(self, datetime, bid, ask):
        self.open_time = datetime
        self.open_bid = bid
        self.open_ask = ask
        print "OPEN@", datetime, self.direction, bid

    def close(self, datetime, bid, ask):
        self.close_time = datetime
        self.close_bid = bid
        self.close_ask = ask
        print "CLOSE@", datetime, self.direction, bid

    def calculate_profit(self):
        if self.direction == 'LONG':
           self.pips = self.close_bid - self.open_ask
        if self.direction == 'SHORT':
           self.pips =  self.open_bid - self.close_ask
        self.profit = self.pips*self.units
        return self.profit

    def __str__(self):
        return "Pair:%s Direction: %s Profit:%f Units:%f" % (self.pair, self.direction, self.profit, self.units)

