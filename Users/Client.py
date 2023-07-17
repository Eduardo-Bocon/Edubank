from Users.User import User


class Client(User):

    standardInterestRate = 3.5 / 100

    def __init__(self, person, password, balance=0, loanAmount=0):
        super().__init__(person, password, balance, loanAmount)
        self.loanAmount = loanAmount

    def getRank(self):
        if self.balance >= 1000000 and self.loanAmount <= 100000:
            return "A"
        elif self.balance >= 100000 and self.loanAmount <= 10000:
            return "B"
        else:
            return "C"

    def getInterestPerMonth(self):
        return self.loanAmount*self.getInterestRate()

    def getInterestRate(self):
        if self.getRank() == "A":
            return self.standardInterestRate - 0.8/100
        elif self.getRank() == "B":
            return self.standardInterestRate - 0.5/100
        elif self.getRank() == "C":
            return self.standardInterestRate
