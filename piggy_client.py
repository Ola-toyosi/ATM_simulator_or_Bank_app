from pathlib import Path
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import json
import socket
import sqlite3
import datetime
from random import choice

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./build/assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Application(Tk):
    customer = ''
    pins = {}
    names = {}
    account_no = {}
    balance = {}
    trxn_id = []

    print(balance)

    def __init__(self):
        super().__init__()
        self.title("Welcome!")
        w = 375
        h = 700 - 100
        self.position_window(w, h)
        self.resizable(False, False)
        

        self.customer = StringVar()
        self.code_trial = 0
        self.pin_trial = 0
        self.customer_code = StringVar()
        self.pins = {'customer code': 0}
        self.connect_socket()
        self.socket.send(str.encode('pin'))
        self.pins = json.loads(bytes.decode(self.socket.recv(1024)))
        self['bg'] = 'blue'
        Application.pins = self.pins
        self.socket.send(str.encode('names'))
        Application.names = json.loads(bytes.decode(self.socket.recv(1024)))
        self.socket.send(str.encode('acct'))
        Application.account_no = json.loads(bytes.decode(self.socket.recv(1024)))
        self.socket.send(str.encode('balance'))
        Application.balance = json.loads(bytes.decode(self.socket.recv(1024)))
        self.socket.send(str.encode('trxn'))
        Application.trxn_id = json.loads(bytes.decode(self.socket.recv(1024)))
        self.socket.send(str.encode('q'))
        
        self.create_widgets()

    def connect_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5424
        self.host = socket.gethostbyname("localhost")
        self.socket.connect((self.host, self.port))
        data = bytes.decode(self.socket.recv(1024))
        print(data)

    def position_window(self, w, h):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.resizable(False, False)

    def create_widgets(self):

        self.canvas = Canvas(
            self,
            bg = "#B06DE4",
            height = 700 - 100,
            width = 375,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.canvas.create_rectangle(
            0.0,
            373.0 - 100,
            375.0,
            598.0 - 100,
            fill="#FFFFFF",
            outline="")

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            187.5,
            466.5 - 100,
            image=self.entry_image_1
        )

        self.entry_code = Entry(self,
            bd=0,
            bg="#EFE3E3",
            highlightthickness=0,
            textvariable=self.customer_code
        )
        self.entry_code.place(
            x=85.0,
            y=451.0 - 100,
            width=205.0,
            height=29.0
        )

        self.canvas.create_text(
            58.0,
            162.0 - 100,
            anchor="nw",
            text="WELCOME \nTO \nPIGGYBANK",
            fill="#FFFFFF",
            font=("Rajdhani Bold", 44 * -1)
        )

        self.canvas.create_text(
            82.0,
            402.0 - 100,
            anchor="nw",
            text="Enter customer code:",
            fill="#B06DE4",
            font=("Rajdhani SemiBold", 22 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))

        self.button_sign_in = Button(self,
            image= self.button_image_1, 
            command=self.sign_in,
            bg='white', 
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
            )

        self.button_sign_in.place(
            x=125.0,
            y=489.0 - 100,
            width=125.0,
            height=60.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            bg="#B06DE4",
            relief="flat"
        )
        self.button_2.place(
            x=239.0,
            y=648.0 - 100,
            width=125.0,
            height=60.0
        )
    def customer_exist(self, customer_code):
        for i in self.pins:
            if customer_code == i:
                return i
        return None

    def contact_customer(self):
        messagebox.showinfo(title='Sorry!', message='Too many attempts, contact customer service')

    def wrong_code(self):
        messagebox.showinfo(title='Try Again!', message='Customer code does not exist, try again')

    def wrong_value(self, value):
        messagebox.showinfo(title='Try Again!', message=f'{value} must be number digits only, try again')

    def code_length(self):
        messagebox.showinfo(title='Try Again!', message='Customer code must be exactly 4 digits long, try again')

    def check_int(self, value):
        try:
            return int(value)
        except ValueError as Argument:
            print("Value must be numbers only\n", Argument)

    def check_len(self, value):
        if len(value) == 4:
            return True
        else:
            return False

    def sign_in(self):
        customer_code = self.customer_code.get()

        if self.check_len(customer_code):
            if type(self.check_int(customer_code)) == int:
                Application.customer = self.customer_exist(customer_code)
                if Application.customer:
                    self.destroy()
                    AuthenticateWindow()
                else:
                    self.entry_customer_code.delete(0, END)
                    self.wrong_code()
                    self.code_trial += 1
                    print(f'trial ={self.code_trial}')
            else:
                self.entry_customer_code.delete(0, END)
                self.wrong_value('Customer code')
                self.code_trial += 1
                print(f'trial ={self.code_trial}')
        else:
            self.code_length()
            self.code_trial += 1
            print(f'trial ={self.code_trial}')
        if self.code_trial == 3:
            self.contact_customer()
            self.destroy()

class AuthenticateWindow(Tk):
    name = ''

    def __init__(self):
        super().__init__()

        self.title("Authentication!")
        w = 375
        h = 500
        Application.position_window(self, w, h)

        self.customer = Application.customer
        self.pin_trial = 0
        self.names = Application.names
        self['bg'] = 'blue'

        self.name = Application.names[Application.customer]
        # self.name = Authenticate_window.name.title()
        AuthenticateWindow.name = self.name.upper()
        # print(self.names)
        # print(Authenticate_window.name)

        self.grid()
        self.create_widgets()

    def create_widgets(self):

        self.canvas = Canvas(
            self,
            bg = "#B06DE4",
            height = 600,
            width = 375,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)
        self.canvas.create_rectangle(
            0.0,
            273.0 - 100,
            375.0,
            498.0 - 100,
            fill="#FFFFFF",
            outline="")

        self.pin=StringVar()
        self.entry_pin = Entry(self,
            bd=0,
            bg="#EFE3E3",
            highlightthickness=0,
            textvariable=self.pin
        )
        self.entry_pin.place(
            x=85.0,
            y=451.0 - 200,
            width=205.0,
            height=29.0
        )

        self.canvas.create_text(
            58.0,
            162.0- 100,
            anchor="nw",
            text=f"Welcome \n{AuthenticateWindow.name};",
            fill="#FFFFFF",
            font=("Rajdhani Bold", 30 * -1)
        )

        self.canvas.create_text(
            82.0,
            402.0 - 200,
            anchor="nw",
            text="Enter pin:",
            fill="#B06DE4",
            font=("Rajdhani SemiBold", 22 * -1)
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))

        self.button_sign_in = Button(self,
            image= self.button_image_3, 
            command=self.enterapp,
            bg='white', 
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
            )

        self.button_sign_in.place(
            x=125.0,
            y=489.0 - 200,
            width=125.0,
            height=60.0
        )

    def authenticate(self, customer, pin):
        if str(Application.pins[customer]) == str(pin):
            return True
        else:
            return False

    def wrong_pin(self):
        messagebox.showinfo(title='Wrong Pin!', message='You have entered a wrong pin, try again')

    def pin_length(self):
        messagebox.showinfo(title='Wrong Pin!', message='Pin must be exactly 4 digits long, try again')

    def enterapp(self):
        customer = self.customer
        pin = self.pin.get()

        if Application.check_len(self, pin):
            if type(Application.check_int(self, pin)) == int:
                if self.authenticate(customer, pin):
                    self.destroy()
                    print('login successful')
                    Transaction()
                else:
                    self.entry_pin.delete(0, END)
                    self.wrong_pin()
                    self.pin_trial += 1
                    print(f'trial ={self.pin_trial}')
            else:
                self.entry_pin.delete(0, END)
                Application.wrong_value(self, 'Pin')
                self.pin_trial += 1
                print(f'trial ={self.pin_trial}')
        else:
            self.pin_length()
            self.pin_trial += 1
            print(f'trial ={self.pin_trial}')
        if self.pin_trial == 3:
            Application.contact_customer(self)
            self.destroy()

class Transaction(Tk):
    # balance = 0

    def __init__(self):
        super().__init__()
        self.title("Transaction Screen")
        w = 375
        h = 600
        Application.position_window(self, w, h)

        Transaction.balance = int(Application.balance[Application.customer])
        Transaction.acct_no = Application.account_no[Application.customer]

        self.grid()
        self.create_widgets()
        Transaction.wm_protocol(self, "WM_DELETE_WINDOW", self.on_closing)


    def create_widgets(self):
        self.canvas = Canvas(
            self,
            bg = "#0A0A0A",
            height = 600,
            width = 375,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.balance_btn_img = PhotoImage(
            file=relative_to_assets("balance.png"))
        self.balance_btn = Button(
            image=self.balance_btn_img,
            borderwidth=0,
            highlightthickness=0,
            bg='#0A0A0A',
            command=self.show_balance,
            relief="flat"
        )
        self.balance_btn.place(
            x=75.0,
            y=100.0,
            width=225.0,
            height=60.0
        )

        self.withdraw_btn_img = PhotoImage(
            file=relative_to_assets("withdraw.png"))
        self.withdraw_btn = Button(
            image=self.withdraw_btn_img,
            borderwidth=0,
            highlightthickness=0,
            bg='#0A0A0A',
            command=self.withdrawScreen,
            relief="flat"
        )
        self.withdraw_btn.place(
            x=75.0,
            y=210.0,
            width=225.0,
            height=60.0
        )

        self.deposit_btn_img = PhotoImage(
            file=relative_to_assets("deposit.png"))
        self.deposit_btn = Button(
            image=self.deposit_btn_img,
            borderwidth=0,
            highlightthickness=0,
            bg='#0A0A0A',
            command=self.depositScreen,
            relief="flat"
        )
        self.deposit_btn.place(
            x=75.0,
            y=325.0,
            width=225.0,
            height=60.0
        )

        self.transfer_btn_img = PhotoImage(
            file=relative_to_assets("transfer.png"))
        self.transfer_btn = Button(
            image=self.transfer_btn_img,
            borderwidth=0,
            highlightthickness=0,
            bg='#0A0A0A',
            command=self.recipientScreen,
            relief="flat"
        )
        self.transfer_btn.place(
            x=75.0,
            y=445.0,
            width=225.0,
            height=60.0
        )

    def show_balance(self):
        AuthenticateWindow.withdraw(self)
        messagebox.showinfo(title='Account Balance', message='Dear {}\n Your current balance '
                                                             'is ₦{:,.2f}'.format(AuthenticateWindow.name,
                                                                                  Transaction.balance))
        AuthenticateWindow.deiconify(self)

    w = 375
    h = 600
    bg = 'purple'

    def withdrawScreen(self):
        AuthenticateWindow.withdraw(self)
        withdraw_window = Toplevel(self)
        withdraw_window.title("Withdraw")
        withdraw_window.configure(bg = "#0A0A0A")
        Application.position_window(withdraw_window, self.w, self.h)
        withdraw_window.grab_set()
        self.withdraw_amount = StringVar()
        


        withdraw_window.canvas = Canvas(
            withdraw_window,
            bg = "#0A0A0A",
            height = 600,
            width = 375,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        withdraw_window.canvas.place(x = 0, y = 0)
        withdraw_window.canvas.create_text(
            10.0,
            194.0,
            anchor="nw",
            text="How much would you like to withdraw?",
            fill="#B06DE4",
            font=("Rajdhani SemiBold", 20 * -1)
        )

        withdraw_window.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        entry_bg_2 = withdraw_window.canvas.create_image(
            187.5,
            309.5,
            image=withdraw_window.entry_image_2
        )
        withdraw_window.label_withdraw_amount = Entry(
            withdraw_window,
            textvariable=self.withdraw_amount,
            bd=0,
            bg="#EFE3E3",
            highlightthickness=0
        )
        withdraw_window.label_withdraw_amount.place(
            x=85.0,
            y=294.0,
            width=205.0,
            height=29.0
        )

        withdraw_window.withdraw_img_btn = PhotoImage(
            file=relative_to_assets("button_4.png"))
        withdraw_window.button_withdraw = Button(
            withdraw_window,
            image=withdraw_window.withdraw_img_btn,
            borderwidth=0,
            highlightthickness=0,
            bg='#0A0A0A',
            command=self.withdraw,
            relief="flat"
        )
        withdraw_window.button_withdraw.place(
            x=125.0,
            y=345.0,
            width=125.0,
            height=60.0
        )

    def depositScreen(self):
        AuthenticateWindow.withdraw(self)
        deposit_window = Toplevel(self)
        deposit_window.title("Deposit")
        deposit_window.configure(bg = "#0A0A0A")
        Application.position_window(deposit_window, self.w, self.h)
        deposit_window.grab_set()
        self.deposit_amount = StringVar()
        


        deposit_window.canvas = Canvas(
            deposit_window,
            bg = "#0A0A0A",
            height = 600,
            width = 375,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        deposit_window.canvas.place(x = 0, y = 0)
        deposit_window.canvas.create_text(
            10.0,
            194.0,
            anchor="nw",
            text="How much would you like to deposit?",
            fill="#B06DE4",
            font=("Rajdhani SemiBold", 20 * -1)
        )

        deposit_window.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        entry_bg_2 = deposit_window.canvas.create_image(
            187.5,
            309.5,
            image=deposit_window.entry_image_2
        )
        deposit_window.label_deposit_amount = Entry(
            deposit_window,
            textvariable=self.deposit_amount,
            bd=0,
            bg="#EFE3E3",
            highlightthickness=0
        )
        deposit_window.label_deposit_amount.place(
            x=85.0,
            y=294.0,
            width=205.0,
            height=29.0
        )

        deposit_window.deposit_img_btn = PhotoImage(
            file=relative_to_assets("button_5.png"))
        deposit_window.button_deposit = Button(
            deposit_window,
            image=deposit_window.deposit_img_btn,
            borderwidth=0,
            highlightthickness=0,
            bg='#0A0A0A',
            command=self.deposit,
            relief="flat"
        )
        deposit_window.button_deposit.place(
            x=125.0,
            y=345.0,
            width=125.0,
            height=60.0
        )

    def transferScreen(self):
        AuthenticateWindow.withdraw(self)
        transfer_window = Toplevel(self)
        transfer_window.title("Transfer")
        transfer_window.configure(bg = "#0A0A0A")
        Application.position_window(transfer_window, self.w, self.h)
        transfer_window.grab_set()
        self.transfer_amount = StringVar()
        


        transfer_window.canvas = Canvas(
            transfer_window,
            bg = "#0A0A0A",
            height = 600,
            width = 375,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        transfer_window.canvas.place(x = 0, y = 0)
        transfer_window.canvas.create_text(
            10.0,
            194.0,
            anchor="nw",
            text="How much would you like to transfer?",
            fill="#B06DE4",
            font=("Rajdhani SemiBold", 20 * -1)
        )

        transfer_window.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        transfer_window.entry_bg_2 = transfer_window.canvas.create_image(
            187.5,
            309.5,
            image=transfer_window.entry_image_2
        )
        transfer_window.label_transfer_amount = Entry(
            transfer_window,
            textvariable=self.transfer_amount,
            bd=0,
            bg="#EFE3E3",
            highlightthickness=0
        )
        transfer_window.label_transfer_amount.place(
            x=85.0,
            y=294.0,
            width=205.0,
            height=29.0
        )

        transfer_window.transfer_img_btn = PhotoImage(
            file=relative_to_assets("button_6.png"))
        transfer_window.button_transfer = Button(
            transfer_window,
            image=transfer_window.transfer_img_btn,
            borderwidth=0,
            highlightthickness=0,
            bg='#0A0A0A',
            command=self.transfer,
            relief="flat"
        )
        transfer_window.button_transfer.place(
            x=125.0,
            y=345.0,
            width=125.0,
            height=60.0
        )

    def recipientScreen(self):
        AuthenticateWindow.withdraw(self)
        recipient_window = Toplevel(self)
        recipient_window.title("Transfer to:")
        recipient_window['bg'] = self.bg
        Application.position_window(recipient_window, self.w, self.h)
        recipient_window.grab_set()
        self.bank = StringVar()

        self.banks = ['Access Bank', 'Citibank', 'Diamond Bank', 'Dynamic Standard Bank', 'Ecobank Nigeria',
                      'Fidelity Bank Nigeria', 'First Bank of Nigeria', 'First City Monument Bank',
                      'Guaranty Trust Bank', 'Heritage Bank Plc', 'Jaiz Bank', 'Keystone Bank Limited',
                      'Providus Bank Plc', 'Polaris Bank', 'Stanbic IBTC Bank Nigeria Limited',
                      'Standard Chartered Bank', 'Sterling Bank', 'Suntrust Bank Nigeria Limited',
                      'Union Bank of Nigeria', 'United Bank for Africa', 'Unity Bank Plc', 'Wema Bank', 'Zenith Bank']
        self.recipient = StringVar()

        recipient_window.configure(bg = "#0A0A0A")


        recipient_window.canvas = Canvas(
            recipient_window,
            bg = "#0A0A0A",
            height = 600,
            width = 375,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        recipient_window.canvas.place(x = 0, y = 0)
        recipient_window.canvas.create_text(
            24.0,
            235.0,
            anchor="nw",
            text="Enter Receipient \nAccount Number:",
            fill="#B06DE4",
            font=("Rajdhani SemiBold", 20 * -1)
        )

        recipient_window.canvas.create_text(
            22.0,
            300.0,
            anchor="nw",
            text="Select Receipient\nBank:",
            fill="#B06DE4",
            font=("Rajdhani SemiBold", 20 * -1)
        )

        recipient_window.entry_image_3 = PhotoImage(
            file=relative_to_assets("entry_3.png"))
        recipient_window.entry_bg_3 = recipient_window.canvas.create_image(
            270.5,
            264.5,
            image=recipient_window.entry_image_3
        )
        recipient_window.entry_recipient = Entry(
            recipient_window,
            textvariable=self.recipient,
            bd=0,
            bg="#EFE3E3",
            highlightthickness=0
        )
        recipient_window.entry_recipient.place(
            x=189.0,
            y=249.0,
            width=163.0,
            height=29.0
        )

        recipient_window.entry_image_4 = PhotoImage(
            file=relative_to_assets("entry_4.png"))
        recipient_window.entry_bg_4 = recipient_window.canvas.create_image(
            270.5,
            330.5,
            image=recipient_window.entry_image_4
        )
        recipient_window.recipient_bank_box = ttk.Combobox(
            recipient_window,
            values=self.banks,
            textvariable=self.bank, 
            state='readonly',
            font=("Rajdhani SemiBold", 16 * -1)
        )
        recipient_window.recipient_bank_box.place(
            x=189.0,
            y=315.0,
            width=163.0,
            height=29.0
        )

        recipient_window.verify_image = PhotoImage(
            file=relative_to_assets("verify.png"))
        recipient_window.button_transfer = Button(
            recipient_window,
            image=recipient_window.verify_image,
            borderwidth=0,
            highlightthickness=0,
            bg='#0A0A0A',
            command=self.confirm_recv,
            relief="flat"
        )
        recipient_window.button_transfer.place(
            x=137.0,
            y=355.0,
            width=125.0,
            height=60.0
        )

        # cur_row = 0
        # recipient_window.recv_frame = Frame(recipient_window)

        # recipient_window.r_frame = Frame(recipient_window.recv_frame)
        # recipient_window.label_recipient = Label(recipient_window.r_frame, text="Enter Recipient\nAccount Number:",
        #                                          font="Arial 10 normal", bg='white')
        # recipient_window.label_recipient.grid(row=0, column=1, sticky=W)

        # recipient_window.entry_recipient = Entry(recipient_window.r_frame, text=" ", textvariable=self.recipient)
        # recipient_window.entry_recipient.grid(row=0, column=2, sticky=W, padx=5)

        # recipient_window.label_recipient_bank = Label(recipient_window.r_frame, text="Select Recipient \nBank: ",
        #                                               font="Arial 10 normal", bg='white')
        # recipient_window.label_recipient_bank.grid(row=1, column=1, sticky=W, pady=10)

        # recipient_window.recipient_bank_box = ttk.Combobox(recipient_window.r_frame, values=self.banks,
        #                                                    textvariable=self.bank, state='readonly')
        # recipient_window.recipient_bank_box.grid(row=1, column=2, sticky=E, padx=5, pady=10)
        # recipient_window.r_frame['bg'] = self.bg
        # recipient_window.r_frame.grid(row=cur_row, column=0, pady=10)

        # cur_row += 1
        # recipient_window.button_transfer = Button(recipient_window.recv_frame, text='Submit', font='Cambria 8 bold',
        #                                           width=12, command=self.confirm_recv, bg='orange red', fg='white')
        # recipient_window.button_transfer.grid(row=cur_row, column=0, pady=5)
        # recipient_window.recv_frame['bg'] = 'purple'
        # recipient_window.recv_frame.grid(row=cur_row, column=3, rowspan=3, padx=40, pady=40)
    
    def numb(self, value):
        for i in value:
            if i not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                print('must be numbers only')
                return False
        return value

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def confirm(self):
        if messagebox.askyesno("another transaction?", "Do you want to perform another transaction?"):
            self.destroy()
            AuthenticateWindow()
        else:
            self.destroy()

    def account_length(self):
        messagebox.showinfo(title='Try Again!', message='Account number must be exactly 10 digits long, try again')

    def empty_bank(self):
        messagebox.showinfo(title='Try Again!', message='Please select a customer bank and try again')

    def insufficient_bal(self):
        messagebox.showinfo(title='Insufficient Balance!', message='You do not have sufficient funds to complete '
                                                                   'this this transaction...')

    def record_trxn(self, amount, date):
        try:
            connrec = sqlite3.connect('piggybank.db')
            cursor = connrec.cursor()
            print("Connected to SQLite")

            sequence = [i for i in range(1000, 5000)]
            trxn_IDs = [x for x in sequence if x not in Application.trxn_id]
            trxn_id = str(choice(trxn_IDs))
            Application.trxn_id.append(int(trxn_id))

            acct_no = str(Transaction.acct_no)
            balance = str(Transaction.balance)
            stmt = "insert into Trxn(trxn_id, accountNo, amount, working_bal, trxn_date) values(?, ?, ?, ?, ?)"
            values = [(trxn_id, acct_no, amount, balance, date)]
            cursor.executemany(stmt, values)
            connrec.commit()
            print("Record Updated successfully ")
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to update sqlite table", error)
        finally:
            if connrec:
                connrec.close()
                print("The SQLite connection is closed")

    def updateSqliteTable(self):
        try:
            conn = sqlite3.connect('piggybank.db')
            cursor = conn.cursor()
            print("Connected to SQLite")

            sql_update_query = f"""Update customers_account set account_balance = {Transaction.balance} 
            where customer_code = {Application.customer}"""
            cursor.execute(sql_update_query)
            conn.commit()
            print("Record Updated successfully ")
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to update sqlite table", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def withdraw(self):
        withdraw_amount = self.withdraw_amount.get()
        if type(Application.check_int(self, withdraw_amount)) == int:
            if self.numb(withdraw_amount):
                if int(withdraw_amount) <= Transaction.balance:
                    Transaction.balance -= int(withdraw_amount)
                    Application.balance[Application.customer] = Transaction.balance
                    transfer_date = datetime.datetime.now()
                    date = str(transfer_date)
                    amount = "-" + str(withdraw_amount)
                    self.record_trxn(amount, date)
                    self.updateSqliteTable()
                    self.confirm()
                else:
                    self.withdraw_amount.set("")
                    self.insufficient_bal()
            else:
                self.withdraw_amount.set("")
                Application.wrong_value(self, 'Amount')
        else:
            self.withdraw_amount.set("")
            Application.wrong_value(self, 'Amount')


    def deposit(self):
        deposit_amount = self.deposit_amount.get()
        if type(Application.check_int(self, deposit_amount)) == int:
            if self.numb(deposit_amount):
                Transaction.balance += int(deposit_amount)
                Application.balance[Application.customer] = Transaction.balance
                transfer_date = datetime.datetime.now()
                date = str(transfer_date)
                amount = "+" + str(deposit_amount)
                self.record_trxn(amount, date)
                self.updateSqliteTable()
                self.confirm()
            else:
                self.deposit_amount.set("")
                Application.wrong_value(self, 'Amount')
        else:
            self.deposit_amount.set("")
            Application.wrong_value(self, 'Amount')

    def confirm_recv(self):
        recipient_acct = self.recipient.get()
        if type(Application.check_int(self, recipient_acct)) == int:
            if len(recipient_acct) == 10:
                if self.numb(recipient_acct):
                    bank = self.bank.get()
                    if len(bank) == 0:
                        self.empty_bank()
                    else:
                        self.transferScreen()
                else:
                    self.recipient.set("")
                    Application.wrong_value(self, "Account number")
            else:
                self.recipient.set("")
                self.account_length()
        else:
            self.recipient.set("")
            Application.wrong_value(self, 'Account number')

    def transfer(self):
        transfer_amount = self.transfer_amount.get()
        if type(Application.check_int(self, transfer_amount)) == int:
            if self.numb(transfer_amount):
                if int(transfer_amount) <= Transaction.balance:
                    Transaction.balance -= int(transfer_amount)
                    Application.balance[Application.customer] = Transaction.balance
                    transfer_date = datetime.datetime.now()
                    date = str(transfer_date)
                    amount = "-" + str(transfer_amount)
                    self.record_trxn(amount, date)
                    self.updateSqliteTable()
                    self.confirm()
                else:
                    self.transfer_amount.set("")
                    self.insufficient_bal()
            else:
                self.transfer_amount.set("")
                Application.wrong_value(self, 'Amount')
        else:
            self.transfer_amount.set("")
            Application.wrong_value(self, 'Amount')


if __name__ == "__main__":
    app = Application()
    app.mainloop()