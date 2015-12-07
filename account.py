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
