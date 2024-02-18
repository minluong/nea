import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class StockSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock System")
        self.conn = sqlite3.connect("stock_database.db")
        self.create_table()

        # Entry fields on the left
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(self.entry_frame, text="Product Name:").grid(row=0, column=0, padx=10, pady=3)
        self.product_name_entry = tk.Entry(self.entry_frame)
        self.product_name_entry.grid(row=0, column=1, padx=10, pady=3)

        tk.Label(self.entry_frame, text="Quantity:").grid(row=1, column=0, padx=10, pady=3)
        self.quantity_entry = tk.Entry(self.entry_frame)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=3)

        tk.Label(self.entry_frame, text="Price:").grid(row=2, column=0, padx=10, pady=3)
        self.price_entry = tk.Entry(self.entry_frame)
        self.price_entry.grid(row=2, column=1, padx=10, pady=3)

        tk.Label(self.entry_frame, text="Total:").grid(row=3, column=0, padx=10, pady=3)
        self.total_entry = tk.Entry(self.entry_frame, state="readonly")
        self.total_entry.grid(row=3, column=1, padx=10, pady=3)

        ttk.Button(self.entry_frame, text="Submit", command=self.submit_form).grid(row=4, column=0, columnspan=2, pady=10, padx=10)
        ttk.Button(self.root, text="Edit", command=self.edit_record).grid(row=1, column=0, pady=10, padx=5)

        # Remove button
        ttk.Button(self.root, text="Remove", command=self.remove_record).grid(row=1, column=1, pady=10, padx=5)

        # OK button for saving edits (initially hidden)
        self.ok_button = ttk.Button(self.entry_frame, text="OK", command=self.save_record)
        self.ok_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10)
        self.ok_button.grid_remove()  # Hide the OK button initially

        # Set entry validation
        self.quantity_entry.configure(validate="key", validatecommand=(self.root.register(self.validate_quantity), '%P'))
        self.price_entry.configure(validate="key", validatecommand=(self.root.register(self.validate_price), '%P'))

        # Treeview on the right
        self.tree = ttk.Treeview(self.root, columns=("Product Name", "Quantity", "Price", "Total"), show="headings")
        self.tree.grid(row=0, column=1, columnspan=3, pady=10)

        columns_and_weights = {
            "Product Name": 100,
            "Quantity": 80,
            "Price": 70,
            "Total": 80
        }

        for col, weight in columns_and_weights.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=weight)

        style = ttk.Style()
        style.configure("Treeview", rowheight=20, font=('Calibri', 10))
        style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'))
        style.map("Treeview", background=[('selected', '#ececec')])

        self.populate_treeview()

    def validate_quantity(self, new_value):
        try:
            if new_value:
                int(new_value)
            return True
        except ValueError:
            return False

    def validate_price(self, new_value):
        try:
            if new_value:
                float(new_value)
            return True
        except ValueError:
            return False

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS stock_data (
            product_name TEXT,
            quantity INTEGER,
            price REAL,
            total REAL
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def submit_form(self):
        if not all([self.product_name_entry.get(), self.quantity_entry.get(), self.price_entry.get()]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        product_name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        # Calculate total
        total = float(quantity) * float(price)

        query = '''
        INSERT INTO stock_data (product_name, quantity, price, total)
        VALUES (?, ?, ?, ?)
        '''
        values = (product_name, quantity, price, total)

        self.conn.execute(query, values)
        self.conn.commit()

        print("Data inserted into the database:", values)  # Print the inserted values for debugging

        self.populate_treeview()

    def remove_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            product_name = self.tree.item(selected_item, "values")[0]
            query = 'DELETE FROM stock_data WHERE product_name = ?'
            self.conn.execute(query, (product_name,))
            self.conn.commit()

            print("Record with Product Name", product_name, "removed from the database.")

            self.populate_treeview()
        else:
            print("Please select a record to remove.")

    def edit_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            product_name = self.tree.item(selected_item, "values")[0]
            query = 'SELECT * FROM stock_data WHERE product_name = ?'
            cursor = self.conn.execute(query, (product_name,))
            record = cursor.fetchone()

            if record:
                self.product_name_entry.delete(0, tk.END)
                self.quantity_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)

                self.product_name_entry.insert(0, record[0])
                self.quantity_entry.insert(0, record[1])
                self.price_entry.insert(0, record[2])

                # Show Quantity entry field
                tk.Label(self.entry_frame, text="Quantity:").grid(row=1, column=0, padx=10, pady=3)
                self.quantity_entry.grid(row=1, column=1, padx=10, pady=3)

                # Hide Total entry field
                tk.Label(self.entry_frame, text="Total:").grid_forget()
                self.total_entry.grid_forget()

                # Hide Submit button and show OK button
                ttk.Button(self.entry_frame, text="Submit", command=self.submit_form).grid_forget()
                self.ok_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10)  # Show the OK button

                print("Editing record with Product Name", product_name)
        else:
            print("Please select a record to edit.")

    def save_record(self):
        product_name = self.product_name_entry.get()
        query = 'UPDATE stock_data SET quantity=?, price=?, total=? WHERE product_name=?'
        values = (
            int(self.quantity_entry.get()),
            float(self.price_entry.get()),
            int(self.quantity_entry.get()) * float(self.price_entry.get()),
            product_name
        )

        self.conn.execute(query, values)
        self.conn.commit()

        print("Record with Product Name", product_name, "saved.")

        # Show Submit button and hide OK button
        ttk.Button(self.entry_frame, text="Submit", command=self.submit_form).grid(row=4, column=0, columnspan=2, pady=10, padx=10)
        self.ok_button.grid_forget()  # Hide the OK button

        self.populate_treeview()

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