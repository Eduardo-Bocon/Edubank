
class User:

    def __init__(self, person, password, balance=0, loanAmount=0):
        self.personInformation = person
        self.password = password
        self.balance = balance
        self.loanAmount = loanAmount
        self.history = TransactionsHistory()

    def deposit(self, quantity):
        self.balance = self.balance + quantity

    def draft(self, quantity):
        if self.balance >= quantity:
            self.balance = self.balance - quantity

    def getPassword(self):
        return self.password

    def setPassword(self, newPassword):
        self.password = newPassword

    def getBalance(self):
        return self.balance

    def getLoanAmount(self):
        return self.loanAmount

    def makeLoan(self, quantity):
        if quantity >=0:
            self.loanAmount = self.loanAmount + quantity
            self.balance = self.balance + quantity

    def payLoan(self, quantity):
        if quantity <= self.loanAmount and quantity <= self.balance and quantity >=0:
            self.loanAmount -= quantity
            self.balance -= quantity

    def transferTo(self, receiver, quantity):
        if self.balance >= quantity and quantity >= 0:
            self.balance -= quantity
            receiver.balance += quantity
            return True
        return False

class Person():
    def __init__(self, name, cpf):
        self.name = name
        self.cpf = cpf

    def getName(self):
        return self.name

    def setName(self, newName):
        self.name = newName

    def getCpf(self):
        return self.cpf

    def setCpf(self, newCpf):
        self.cpf = newCpf

class TransactionsHistory():
    def __init__(self):
        self.values = list()
        self.receivers = list()

    def newValue(self, value):
        self.values.append(value)

    def newReceiver(self, cpf):
        self.receivers.append(cpf)