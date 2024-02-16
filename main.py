import tkinter as tk
from login import Login


def main():
    root = tk.Tk()
    login_app = Login(root)
    root.mainloop()


if __name__ == "__main__":
    main()