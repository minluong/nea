import tkinter as tk
from tkinter import ttk
import sqlite3


class StockSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock System")
        self.create_stock_widgets()
        self.conn = sqlite3.connect("stock_database.db")
        self.create_table()
        self.tree = ttk.Treeview(self.root, columns=("ID", "Product Name", "Stock Level", "Reorder Level", "Forename", "Surname", "Address", "Total"), show = "headings")
        self.tree.grid(row = 8, column = 0, columnspan = 2, pady = 10)
        columns_and_weights = {
            "ID": 30,
            "Product Name": 100,
            "Stock Level": 90,
            "Reorder Level": 100,
            "Forename": 80,
            "Surname": 70,
            "Address": 150,
            "Total": 80
        }


        for col, weight in columns_and_weights.items():
            self.tree.heading(col, text = col)
            self.tree.column(col, width = weight)


        style = ttk.Style()
        style.configure("Treeview", rowheight = 20, font = ('Calibri', 10))
        style.configure("Treeview.Heading", font = ('Calibri', 10, 'bold'))


        style.map("Treeview", background = [('selected', '#ececec')])


        self.tree.insert("", "end", values = ("", "", "", "", "", "", ""))


        self.populate_treeview()


    def create_stock_widgets(self):
        tk.Label(self.root, text = "Product Name:").grid(row = 0, column = 0, padx = 10, pady = 3)
        self.product_name_entry = tk.Entry(self.root)
        self.product_name_entry.grid(row = 0, column = 1, padx = 10, pady = 3)


        tk.Label(self.root, text = "Stock Level:").grid(row = 1, column = 0, padx = 10, pady = 3)
        self.stock_level_entry = tk.Entry(self.root)
        self.stock_level_entry.grid(row = 1, column = 1, padx = 10, pady = 3)


        tk.Label(self.root, text = "Reorder Level:").grid(row = 2, column = 0, padx = 10, pady = 3)
        self.reorder_level_entry = tk.Entry(self.root)
        self.reorder_level_entry.grid(row = 2, column = 1, padx = 10, pady = 3)


        tk.Label(self.root, text = "Forename:").grid(row = 3, column = 0, padx = 10, pady = 3)
        self.forename_entry = tk.Entry(self.root)
        self.forename_entry.grid(row = 3, column = 1, padx = 10, pady = 3)


        tk.Label(self.root, text = "Surname:").grid(row = 4, column = 0, padx = 10, pady = 3)
        self.surname_entry = tk.Entry(self.root)
        self.surname_entry.grid(row = 4, column = 1, padx = 10, pady = 3)


        tk.Label(self.root, text = "Delivery Address:").grid(row = 5, column = 0, padx = 10, pady = 3)
        self.address_entry = tk.Entry(self.root)
        self.address_entry.grid(row = 5, column = 1, padx = 10, pady = 3)


        tk.Label(self.root, text = "Total:").grid(row = 6, column = 0, padx = 10, pady = 3)
        self.total_entry = tk.Entry(self.root)
        self.total_entry.grid(row = 6, column = 1, padx = 10, pady = 3)


        ttk.Button(self.root, text = "Submit", command = self.submit_form).grid(row = 7, column = 0, columnspan = 2, pady = 10, padx = 10)
        ttk.Button(self.root, text = "Remove", command = self.remove_record).grid(row = 9, column = 0, columnspan = 2, pady = 10, padx = 10)


    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS stock_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            stock_level INTEGER,
            reorder_level INTEGER,
            forename TEXT,
            surname TEXT,
            address TEXT,
            total REAL
        )
        '''
        self.conn.execute(query)
        self.conn.commit()


    def submit_form(self):
        product_name = self.product_name_entry.get()
        stock_level = self.stock_level_entry.get()
        reorder_level = self.reorder_level_entry.get()
        forename = self.forename_entry.get()
        surname = self.surname_entry.get()
        address = self.address_entry.get()
        total = self.total_entry.get()


        query = '''
        INSERT INTO stock_data (product_name, stock_level, reorder_level, forename, surname, address, total)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        values = (product_name, stock_level, reorder_level, forename, surname, address, total)


        self.conn.execute(query, values)
        self.conn.commit()


        print("Data inserted into the database.")


        self.populate_treeview()


    def remove_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            record_id = self.tree.item(selected_item, "values")[0]
            query = 'DELETE FROM stock_data WHERE id = ?'
            self.conn.execute(query, (record_id,))
            self.conn.commit()


            print("Record with ID", record_id, "removed from the database.")


            self.populate_treeview()
        else:
            print("Please select a record to remove.")


    def populate_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)


        query = 'SELECT * FROM stock_data'
        cursor = self.conn.execute(query)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)


if __name__ == "__main__":
    root = tk.Tk()
    app = StockSystem(root)
    root.mainloop()


