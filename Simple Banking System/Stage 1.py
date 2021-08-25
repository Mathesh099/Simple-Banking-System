import random
lists = []

while True:
    IIN = '400000'
    number = "1"
    while len(number) != 10:
        number = random.randint(0, 9999999999)
        number = str(number)
    card_number = IIN + number

    PIN = ""
    for i in range(4):
        PIN += str(random.randint(0, 9))
    Balance = 0
    lists.append(card_number)
    lists.append(PIN)
    choice = input('1. Create an account \n2. Log into account\n0. Exit\n')
    print()
    if choice == '1':
        print("Your card has been created")
        print('Your card number:')
        print(card_number)
        print('Your card PIN:')
        print(PIN)
        print()
    elif choice == '2':
        card = input('Enter your card number:\n')
        pin = input('Enter your PIN:\n')
        print()
        if card in lists and pin in lists:
            print("You have successfully logged in!")
            print()
            while True:
                choice = input('1. Balance \n2. Log out\n0. Exit\n')
                print()
                if choice == '1':
                    print('Balance:',Balance)
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
