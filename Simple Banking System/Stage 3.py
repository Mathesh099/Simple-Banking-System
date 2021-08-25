import random
import sqlite3
card_number = None
details = None
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS card (
id INTEGER PRIMARY KEY AUTOINCREMENT,
number TEXT NOT NULL,
pin TEXT NOT NULL,
balance INTEGER DEFAULT 0
);
''')
conn.commit()
while True:
    IIN = '400000'
    number = "1"
    choice = input('1. Create an account \n2. Log into account\n0. Exit\n')
    print()
    while len(number) != 9:
        number = random.randint(0, 999999999)
        number = str(number)
        card_number = IIN + number
        temp1 = 0
        temp2 = 0
        sums = 0
        check_sum = 0
        for i in range(len(card_number)):
            if i in [0, 2, 4, 6, 8, 10, 12, 14]:
                if int(card_number[i]) * 2 > 9:
                    a = int(card_number[i]) * 2 - 9
                    temp1 += a
                else:
                    temp1 += int(card_number[i]) * 2
            else:
                temp2 += int(card_number[i])
        sums = int(temp1) + int(temp2)
        check_sum = (sums * 9) % 10
        card_number += str(check_sum)

    PIN = ""
    for i in range(4):
        PIN += str(random.randint(0, 9))

    if choice == '1':
        cur.execute(f"INSERT INTO card(number, pin, balance) VALUES({card_number}, {PIN}, 0)")
        conn.commit()
        print("Your card has been created")
        print('Your card number:')
        print(card_number)
        print('Your card PIN:')
        print(PIN)
        print()
    elif choice == '2':
        card = input('Enter your card number:\n')
        pin = input('Enter your PIN:\n')
        cur.execute("SELECT * FROM card")
        bank_details = cur.fetchall()
        for x in bank_details:
            if x[1] == card:
                if x[2] == pin:
                    details = True
                else:
                    details = False
        print()
        if details:
            print("You have successfully logged in!")
            print()
            cur.execute(f"SELECT * FROM card WHERE number = {card_number}")
            cards = cur.fetchall()
            while True:
                choice = input('1. Balance \n2. Log out\n0. Exit\n')
                print()
                if choice == '1':
                    print('Balance:', cards[3])
                    print()
                elif choice == '2':
                    print('You have successfully logged out!')
                    print()
                    break
                else:
                    print('Bye!')
                    exit()
        else:
            print('Wrong card number or PIN!')
            print()
    else:
        print('Bye!')
        exit()
