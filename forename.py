import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ForenameEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Forename Editor")
        self.create_widgets()
        self.conn = sqlite3.connect("forename_database.db")
        self.create_table()
        self.populate_listbox()

    def create_widgets(self):
        self.forename_listbox = tk.Listbox(self.root)
        self.forename_listbox.pack(padx=10, pady=10)

        self.new_forename_entry = tk.Entry(self.root)
        self.new_forename_entry.pack(pady=5)

        tk.Button(self.root, text="Add Forename", command=self.add_forename).pack(pady=5)

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS forename_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            forename TEXT
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_forename(self):
        new_forename = self.new_forename_entry.get()
        if new_forename:
            query = 'INSERT INTO forename_data (forename) VALUES (?)'
            self.conn.execute(query, (new_forename,))
            self.conn.commit()
            self.new_forename_entry.delete(0, tk.END)
            self.populate_listbox()
            messagebox.showinfo("Information", "Forename added successfully.")
        else:
            messagebox.showinfo("Information", "Please enter a Forename.")

    def populate_listbox(self):
        self.forename_listbox.delete(0, tk.END)
        query = 'SELECT * FROM forename_data'
        cursor = self.conn.execute(query)
        for row in cursor.fetchall():
            self.forename_listbox.insert(tk.END, row[1])

if __name__ == "__main__":
    root = tk.Tk()
    app = ForenameEditor(root)
    root.mainloop()
