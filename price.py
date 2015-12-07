class Event(object):
    pass

class Bar(Event):
    def __init__(self, paird, datetime, open_, high, low, close):
        self.event_type = 'BAR'
        self.pair = pair
        self.datetime = datetime
        self.open_ = open_
        self.high = high
        self.low = low
        self.close = close
    def __str__(self):
        return "BAR@%s %f %f %f %f" % (self.datetime, self.open_, self.high, self.low, self.close)

class Tick(Event):
    def __init__(self, pair, datetime, bid, ask):
        self.event_type = 'TICK'
        self.pair = pair
        self.datetime = datetime
        self.bid = bid
        self.ask = ask
    def __str__(self):
        return "TICK@%s %f %f" % (self.datetime, self.bid, self.ask)

class Signal(Event):
    def __init__(self, pair, order_type, direction, datetime):
        self.event_type = 'SIGNAL'
        self.pair = pair
        self.order_type = order_type
        self.direction = direction
        self.datetime = datetime
    def __str__(self):
        return "SIGNAL@ %s: %5s %5s %6s" % (self.datetime, self.order_type, self.direction, self.pair)
