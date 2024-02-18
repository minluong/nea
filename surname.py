import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class SurnameEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Surname Editor")
        self.create_widgets()
        self.conn = sqlite3.connect("surname_database.db")
        self.create_table()
        self.populate_listbox()

    def create_widgets(self):
        self.surname_listbox = tk.Listbox(self.root)
        self.surname_listbox.pack(padx=10, pady=10)

        self.new_surname_entry = tk.Entry(self.root)
        self.new_surname_entry.pack(pady=5)

        tk.Button(self.root, text="Add Surname", command=self.add_surname).pack(pady=5)

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS surname_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            surname TEXT
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_surname(self):
        new_surname = self.new_surname_entry.get()
        if new_surname:
            query = 'INSERT INTO surname_data (surname) VALUES (?)'
            self.conn.execute(query, (new_surname,))
            self.conn.commit()
            self.new_surname_entry.delete(0, tk.END)
            self.populate_listbox()
            messagebox.showinfo("Information", "Surname added successfully.")
        else:
            messagebox.showinfo("Information", "Please enter a Surname.")

    def populate_listbox(self):
        self.surname_listbox.delete(0, tk.END)
        query = 'SELECT * FROM surname_data'
        cursor = self.conn.execute(query)
        for row in cursor.fetchall():
            self.surname_listbox.insert(tk.END, row[1])

if __name__ == "__main__":
    root = tk.Tk()
    app = SurnameEditor(root)
    root.mainloop()
