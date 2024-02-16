import tkinter as tk
from tkinter import ttk, messagebox
from stock import StockSystem


class Login:
    def __init__(self, root, success_callback=None):
        self.root = root
        self.root.title("Login Page")
        self.success_callback = success_callback
        self.create_login_widgets()


    def create_login_widgets(self):
        self.root.geometry("200x200")
        tk.Label(self.root, text="Username: ").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)


        tk.Label(self.root, text="Password: ").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)


        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)


        tk.Button(button_frame, text="Sign Up", command=self.signup).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Login", command=self.login).pack(side=tk.RIGHT, padx=5)


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()


        if self.check_login(username, password):
            messagebox.showinfo("Login Successful", "Welcome, {}".format(username))
            self.root.destroy()
            self.launch_stock_program()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()


        if self.username_exists(username):
            messagebox.showerror("Sign Up Failed", "Username already exists. Choose a different username.")
        else:
            with open('login.txt', 'a') as file:
                file.write(f"{username} {password}\n")
            messagebox.showinfo("Sign Up Successful", "Account created successfully. You can now log in.")


    def check_login(self, username, password):
        with open('login.txt', 'r') as file:
            for line in file:
                stored_username, stored_password = line.strip().split()
                if username == stored_username and password == stored_password:
                    return True
        return False


    def username_exists(self, username):
        with open('login.txt', 'r') as file:
            for line in file:
                stored_username, _ = line.strip().split()
                if username == stored_username:
                    return True
        return False

    def launch_stock_program(self):
        root = tk.Tk()
        stock_program = StockSystem(root)
        root.mainloop()