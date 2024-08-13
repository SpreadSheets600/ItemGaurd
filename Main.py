import sqlite3
import os
import qrcode
from datetime import datetime

QR_DIR = "Codes"
os.makedirs(QR_DIR, exist_ok=True)

DB_FILE = "ItemData.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_name TEXT NOT NULL,
                        label_id TEXT NOT NULL UNIQUE,
                        date_added TEXT NOT NULL,
                        date_used TEXT
                      )''')
    conn.commit()
    conn.close()

def generate_qr(label_id):

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(label_id)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    qr_path = os.path.join(QR_DIR, f"{label_id}.png")
    img.save(qr_path)
    print(f"+ QR Code Saved To {qr_path}")

def add_item(item_name):

    label_id = f"{item_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    generate_qr(label_id)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO items (item_name, label_id, date_added) 
                      VALUES (?, ?, ?)''', (item_name, label_id, date_added))
    conn.commit()
    conn.close()

    print(f"+ Item '{item_name}' Added With Label ID '{label_id}'.")

def record_usage(label_id):

    date_used = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''UPDATE items SET date_used = ? WHERE label_id = ?''', (date_used, label_id))
    conn.commit()
    conn.close()

    print(f"+ Usage Recorded For Label ID '{label_id}' At {date_used}.")

def view_items():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''SELECT item_name, label_id, date_added, date_used FROM items''')
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        print(row)

if __name__ == "__main__":
    init_db()

    while True:
        print("+ 1. Add Item")
        print("+ 2. View Items")
        print("+ 3. Record Usage")
        print("+ 4. Exit")
        choice = input("\n+ Enter Your Choice : ")

        if choice == "1":
            item_name = input("\n + Enter The Item Name : ")
            add_item(item_name)

        elif choice == "3":
            label_id = input("\n + Enter The Label ID : ")
            record_usage(label_id)

        elif choice == "2":
            view_items()

        elif choice == "4":
            break

        else:
            print("+ Invalid Choice.\nPlease Try Again.")
