from Users.User import User


class Employee(User):
    interestRate = 3/100
    def __init__(self, person, password, balance=0, loan=0):
        super().__init__(person, password, balance, loan)

    def getInterestPerMonth(self):
        return self.loanAmount * self.interestRate

    def getInterestRate(self):
        return self.interestRate
