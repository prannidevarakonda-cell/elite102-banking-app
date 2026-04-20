import mysql.connector

# Connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="Pranay",
        password="Pranay123!",
        database="Cinder_bank"
    )

# TEST THE CONNECTION
try:
    db = get_db_connection()
    if db.is_connected():
        print("✅ Python is successfully connected to the Database!")
    db.close()
except Exception as e:
    print(f"❌ Connection Failed: {e}")

def show_menu():
    print("-------------------------------")
    print("Welcome to the Cinder Online Banking System!")
    print("--------------------------------")
    print("1. Create Account")
    print("2. Login")
    print("3. Check Balance")
    print("4. Deposit")
    print("5. Withdraw")
    print("6. Access user information")
    print("7. View Transaction History")
    print("8. Admin Panel")
    print("9. Exit Application")
    print("-------------------------------")

import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Pranay123!", # Use your actual password
        database="Cinder_bank"
    )

# Create or Log in to an account

def create_account(name, initial_deposit, pin):
    db = get_db_connection()
    cursor = db.cursor()
    query = "INSERT INTO accounts (holder_name, balance, pin) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, initial_deposit, pin))
    db.commit()
    account_id = cursor.lastrowid
    
    # Log initial deposit transaction
    cursor.execute("INSERT INTO transactions (account_id, type, amount, timestamp) VALUES (%s, 'deposit', %s, NOW())", (account_id, initial_deposit))
    db.commit()
    
    print(f"Account created for {name}! Your Account ID is: {account_id}")
    print("Please save this Account ID for login purposes.")
    db.close()
    return account_id

def login(account_id, pin):
    """Verify login credentials and return account info if valid"""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT holder_name, balance, pin FROM accounts WHERE id = %s", (account_id,))
    user = cursor.fetchone()
    db.close()
    
    if user and user[2] == pin:
        print(f"Welcome, {user[0]}!")
        return account_id
    else:
        print("❌ Invalid account ID or PIN. Please try again.")
        return None

# Check balance, deposit, and withdraw functions
def check_balance(account_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    result = cursor.fetchone()
    if result:
        print(f"Your current balance is: ${result[0]}")
    db.close()

def deposit(account_id, amount):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, account_id))
    db.commit()
    
    # Log transaction
    cursor.execute("INSERT INTO transactions (account_id, type, amount, timestamp) VALUES (%s, 'deposit', %s, NOW())", (account_id, amount))
    db.commit()
    
    print(f"Deposited ${amount} successfully.")
    db.close()

def withdraw(account_id, amount):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    balance = cursor.fetchone()[0]
    if balance >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, account_id))
        db.commit()
        
        # Log transaction
        cursor.execute("INSERT INTO transactions (account_id, type, amount, timestamp) VALUES (%s, 'withdraw', %s, NOW())", (account_id, amount))
        db.commit()
        
        print("Withdrawal successful!")
    else:
        print("Error: Insufficient funds. Please check your balance and try again.")
    db.close()
#Add a password-protected function to access user information
def access_user_info(account_id):
    # This is your password-protected function
    provided_pin = input("Enter your 4-digit PIN to access info: ")
    
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT holder_name, balance, pin FROM accounts WHERE id = %s", (account_id,))
    user = cursor.fetchone()
    
    if user and user[2] == provided_pin:
        print("\n--- USER INFORMATION ---")
        print(f"Name: {user[0]}")
        print(f"Balance: ${user[1]}")
    else:
        print("Incorrect PIN. Please try again or contact support if you've forgotten your PIN.")
    db.close()

def view_transaction_history(account_id):
    """View transaction history for the logged-in account"""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT type, amount, timestamp FROM transactions WHERE account_id = %s ORDER BY timestamp DESC", (account_id,))
    transactions = cursor.fetchall()
    db.close()
    
    if transactions:
        print("\n--- TRANSACTION HISTORY ---")
        print("Type\t\tAmount\t\tDate")
        print("-" * 40)
        for trans in transactions:
            print(f"{trans[0]}\t\t${trans[1]}\t\t{trans[2]}")
    else:
        print("No transactions found.")

# Admin functions for managing accounts
def list_all_accounts():
    """Admin function to list all accounts"""
    admin_pin = input("Enter admin PIN: ")
    if admin_pin != "1234":  # Simple admin PIN for demo
        print("❌ Invalid admin PIN.")
        return
    
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id, holder_name, balance FROM accounts")
    accounts = cursor.fetchall()
    db.close()
    
    if accounts:
        print("\n--- ALL ACCOUNTS ---")
        print("ID\tName\t\tBalance")
        print("-" * 30)
        for account in accounts:
            print(f"{account[0]}\t{account[1]}\t\t${account[2]}")
    else:
        print("No accounts found.")

def delete_account():
    """Admin function to delete an account"""
    admin_pin = input("Enter admin PIN: ")
    if admin_pin != "1234":
        print("❌ Invalid admin PIN.")
        return
    
    try:
        account_id = int(input("Enter account ID to delete: "))
        confirm = input(f"Are you sure you want to delete account {account_id}? (yes/no): ")
        if confirm.lower() != "yes":
            print("Deletion cancelled.")
            return
        
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM accounts WHERE id = %s", (account_id,))
        db.commit()
        if cursor.rowcount > 0:
            print(f"Account {account_id} deleted successfully.")
        else:
            print(" Account not found.")
        db.close()
    except ValueError:
        print("Invalid account ID.")





if __name__ == "__main__":
    logged_in_account = None
    
    while True:
        show_menu()
        choice = input("Please select an option: ")
        
        if choice == "1":
            # Create Account
            name = input("Enter your full name: ")
            try:
                initial_deposit = float(input("Enter initial deposit amount: $"))
                pin = input("Create a 4-digit PIN: ")
                create_account(name, initial_deposit, pin)
            except ValueError:
                print("Invalid amount. Please enter a valid number.")
        
        elif choice == "2":
            # Login
            try:
                account_id = int(input("Enter your account ID: "))
                pin = input("Enter your PIN: ")
                logged_in_account = login(account_id, pin)
            except ValueError:
                print("Invalid input. Please enter valid details.")
        
        elif choice == "3":
            # Check Balance
            if logged_in_account:
                check_balance(logged_in_account)
            else:
                print(" Please login first.")
        
        elif choice == "4":
            # Deposit
            if logged_in_account:
                try:
                    amount = float(input("Enter deposit amount: $"))
                    deposit(logged_in_account, amount)
                except ValueError:
                    print(" Invalid amount.")
            else:
                print("Please login first.")
        
        elif choice == "5":
            # Withdraw
            if logged_in_account:
                try:
                    amount = float(input("Enter withdrawal amount: $"))
                    withdraw(logged_in_account, amount)
                except ValueError:
                    print(" Invalid amount.")
            else:
                print(" Please login first.")
        
        elif choice == "6":
            # Access user information
            if logged_in_account:
                access_user_info(logged_in_account)
            else:
                print(" Please login first.")
        
        elif choice == "7":
            # View Transaction History
            if logged_in_account:
                view_transaction_history(logged_in_account)
            else:
                print(" Please login first.")
        
        elif choice == "8":
            # Admin Panel
            print("\n--- ADMIN PANEL ---")
            print("1. List All Accounts")
            print("2. Delete Account")
            print("3. Back to Main Menu")
            admin_choice = input("Select admin option: ")
            
            if admin_choice == "1":
                list_all_accounts()
            elif admin_choice == "2":
                delete_account()
            elif admin_choice == "3":
                pass
            else:
                print("Invalid admin option.")
        
        elif choice == "9":
            # Exit
            print("Thank you for using Cinder Online Banking System. Goodbye!")
            break
        
        else:
            print("Invalid option. Please try again.")