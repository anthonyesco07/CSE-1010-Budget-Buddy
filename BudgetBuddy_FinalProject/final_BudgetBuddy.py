import customtkinter as ctk
from tkinter import messagebox, filedialog
from library.classes_9 import Budget
from library import functions
import csv

class BudgetBuddyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Buddy")
        self.root.geometry("500x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        
        self.name = ""
        self.income = 0
        self.grocery_budget = Budget("Grocery")
        self.car_budget = Budget("Car")
        self.current_expense_type = "Grocery"

        self.welcome_frame()

    
    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def restart_app(self):
        """Resets everything and goes back to the main screen"""
        self.name = ""
        self.income = 0
        self.grocery_budget = Budget("Grocery")
        self.car_budget = Budget("Car")
        self.welcome_frame()

    
    def welcome_frame(self):
        self.clear_root()
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both", padx=50, pady=50)

        ctk.CTkLabel(frame, text="Budget Buddy", font=("Segoe UI", 26, "bold")).pack(pady=30)
        ctk.CTkLabel(frame, text="Enter your name:").pack(pady=5)
        self.name_entry = ctk.CTkEntry(frame, width=250)
        self.name_entry.pack(pady=10)
        ctk.CTkButton(frame, text="Continue", command=self.get_name).pack(pady=20)

    def get_name(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter your name")
            return
        self.name = name
        self.income_frame()

    
    def income_frame(self):
        self.clear_root()
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both", padx=50, pady=50)

        ctk.CTkLabel(frame, text=f"Hello {self.name}!", font=("Segoe UI", 22, "bold")).pack(pady=20)
        ctk.CTkLabel(frame, text="Enter your monthly income:").pack(pady=10)

        self.income_entry = ctk.CTkEntry(frame, width=250)
        self.income_entry.pack(pady=10)

        ctk.CTkButton(frame, text="Continue", command=self.get_income).pack(pady=20)

    def get_income(self):
        try:
            income = float(self.income_entry.get())
            if income < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid non-negative income")
            return

        self.income = income
        self.load_or_continue_frame()

    
    def load_or_continue_frame(self):
        self.clear_root()

        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both", padx=50, pady=50)

        ctk.CTkLabel(frame, text="Would you like to load a previous budget file?",
                     font=("Segoe UI", 20)).pack(pady=20)

        ctk.CTkButton(frame, text="Load From File",
                      command=self.load_from_file_first, width=200).pack(pady=10)

        ctk.CTkButton(frame, text="Continue Without Loading",
                      command=lambda: self.expense_frame("Grocery"), width=200).pack(pady=10)

   
    def expense_frame(self, expense_type):
        self.clear_root()
        self.current_expense_type = expense_type

        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both", padx=50, pady=50)

        ctk.CTkLabel(frame, text=f"{expense_type} Expenses",
                     font=("Segoe UI", 22, "bold")).pack(pady=(10, 20))

        
        input_frame = ctk.CTkFrame(frame)
        input_frame.pack(pady=10, fill="x", padx=20)

        self.expense_entry = ctk.CTkEntry(input_frame)
        self.expense_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))

        ctk.CTkButton(input_frame, text="Add", width=80,
                      command=self.add_expense).pack(side="left")

        
        self.expense_list_frame = ctk.CTkScrollableFrame(frame, height=250)
        self.expense_list_frame.pack(pady=20, fill="both", expand=True)

        
        self.display_loaded_items()

        ctk.CTkButton(frame, text="Continue",
                      command=self.next_expense_page).pack(pady=10)

    def display_loaded_items(self):
        """Correctly repopulates the scroll frame."""
        if self.current_expense_type == "Grocery":
            budget = self.grocery_budget
        else:
            budget = self.car_budget

        for cat, amt in zip(budget.categories, budget.expenses):
            self._add_expense_widget(cat, amt)

    
    def add_expense(self):
        text = self.expense_entry.get().strip()
        if not text:
            return

        try:
            cat, val = text.split()
            val = float(val)
        except:
            messagebox.showerror("Error", "Enter in format: ItemName 10")
            return

        if self.current_expense_type == "Grocery":
            budget = self.grocery_budget
        else:
            budget = self.car_budget

        budget.categories.append(cat)
        budget.expenses.append(val)

        self._add_expense_widget(cat, val)
        self.expense_entry.delete(0, "end")

    def _add_expense_widget(self, cat, val):
        item_frame = ctk.CTkFrame(self.expense_list_frame)
        item_frame.pack(fill="x", pady=2, padx=5)

        ctk.CTkLabel(item_frame, text=f"{cat}: ${val:.2f}").pack(side="left", padx=5)

        ctk.CTkButton(item_frame, text="X", width=25,
                      fg_color="red", hover_color="#ff4d4d",
                      command=lambda f=item_frame, c=cat, v=val: self.remove_expense(f, c, v)
                      ).pack(side="right", padx=5)

    def remove_expense(self, frame, cat, val):
        frame.destroy()

        if self.current_expense_type == "Grocery":
            budget = self.grocery_budget
        else:
            budget = self.car_budget

        idx = budget.categories.index(cat)
        budget.categories.pop(idx)
        budget.expenses.pop(idx)

    
    def save_to_file(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file:
            return

        with open(file, "w", newline="") as f:
            writer = csv.writer(f)

            for cat, amt in zip(self.grocery_budget.categories, self.grocery_budget.expenses):
                writer.writerow(["Grocery", cat, amt])

            for cat, amt in zip(self.car_budget.categories, self.car_budget.expenses):
                writer.writerow(["Car", cat, amt])

        messagebox.showinfo("Saved", "Expenses saved successfully!")

        
        self.restart_app()

    def load_from_file_first(self):
        if self.load_from_file():
            self.expense_frame("Grocery")

    def load_from_file(self):
        file = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file:
            return False

        
        self.grocery_budget.categories.clear()
        self.grocery_budget.expenses.clear()
        self.car_budget.categories.clear()
        self.car_budget.expenses.clear()

        with open(file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != 3:
                    continue

                category, cat, amt = row
                amt = float(amt)

                if category == "Grocery":
                    self.grocery_budget.categories.append(cat)
                    self.grocery_budget.expenses.append(amt)

                elif category == "Car":
                    self.car_budget.categories.append(cat)
                    self.car_budget.expenses.append(amt)

        messagebox.showinfo("Loaded", "Expenses loaded successfully!")
        return True

    
    def next_expense_page(self):
        if self.current_expense_type == "Grocery":
            self.expense_frame("Car")
        else:
            self.summary_frame()

    
    def summary_frame(self):
        self.clear_root()
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both", padx=50, pady=50)

        grocery_total = self.grocery_budget.get_expenses()
        car_total = self.car_budget.get_expenses()
        total_expense = grocery_total + car_total
        balance = functions.calc_balances(self.income, total_expense)

        if balance > 0:
            status = "✅ Great! You're saving money!"
        elif balance == 0:
            status = "😐 You're breaking even."
        else:
            status = "⚠️ You're overspending!"

        ctk.CTkLabel(frame, text=f"Hello {self.name}!",
                     font=("Segoe UI", 22, "bold")).pack(pady=15)

        ctk.CTkLabel(frame, text=f"Total Grocery Expenses: ${grocery_total:.2f}",
                     font=("Segoe UI", 18)).pack(pady=5)

        ctk.CTkLabel(frame, text=f"Total Car Expenses: ${car_total:.2f}",
                     font=("Segoe UI", 18)).pack(pady=5)

        ctk.CTkLabel(frame, text=f"Overall Total: ${total_expense:.2f}",
                     font=("Segoe UI", 18)).pack(pady=5)

        ctk.CTkLabel(frame, text=f"Balance: ${balance:.2f}",
                     font=("Segoe UI", 18)).pack(pady=5)

        ctk.CTkLabel(frame, text=status, font=("Segoe UI", 18)).pack(pady=15)

        
        ctk.CTkButton(frame, text="Save to File", width=180,
                      command=self.save_to_file).pack(pady=10)

      
        ctk.CTkButton(frame, text="Return to Menu", width=180,
                      command=self.restart_app).pack(pady=10)



if __name__ == "__main__":
    root = ctk.CTk()
    app = BudgetBuddyApp(root)
    root.mainloop()