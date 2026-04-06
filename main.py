class BankAccount:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
        else:
            print("Invalid withdrawal amount.")

    def check_balance(self):
        print(f"Current balance: ${self.balance}")

# Example usage
if __name__ == "__main__":
    account = BankAccount("John Doe", 1000)
    account.check_balance()
    account.deposit(500)
    account.withdraw(200)
    account.check_balance()