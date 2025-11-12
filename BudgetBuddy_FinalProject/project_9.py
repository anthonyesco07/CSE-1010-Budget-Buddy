import os
from library import functions
from library.classes_9 import Budget

os.system('cls' if os.name == 'nt' else 'clear')

while True:
     name = input("To being enter your name: ").strip()
     if name != "":
          break
     print("\n** ERROR **")
     print("Name Cannot Be Empty\n")



os.system('cls' if os.name == 'nt' else 'clear')

print(f"Hello {name}, This is BudgetBuddy! Your Personal Budgeting Assistant")
while True:
    try:
        income = float(input("input your monthly income (numbers only):"))
        if income >= 0:
            break
        else:
            print("\n** ERROR **")
            print("Income Cannot Be Negative\n")
    except:
        print("\n** ERROR **")
        print("Please Enter Numbers Only\n")

  
             


total_expenses = []

grocery = Budget("Grocery")
car = Budget("Car")

grocery.add_expenses()
car.add_expenses()

total_expenses.append(grocery.get_expenses())
total_expenses.append(car.get_expenses())

bal = functions.calc_balances(income, sum(total_expenses))

functions.financial_status(bal)

grocery.get_expenses_list()
car.get_expenses_list()

print("this is a test")