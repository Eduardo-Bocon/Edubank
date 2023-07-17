# Feito por Eduardo Boçon 23103123

import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import csv
from Design import Colors
from Users.Client import Client
from Users.Employee import Employee
import atexit
from Users.User import Person

# Tamanho da janela
windWidth = 1920
windHeight = 1080

# lista com objetos cliente
users_data = []

# Index do cliente logado na lista de clientes
loggedUserIndex = 0

def newLoggedClient(client):
    global loggedUserIndex
    loggedUserIndex = users_data.index(client)

def getUsers():

    with open('usersData.csv', 'r', newline='') as file_csv:

        reader_csv = csv.reader(file_csv)
        for line in file_csv:
            if line != None:
                name_data, cpf_data, password_data, userType_data, balance_data, loan_data = line.split(",")
                balance_data = float(balance_data)
                loan_data = float(loan_data[:-2])  # o fim de linha vem com um '\r' e um '\n' no final
                if userType_data == '1':
                    person = Person(name_data, cpf_data)
                    users_data.append(Employee(person, password_data, balance=balance_data, loan=loan_data))
                elif userType_data == '0':
                    person = Person(name_data, cpf_data)
                    users_data.append(Client(person, password_data, balance=balance_data, loanAmount=loan_data))

def getTransactions():
    with open('transactionsData.csv', 'r', newline='') as file_csv:

        reader_csv = csv.reader(file_csv)
        for line in file_csv:
            if line != None:
                sender_data, value_data, receiver_data = line.split(",")
                value_data = float(value_data)
                receiver_data = receiver_data[:-2]  # o fim de linha vem com um '\r' e um '\n' no final
            for user in users_data:
                if user.personInformation.getCpf() == sender_data:
                    user.history.newValue(value_data)
                    user.history.newReceiver(receiver_data)

# Salvar os dados no fim do programa
def saveData():
    with open('usersData.csv', 'w', newline='') as file_csv:

        writer = csv.writer(file_csv)
        for user in users_data:
            userType = 0
            if isinstance(user, Employee):
                userType = 1;
            writer.writerow([user.personInformation.getName(),user.personInformation.getCpf(), user.getPassword(), userType, user.getBalance(), user.getLoanAmount()])
    with open('transactionsData.csv', 'w', newline='') as file_csv:

        writer = csv.writer(file_csv)
        for user in users_data:
            for i in range(len(user.history.values)):
                writer.writerow([user.personInformation.getCpf(), user.history.values[i],user.history.receivers[i]])

atexit.register(saveData)

def goToLoginWindow():

    # Definições da janela de login
    loginWindow = tk.Tk()
    loginWindow.title("EduBank")
    loginWindow.geometry(f"{windWidth}x{windHeight}")
    loginWindow.minsize(windWidth, windHeight)
    loginWindow.configure(bg=Colors.pinkishRed)

    # icone
    icon = "Design/bird icon2.ico"
    loginWindow.iconbitmap(default=icon)

    def tryLogin():
        wrongPasswordLabel.place_forget()
        userNotFoundLabel.place_forget()
        username = usernameEntry.get()
        password = passwordEntry.get()
        userExist = False
        for client in users_data:
            if client.personInformation.getName() == username or client.personInformation.getCpf() == username:
                userExist = True
                if client.getPassword() == password:
                    newLoggedClient(client)
                    loginWindow.destroy()
                    goToMainWindow()
                else:
                    wrongPasswordLabel.place(relx=0.65, y=650, anchor="center")
        if not userExist:
            userNotFoundLabel.place(relx=0.68, y=500, anchor="center")

    def fromLoginToRegister():
        loginWindow.destroy()
        goToRegisterWindow()

    #Entrada do usuario
    charLimit = 20
    usernameEntry = tk.Entry(loginWindow, width=charLimit, font=("Segoe UI", 23))
    passwordEntry = tk.Entry(loginWindow, width=charLimit, show="*", font=("Segoe UI", 23))

    loginButton = tk.Button(loginWindow, text="Login", padx=60, pady=20, command=tryLogin, activebackground=Colors.lightGrey)
    registerButton = tk.Button(loginWindow, text="Cadastrar", padx=55, pady=20, command=fromLoginToRegister, activebackground=Colors.lightGrey)

    usernameLabel = tk.Label(loginWindow, text="Nome ou CPF:", font=("Segoe UI", 20),bg=Colors.pinkishRed, fg=Colors.white)
    passwordLabel = tk.Label(loginWindow, text="Senha:", font=("Segoe UI", 20),bg=Colors.pinkishRed, fg=Colors.white)
    wrongPasswordLabel = tk.Label(loginWindow, text="Senha invalida", font=("Segoe UI", 20), bg=Colors.pinkishRed, fg=Colors.white)
    userNotFoundLabel = tk.Label(loginWindow, text="Usuario não encontrado", font=("Segoe UI", 20), bg=Colors.pinkishRed, fg=Colors.white)

    birdImage = Image.open("Design/bird icon.png")
    birdImage_tk = ImageTk.PhotoImage(birdImage)
    birdImage_Label = tk.Label(loginWindow, image=birdImage_tk, borderwidth=0)

    usernameLabel.place(relx=0.5, y=450, anchor="center")
    usernameEntry.place(relx=0.5, y=500, anchor="center")
    passwordLabel.place(relx=0.5, y=600, anchor="center")
    passwordEntry.place(relx=0.5, y=650, anchor="center")

    loginButton.place(relx=0.5, y=800, anchor="center")
    registerButton.place(relx=0.5, y = 900, anchor="center")
    birdImage_Label.place(relx=0.5, y=200, anchor="center")

    #loop principal
    loginWindow.mainloop()


def goToRegisterWindow():

    # Definições da janela de cadastro
    registerWindow = tk.Tk()
    registerWindow.title("EduBank")
    registerWindow.geometry(f"{windWidth}x{windHeight}")
    registerWindow.minsize(windWidth, windHeight)
    registerWindow.configure(bg=Colors.pinkishRed)

    def newRegister():
        if nameRegEntry.get() != "" and cpfRegEntry.get() != "" and passwordRegEntry.get() != "":
            name = nameRegEntry.get()
            cpf = cpfRegEntry.get()
            password = passwordRegEntry.get()

            # limpa a tela
            for widget in registerWindow.winfo_children():
                widget.destroy()

            users_data.append(Client(Person(name,cpf), password))
            #avisa que deu certo o cadastro
            successfulRegLabel = tk.Label(registerWindow, text="Cadastro concluido!", font=("Segoe UI", 25), bg=Colors.pinkishRed, fg=Colors.white)
            successfulRegLabel.place(relx=0.5, rely=0.5, anchor="center")
            registerWindow.update()
            time.sleep(3)

            registerWindow.destroy()
            goToLoginWindow()

    def fromRegisterToLogin():
        registerWindow.destroy()
        goToLoginWindow()

    # Entrada do usuario
    charLimit = 20
    nameRegEntry = tk.Entry(registerWindow, width=charLimit, font=("Segoe UI", 23))
    cpfRegEntry = tk.Entry(registerWindow, width=charLimit, font=("Segoe UI", 23))
    passwordRegEntry = tk.Entry(registerWindow, width=charLimit, show="*", font=("Segoe UI", 23))

    nameRegLabel = tk.Label(registerWindow, text="Nome:", font=("Segoe UI", 20), bg=Colors.pinkishRed, fg=Colors.white)
    cpfRegLabel = tk.Label(registerWindow, text="CPF:", font=("Segoe UI", 20), bg=Colors.pinkishRed, fg=Colors.white)
    passwordRegLabel = tk.Label(registerWindow, text="Senha:", font=("Segoe UI", 20), bg=Colors.pinkishRed, fg=Colors.white)

    registerButton = tk.Button(registerWindow, text="Cadastrar", padx=55, pady=20, command=newRegister, activebackground=Colors.lightGrey)
    loginButton = tk.Button(registerWindow, text="Login", padx=55, pady=20, command=fromRegisterToLogin, activebackground=Colors.lightGrey)

    nameRegLabel.place(relx=0.5, y=300, anchor="center")
    nameRegEntry.place(relx=0.5, y=350, anchor="center")
    cpfRegLabel.place(relx=0.5, y=450, anchor="center")
    cpfRegEntry.place(relx=0.5, y=500, anchor="center")
    passwordRegLabel.place(relx=0.5, y=600, anchor="center")
    passwordRegEntry.place(relx=0.5, y=650, anchor="center")
    registerButton.place(relx=0.5, y=800, anchor="center")
    loginButton.place(relx=0.5, y=900, anchor="center")


def goToMainWindow():

    def updateValues():
        loanQuantityLoanLabel.config(text="Divida: R$ {:.2f}".format(users_data[loggedUserIndex].getLoanAmount()))
        loanQuantityOverLabel.config(text="Divida: R$ {:.2f}".format(users_data[loggedUserIndex].getLoanAmount()))
        balanceOverLabel.config(text="Saldo: R$ {:.2f}".format(users_data[loggedUserIndex].getBalance()))
        balanceDeposit_DraftLabel.config(text="Saldo: R$ {:.2f}".format(users_data[loggedUserIndex].getBalance()))
        interestRate_DraftLabel.config(text="Taxa de juros: {:.2f}%".format(users_data[loggedUserIndex].getInterestRate() * 100))
        interestPerMonth_DraftLabel.config(text="Juros neste mês: R$ {:.2f}".format(
        users_data[loggedUserIndex].getInterestPerMonth()))
        printHistory()
        if isinstance(users_data[loggedUserIndex], Employee):
            reloadUserList()

    # Definições da janela principal
    mainWindow = tk.Tk()
    mainWindow.title("EduBank")
    mainWindow.geometry(f"{windWidth}x{windHeight}")
    mainWindow.minsize(windWidth, windHeight)
    mainWindow.configure(bg=Colors.pinkishRed)

    style = ttk.Style()
    style.configure("My.TNotebook", background=Colors.pinkishRed)

    tabs = ttk.Notebook(mainWindow, style="My.TNotebook")
    tabs.place(x=0,y=0,width=windWidth,height=windHeight)

    # Aba Geral
    overview_tab = ttk.Frame(tabs)
    tabs.add(overview_tab,text="Geral")
    # interface da aba de visão geral da conta
    nameOverLabel = tk.Label(overview_tab, text=users_data[loggedUserIndex].personInformation.getName(), font=("Segoe UI Bold", 40), fg=Colors.pinkishRed)
    balanceOverLabel = tk.Label(overview_tab, text="Saldo: R$ {:.2f}".format(users_data[loggedUserIndex].getBalance()), font=("Segoe UI Bold", 40),fg=Colors.pinkishRed)
    loanQuantityOverLabel= tk.Label(overview_tab, text="Divida: R$ {:.2f}".format(float(users_data[loggedUserIndex].getLoanAmount())), font=("Segoe UI Bold", 40), fg=Colors.pinkishRed)
    profileImage = Image.open("Design/profileIcon.png")
    profileImage = profileImage.resize((400, 400))
    profileImage_tk = ImageTk.PhotoImage(profileImage)
    profileImage_Label = tk.Label(overview_tab, image=profileImage_tk, borderwidth=0)

    nameOverLabel.place(relx=0.35,rely=0.15)
    balanceOverLabel.place(relx=0.35, rely=0.30)
    loanQuantityOverLabel.place(relx=0.35, rely=0.45)
    profileImage_Label.place(relx=0.15,rely=0.3, anchor="center")

    # Aba Transferencia
    transfer_tab = ttk.Frame(tabs)
    tabs.add(transfer_tab, text="Transferência")

    receiverIndex = -1

    def showReceiver():
        global receiverIndex
        receiverIndex = -1
        for client in users_data:
            if client.personInformation.getName() == receiver_TransferEntry.get() or client.personInformation.getCpf() == receiver_TransferEntry.get():
                receiverData_TransferLabel.config(text="Dados do destinatario\nNome: {} \nCPF: {}".format(client.personInformation.getName(), client.personInformation.getCpf()))
                receiverIndex = users_data.index(client)
        if receiverIndex == -1:
            receiverData_TransferLabel.config(
                text="Usuario não encontrado")

    def makeTransfer():

        def hideTransfer():
            confirmedTransfer_TransferLabel.place_forget()

        global receiverIndex
        quantity = float(transferQuantity_TransferEntry.get())
        if receiverIndex >= 0:
            transferMade = users_data[loggedUserIndex].transferTo(users_data[receiverIndex], quantity)
            if transferMade:

                # salva no historico de quem enviou
                users_data[loggedUserIndex].history.newValue(quantity*-1)
                users_data[loggedUserIndex].history.newReceiver(users_data[receiverIndex].personInformation.getCpf())

                confirmedTransfer_TransferLabel.place(relx=0.5, rely=0.8, anchor="n")
                confirmedTransfer_TransferLabel.after(2500, hideTransfer)
                updateValues()


    receiver_TransferLabel = tk.Label(transfer_tab, text="Nome/CPF do destinatario:", font=("Segoe UI Bold", 40), fg=Colors.pinkishRed)
    receiverData_TransferLabel = tk.Label(transfer_tab, text="Dados do destinatario\nNome: {} \nCPF: {}".format("", ""), font=("Segoe UI Bold", 40), fg=Colors.pinkishRed)
    confirmedTransfer_TransferLabel = tk.Label(transfer_tab, text="Transferência concluida", font=("Segoe UI Bold", 40), fg=Colors.pinkishRed)
    receiver_TransferEntry = tk.Entry(transfer_tab, width=11, font=("Segoe UI", 30))
    transferQuantity_TransferEntry = tk.Entry(transfer_tab, width=11, font=("Segoe UI", 30))
    searchReceiver_TransferButton = tk.Button(transfer_tab, text="Procurar", padx=60, pady=20, command=showReceiver, fg=Colors.white,
                               background=Colors.pinkishRed, activebackground=Colors.lightGrey)
    transfer_TransferButton = tk.Button(transfer_tab, text="Transferir", padx=60, pady=20, command=makeTransfer, fg=Colors.white,
                               background=Colors.pinkishRed, activebackground=Colors.lightGrey)

    receiver_TransferLabel.place(relx=0.25, rely=0.2, anchor="n")
    receiverData_TransferLabel.place(relx=0.7, rely=0.2, anchor="n")
    receiver_TransferEntry.place(relx=0.1, rely=0.35)
    searchReceiver_TransferButton.place(relx=0.3, rely=0.35)
    transferQuantity_TransferEntry.place(relx=0.4, rely=0.6)
    transfer_TransferButton.place(relx=0.55, rely=0.6)

    # Aba Histórico de Transferencias
    history_tab = ttk.Frame(tabs)
    tabs.add(history_tab, text="Histórico de Transferências")

    def printHistory():

        transfer_treeview = ttk.Treeview(history_tab, columns=("Pessoa", "Valor"), show="headings")
        transfer_treeview.configure(height=30)
        transfer_treeview.heading("Pessoa", text="Pessoa")
        transfer_treeview.heading("Valor", text="Valor")
        transfer_treeview.place(y=150, relx=0.5, anchor="n")

        # printa as transferencias negativas
        transfer_treeview.insert("", "end", values=("Enviou", ""))
        for i in range(len(users_data[loggedUserIndex].history.values)):
            transfer_treeview.insert("", "end", values=(
                users_data[loggedUserIndex].history.receivers[i], users_data[loggedUserIndex].history.values[i]))


        # printa as transferencias positivas
        transfer_treeview.insert("", "end")
        transfer_treeview.insert("", "end",values=("Recebeu", ""))
        for user in users_data:
            if user.personInformation.getCpf() != users_data[loggedUserIndex].personInformation.getCpf():
                for i in range(len(user.history.values)):
                    if user.history.receivers[i] == users_data[loggedUserIndex].personInformation.getCpf():
                        transfer_treeview.insert("", "end", values=(user.personInformation.getCpf(), user.history.values[i]*-1))

    printHistory()


    # Aba Emprestimo
    loan_tab = ttk.Frame(tabs)
    tabs.add(loan_tab, text="Emprestimo")

    def makeLoan():
        users_data[loggedUserIndex].makeLoan(float(makeLoanEntry.get()))
        updateValues()

    def payLoan():
        users_data[loggedUserIndex].payLoan(float(makeLoanEntry.get()))
        updateValues()

    loanQuantityLoanLabel= tk.Label(loan_tab, text="Divida: R$ {:.2f}".format(float(users_data[loggedUserIndex].getLoanAmount())), font=("Segoe UI Bold", 40), fg=Colors.pinkishRed)
    interestRate_DraftLabel = tk.Label(loan_tab, text="Taxa de juros: {:.2f}%".format(users_data[loggedUserIndex].getInterestRate()*100),
                                       font=("Segoe UI Bold", 40), fg=Colors.pinkishRed)
    interestPerMonth_DraftLabel = tk.Label(loan_tab, text="Juros neste mês: R$ {:.2f}".format(
        users_data[loggedUserIndex].getInterestPerMonth()),
                                       font=("Segoe UI Bold", 40), fg=Colors.pinkishRed)
    makeLoanEntry = tk.Entry(loan_tab, width=11, font=("Segoe UI", 30))
    makeLoanButton = tk.Button(loan_tab, text="Fazer emprestimo", padx=60, pady=20, command=makeLoan, fg=Colors.white, background=Colors.pinkishRed, activebackground=Colors.lightGrey)
    payLoanButton = tk.Button(loan_tab, text="Pagar divida", padx=70, pady=20, command=payLoan, fg=Colors.white, background=Colors.pinkishRed, activebackground=Colors.lightGrey)

    loanQuantityLoanLabel.place(relx=0.5, rely=0.2, anchor="center")
    interestRate_DraftLabel.place(relx=0.5, rely=0.6, anchor="center")
    interestPerMonth_DraftLabel.place(relx=0.5, rely=0.7, anchor="center")
    makeLoanEntry.place(relx=0.3, rely=0.3)
    makeLoanButton.place(relx=0.5, rely=0.3)
    payLoanButton.place(relx=0.5, rely=0.4)

    # Aba Deposito e saque
    depositDraft_tab = ttk.Frame(tabs)
    tabs.add(depositDraft_tab, text="Deposito/Saque")

    def deposit():
        users_data[loggedUserIndex].deposit(float(deposit_DraftEntry.get()))
        updateValues()

    def draft():
        users_data[loggedUserIndex].draft(float(deposit_DraftEntry.get()))
        updateValues()

    balanceDeposit_DraftLabel = tk.Label(depositDraft_tab, text="Saldo: R$ {:.2f}".format(float(users_data[loggedUserIndex].getBalance())),
                                     font=("Segoe UI Bold", 40), fg=Colors.pinkishRed)

    deposit_DraftEntry = tk.Entry(depositDraft_tab, width=11, font=("Segoe UI", 30))
    deposit_DraftButton = tk.Button(depositDraft_tab, text="Depositar", padx=60, pady=20, command=deposit, fg=Colors.white,
                               background=Colors.pinkishRed, activebackground=Colors.lightGrey)
    draft_DraftButton = tk.Button(depositDraft_tab, text="Sacar", padx=60, pady=20, command=draft, fg=Colors.white,
                                  background=Colors.pinkishRed, activebackground=Colors.lightGrey)


    balanceDeposit_DraftLabel.place(relx=0.5, rely=0.2, anchor="center")
    deposit_DraftEntry.place(relx=0.3, rely=0.3)
    deposit_DraftButton.place(relx=0.5, rely=0.3)
    draft_DraftButton.place(relx=0.5, rely=0.4)

    # Aba Controle de usuarios
    usersControl_tab = ttk.Frame(tabs)
    tabs.add(usersControl_tab, text="Controle de Usuarios")

    global currentIndex
    currentIndex = 0 # necessario pra dar reload na userlist

    if isinstance(users_data[loggedUserIndex], Client):
        tabs.hide(5)

    def changeLevel():
        selectedUser = usersList.selection()
        indexSelectedUser = (int(selectedUser[0][-3:], 16) - 1)-currentIndex # pega o index do objeto com base na escolha do usuario

        if isinstance(users_data[indexSelectedUser], Client):
            users_data[indexSelectedUser] = Employee(users_data[indexSelectedUser].personInformation.getName(),users_data[indexSelectedUser].personInformation.getCpf(),users_data[indexSelectedUser].getPassword(),users_data[indexSelectedUser].getBalance(),users_data[indexSelectedUser].getLoanAmount())
        else:
            users_data[indexSelectedUser] = Client(users_data[indexSelectedUser].personInformation.getName(),users_data[indexSelectedUser].personInformation.getCpf(),users_data[indexSelectedUser].getPassword(),users_data[indexSelectedUser].getBalance(),users_data[indexSelectedUser].getLoanAmount())
        reloadUserList()


    def deleteUser():
        selectedUser = usersList.selection()
        indexSelectedUser = (int(selectedUser[0][-3:], 16) - 1) - currentIndex
        del users_data[indexSelectedUser]
        reloadUserList()

    def reloadUserList():
        global currentIndex
        usersList.delete(*usersList.get_children()) # deleta da tela os dados, mas mantem os index
        for user in users_data:
            userType = 0
            if isinstance(user, Employee):
                userType = 1;
            usersList.insert("", "end",
                             values=(user.personInformation.getName(), user.personInformation.getCpf(), user.getBalance(), user.getLoanAmount(), userType))
            currentIndex += 1

    usersList = ttk.Treeview(usersControl_tab, columns=("Nome","CPF", "Saldo", "Emprestimos","Nivel"), show="headings")
    usersList.heading("Nome", text="Nome")
    usersList.heading("CPF", text="CPF")
    usersList.heading("Saldo", text="Saldo")
    usersList.heading("Emprestimos", text="Emprestimos")
    usersList.heading("Nivel", text="Nivel")

    changeLevel_controlButton = tk.Button(usersControl_tab, text="Mudar nivel", padx=60, pady=20, command=changeLevel, fg=Colors.white, background=Colors.pinkishRed, activebackground=Colors.lightGrey)
    deleteUser_controlButton = tk.Button(usersControl_tab, text="Deletar usuario", padx=60, pady=20, command=deleteUser, fg=Colors.white, background=Colors.pinkishRed, activebackground=Colors.lightGrey)

    usersList.place(relx=0.5,rely=0.2, anchor="center")
    changeLevel_controlButton.place(relx=0.4,rely=0.5, anchor="center")
    deleteUser_controlButton.place(relx=0.6, rely=0.5, anchor="center")

    reloadUserList()

    def logout():
        mainWindow.destroy()
        goToLoginWindow()

    logoutButton = tk.Button(mainWindow, text="Logout", padx=60, pady=20, command=logout, fg=Colors.white, background=Colors.pinkishRed, activebackground=Colors.lightGrey)

    logoutButton.place(relx=0.9, rely=0.05)
    mainWindow.mainloop()

# inicio
getUsers()
getTransactions()
goToLoginWindow()

