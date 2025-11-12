class Budget:
    def __init__(self, expense_type):
        self.expense_type = expense_type
        self.expenses = []
        self.categories = []
    
    def add_expenses(self):
        while True:
            try:
                num_expenses = int(input(f"Enter the number of {self.expense_type} expenses you want to add (integers only, max 20): "))
                if num_expenses < 0:
                    print("\n** ERROR **")
                    print("Number Cannot Be Negative\n")
                    continue
                if num_expenses > 20:
                    print("\n** ERROR **")
                    print("Too Many Expenses! Try a smaller number\n")
                    continue
                break
            except:
                print("\n** ERROR **") 
                print("Input Integers Only\n")
        

        print("\nEnter expenses in \"Type Cost\" format. e.g., Milk 10")
        for i in range(num_expenses):
            while True:
                try:
                    type, exp = input(f" Enter expense #{i+1}: ").split()
                    self.expenses.append(float(exp))
                    self.categories.append(type)
                    break
                except:
                    print("\n** ERROR **")
                    print("Wrong input format. Please type expenses in this format: Milk 10\n")
            
                           

    def get_expenses(self):
        total = sum(self.expenses)
        print()
        print(f"Total money you spent on {self.expense_type} is {total}.")
        return total
    
    def get_expenses_list(self):
        print(f"Money you spent on {self.expense_type} are:")
        print()
        for i in range(len(self.expenses)):
            print(f"{self.categories[i]} : {self.expenses[i]}")
    
    
