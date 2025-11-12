import tkinter as tk
from tkinter import messagebox
from library.classes_9 import Budget
from library import functions

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy - Tkinter Edition")
        self.root.geometry("500x600")

        # ----- Name -----
        tk.Label(root, text="Welcome to BudgetBuddy!", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(root, text="Enter your name:").pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack(pady=5)

        # ----- Income -----
        tk.Label(root, text="Enter your monthly income:").pack()
        self.income_entry = tk.Entry(root)
        self.income_entry.pack(pady=5)

        # ----- Expense Inputs -----
        self.grocery_budget = Budget("Grocery")
        self.car_budget = Budget("Car")

        tk.Label(root, text="Add Grocery Expenses (Type Cost):").pack(pady=5)
        self.grocery_text = tk.Text(root, height=4, width=40)
        self.grocery_text.pack()

        tk.Label(root, text="Add Car Expenses (Type Cost):").pack(pady=5)
        self.car_text = tk.Text(root, height=4, width=40)
        self.car_text.pack()

        # ----- Button -----
        tk.Button(root, text="Calculate Budget", command=self.calculate_budget, bg="#4CAF50", fg="white").pack(pady=15)

        # ----- Result -----
        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def calculate_budget(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Name cannot be empty")
            return

        try:
            income = float(self.income_entry.get())
            if income < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid non-negative income")
            return

        # Parse expenses
        def parse_expenses(text_widget, budget_obj):
            text = text_widget.get("1.0", tk.END).strip()
            if not text:
                return
            lines = text.split("\n")
            for line in lines:
                try:
                    cat, val = line.split()
                    budget_obj.expenses.append(float(val))
                    budget_obj.categories.append(cat)
                except:
                    messagebox.showwarning("Warning", f"Invalid line ignored: {line}")

        parse_expenses(self.grocery_text, self.grocery_budget)
        parse_expenses(self.car_text, self.car_budget)

        total_expense = self.grocery_budget.get_expenses() + self.car_budget.get_expenses()
        balance = functions.calc_balances(income, total_expense)

        # Financial status message
        if balance > 0:
            status = "✅ Great! You are saving money!"
        elif balance == 0:
            status = "😐 You are breaking even."
        else:
            status = "⚠️ You are overspending!"

        self.result_label.config(
            text=f"Hello {name}!\nTotal Expenses: ${total_expense:.2f}\nBalance: ${balance:.2f}\n{status}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()