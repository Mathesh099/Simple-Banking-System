import random
import sqlite3
card_number = None
cards = None
details = False
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
            if card == x[1]:
                if pin == x[2]:
                    details = True
                else:
                    details = False
        print()
        if not details:
            print('Wrong card number or PIN!')
            print()
        else:
            print("You have successfully logged in!")
            print()

            while True:
                choice = input('1. Balance \n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n')
                print()
                if choice == '1':
                    cur.execute(f"SELECT * FROM card WHERE number = {card}")
                    cards = cur.fetchall()
                    balance = cards[0][3]
                    print('Balance:', balance)
                    print()
                elif choice == '2':
                    amount = int(input('Enter income:\n'))
                    print(amount)
                    cur.execute(f"SELECT * FROM card WHERE number = {card}")
                    cards = cur.fetchall()
                    total_amount = cards[0][3] + amount
                    cur.execute(f'UPDATE card SET balance = {total_amount} WHERE number = {card}')
                    conn.commit()
                    print('Income was added!')
                elif choice == '3':
                    print('Transfer')
                    transfer_card = input('Enter card number:\n')
                    cur.execute('SELECT * FROM card')
                    bank_details = cur.fetchall()
                    for x in bank_details:
                        if transfer_card in x[1]:
                            details = True
                        else:
                            details = False
                    transfer_temp1 = 0
                    transfer_temp2 = 0
                    for i in range(len(transfer_card) - 1):
                        if i in [0, 2, 4, 6, 8, 10, 12, 14]:
                            if int(transfer_card[i]) * 2 > 9:
                                b = int(transfer_card[i]) * 2 - 9
                                transfer_temp1 += b
                            else:
                                transfer_temp1 += int(transfer_card[i]) * 2
                        else:
                            transfer_temp2 += int(transfer_card[i])

                    transfer_sum = int(transfer_temp1) + int(transfer_temp2)
                    transfer_check1 = list(transfer_card).pop()
                    transfer_check2 = int(transfer_sum) + int(transfer_check1)
                    transfer_check3 = transfer_check2 % 10
                    if transfer_check3 == 0:
                        transfer_card_check = True
                    else:
                        transfer_card_check = False
                    if not transfer_card_check:
                        print('Probably you made a mistake in the card number. Please try again!')
                    elif not details:
                        print("Such a card does not exist.")
                    elif transfer_card == card:
                        print("You can 't transfer money to the same account!")
                    else:
                        amount = int(input('Enter how much money you want to transfer:\n'))
                        cur.execute(f"SELECT * FROM card WHERE number = {card}")
                        cards = cur.fetchall()
                        if amount > cards[0][3]:
                            print('Not enough money!')
                        else:
                            cur.execute(f"SELECT * FROM card WHERE number = {card}")
                            cards = cur.fetchall()
                            cur.execute(f'UPDATE card SET balance = {cards[0][3] - amount} WHERE number = {card}')
                            conn.commit()

                            cur.execute(f'SELECT * FROM CARD WHERE number = {transfer_card}')
                            cards = cur.fetchall()
                            cur.execute(f'UPDATE card SET balance = {cards[0][3] + amount} WHERE number = {transfer_card}')
                            conn.commit()
                            print('Success!')
                elif choice == '4':
                    cur.execute(f'DELETE FROM card WHERE number = {card}')
                    conn.commit()
                    print('The account has been closed!')
                    break
                elif choice == '5':
                    print('You have successfully logged out!')
                    print()
                    break
                else:
                    print('Bye!')
                    exit()
    else:
        print('Bye!')
        exit()
