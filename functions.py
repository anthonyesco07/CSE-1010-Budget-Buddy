#Logic from Project 2 & 3 goes here
def calc_balances(income, expense):
    print(f"Total expenses are {expense}")
    balance = income - expense
    return balance 

def financial_status(balance):
    if int(balance) > 0:
        print("Great! You are saving money")
    elif int(balance) == 0:
        print("You are breaking even")
    else:
        print("**WARNING** You are overspending!")
