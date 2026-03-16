from tkinter import *
import os
from cryptography.fernet import Fernet
import sqlite3

from tkinter import ttk


class Vault:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("600x400")
        self.root.title("Avault")
        self.ie = 3
        self.folder = os.path.expanduser("~/.sstm")
        os.makedirs(self.folder, exist_ok=True)
        self.db_path = os.path.join(self.folder, "mydatabase.db")
        self.key_path = os.path.expanduser("~/.sstm/keyp.key")

        if not os.path.exists(self.key_path):
            self.key = Fernet.generate_key()
            with open(self.key_path, "wb") as f:
                f.write(self.key)
        else:
            with open(self.key_path, "rb") as f:
                self.key = f.read()


        self.cipher = Fernet(self.key)
        self.main_menu()
        self.init_db()

    def run(self):
        self.root.mainloop()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Email TEXT NOT NULL,
                Password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    def main_menu(self):
        self.la1 = Label(self.root, text="Enter password")
        self.la1.pack(pady=20)

        self.en1 = Entry(self.root, show="*")
        self.en1.pack(pady=10)

        self.bs1 = Button(self.root, text="Enter", command=self.get_entry)
        self.bs1.pack(pady=10)

    def get_entry(self):
        self.paswd = self.en1.get()
        if self.paswd == "":
            self.la1.config(text="Password cannot be empty")
            return
        self.shfra()

    def shfra(self):
        folder = os.path.expanduser("~/.sstm")
        os.makedirs(folder, exist_ok=True)

        path = os.path.join(folder, "passwd.txt")
        key_path = os.path.join(folder, "key.key")

        if not os.path.exists(key_path):
            key = Fernet.generate_key()
            with open(key_path, "wb") as f:
                f.write(key)
        else:
            with open(key_path, "rb") as f:
                key = f.read()

        cipher = Fernet(key)

        if not os.path.exists(path):
            encrypted = cipher.encrypt(self.paswd.encode())
            with open(path, "wb") as f:
                f.write(encrypted)
            print("Password saved")
            self.open_vault()
            return

        with open(path, "rb") as f:
            saved = f.read()

        decrypted = cipher.decrypt(saved).decode()

        if self.paswd == decrypted:
            self.open_vault()
            self.ie = 3
        else:
            self.ie -= 1
            self.la1.config(text=f"Wrong password - {self.ie} tries left")
            if self.ie == 0:
                if os.path.exists(folder):
                    os.system(f"rm -rf {folder}")
                self.la1.config(text="Vault reset!")
                self.ie = 3

    def get_Email(self):
        self.email = self.ENTRY_EMAIL.get()
        self.passwd = self.ENTRY_PASSWORD.get()
        enc_email = self.cipher.encrypt(self.email.encode())
        enc_pass = self.cipher.encrypt(self.passwd.encode())

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        if self.email and self.passwd:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("INSERT INTO users (Email, Password) VALUES (?, ?)", (enc_email, enc_pass))
            self.conn.commit()
            self.conn.close()
            self.ENTRY_EMAIL.delete(0, END)
            self.ENTRY_PASSWORD.delete(0, END)
        else:
            print("")
    def open_vault(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        def show(frame):
            frame.lift()

        self.con = Frame(self.root)
        self.con.pack(fill=BOTH, expand=True)

        self.top_bar = Frame(self.con, bg="#ddd", height=35)
        self.top_bar.place(relx=0, rely=0, relwidth=1)

        frame_y = 35 / 400

        self.add_frame = Frame(self.con, bg="lightblue")
        Label(self.add_frame,text="",bg="lightblue").pack()
        Label(self.add_frame,text="Email",bg="lightblue").pack()
        Label(self.add_frame, text="",bg="lightblue").pack()
        self.ENTRY_EMAIL = (Entry(self.add_frame))
        self.ENTRY_EMAIL.pack()
        Label(self.add_frame, text="",bg="lightblue").pack()
        Label(self.add_frame, text="Password",bg="lightblue").pack()
        Label(self.add_frame, text="",bg="lightblue").pack()
        self.ENTRY_PASSWORD = (Entry(self.add_frame,show="*"))
        self.ENTRY_PASSWORD.pack()
        Button(self.add_frame, text="submit", command=self.get_Email).pack()


        self.show_frame = Frame(self.con, bg="lightgreen")
        columns = ("ID", "Email", "Password")
        self.tree = ttk.Treeview(self.show_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=BOTH, expand=True)

        def update_tree():
            self.tree.delete(*self.tree.get_children())
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            conn.close()
            if not rows:
                print("No data to show!")
                return
            for row in rows:
                dec_email = self.cipher.decrypt(row[1]).decode()
                dec_pass = self.cipher.decrypt(row[2]).decode()
                self.tree.insert("", END, values=(row[0], dec_email, dec_pass))

        self.delete_frame = Frame(self.con, bg="lightcoral")

        def delete_row():
            selected_item = self.tree.selection()
            if not selected_item:
                print("No row selected!")
                return
            values = self.tree.item(selected_item, "values")
            row_id = values[0]
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (row_id,))
            conn.commit()
            conn.close()
            self.tree.delete(selected_item)
        for f in (self.add_frame, self.show_frame, self.delete_frame):
            f.place(relx=0, rely=frame_y, relwidth=1, relheight=1-frame_y)
        Button(self.delete_frame, text="Delete Selected", command=delete_row).pack(pady=20)
        Button(self.top_bar, text="Insert", command=lambda: show(self.add_frame)).pack(side="left")
        Button(self.top_bar, text="Show", command=lambda: [show(self.show_frame), update_tree()]).pack(side="left")
        Button(self.top_bar, text="Remove", command=lambda: show(self.delete_frame)).pack(side="left")


#mi_bombo

        show(self.add_frame)


app = Vault()
app.run()
