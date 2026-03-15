import tkinter as tk
from tkinter import messagebox
import json

file_name = "contacts.json"
selected_index = None


# ---------- File Handling ---------- #

def load_contacts():
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except:
        return []


def save_contacts():
    with open(file_name, "w") as f:
        json.dump(contacts, f, indent=4)


# ---------- Functions ---------- #

def clear_fields():
    global selected_index
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    selected_index = None


def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    if not name or not phone or not email:
        messagebox.showwarning("Input Error", "Fill all fields")
        return

    contacts.append({"name": name, "phone": phone, "email": email})
    save_contacts()
    refresh_cards()
    clear_fields()


def edit_contact():
    global selected_index

    if selected_index is None:
        messagebox.showwarning("Select", "Select a contact card first")
        return

    contacts[selected_index]["name"] = name_entry.get()
    contacts[selected_index]["phone"] = phone_entry.get()
    contacts[selected_index]["email"] = email_entry.get()

    save_contacts()
    refresh_cards()
    clear_fields()


def delete_contact(index):
    confirm = messagebox.askyesno("Delete", "Delete this contact?")
    if confirm:
        contacts.pop(index)
        save_contacts()
        refresh_cards()
        clear_fields()


def select_contact(index):
    global selected_index
    selected_index = index

    contact = contacts[index]

    clear_fields()

    name_entry.insert(0, contact["name"])
    phone_entry.insert(0, contact["phone"])
    email_entry.insert(0, contact["email"])

    selected_index = index


def search_contact():

    keyword = search_entry.get().lower()

    if keyword == "":
        refresh_cards()
        return

    filtered = []

    for i, c in enumerate(contacts):
        if keyword in c["name"].lower() or keyword in c["phone"]:
            filtered.append((i, c))

    refresh_cards(filtered)


# ---------- Card UI ---------- #

def refresh_cards(data=None):

    for widget in card_frame.winfo_children():
        widget.destroy()

    if data is None:
        display = list(enumerate(contacts))
    else:
        display = data

    if len(display) == 0:
        tk.Label(
            card_frame,
            text="No contacts found 😅",
            font=("Arial", 14),
            bg="#eef2f7"
        ).pack(pady=20)
        return

    for index, c in display:

        card = tk.Frame(
            card_frame,
            bg="white",
            bd=1,
            relief="solid",
            padx=10,
            pady=10
        )

        card.pack(pady=8, padx=20, fill="x")

        card.bind("<Button-1>", lambda e, x=index: select_contact(x))

        name = tk.Label(card, text=c["name"], font=("Arial", 14, "bold"), bg="white")
        name.grid(row=0, column=0, sticky="w")

        phone = tk.Label(card, text="📞 " + c["phone"], bg="white")
        phone.grid(row=1, column=0, sticky="w")

        email = tk.Label(card, text="✉ " + c["email"], bg="white")
        email.grid(row=2, column=0, sticky="w")

        delete_btn = tk.Button(
            card,
            text="Delete",
            bg="#e74c3c",
            fg="white",
            command=lambda x=index: delete_contact(x)
        )

        delete_btn.grid(row=0, column=1, rowspan=3, padx=10)


# ---------- GUI ---------- #

contacts = load_contacts()

root = tk.Tk()
root.title("Contact Manager")
root.geometry("700x600")
root.configure(bg="#eef2f7")


tk.Label(
    root,
    text="📇 Contact Manager",
    font=("Arial Black", 24),
    bg="#eef2f7",
    fg="#1f3c88"
).pack(pady=15)


# Search
search_frame = tk.Frame(root, bg="#eef2f7")
search_frame.pack()

search_entry = tk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=0, padx=5)

tk.Button(
    search_frame,
    text="Search",
    bg="#1f3c88",
    fg="white",
    command=search_contact
).grid(row=0, column=1)


# Input
input_frame = tk.Frame(root, bg="#eef2f7")
input_frame.pack(pady=15)

tk.Label(input_frame, text="Name", bg="#eef2f7").grid(row=0, column=0)
name_entry = tk.Entry(input_frame, width=30)
name_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Phone", bg="#eef2f7").grid(row=1, column=0)
phone_entry = tk.Entry(input_frame, width=30)
phone_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Email", bg="#eef2f7").grid(row=2, column=0)
email_entry = tk.Entry(input_frame, width=30)
email_entry.grid(row=2, column=1)


# Buttons
btn_frame = tk.Frame(root, bg="#eef2f7")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", width=12, bg="#1f3c88", fg="white", command=add_contact).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Edit", width=12, bg="#27ae60", fg="white", command=edit_contact).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Clear", width=12, bg="#7f8c8d", fg="white", command=clear_fields).grid(row=0, column=2, padx=5)


# Scrollable cards
canvas = tk.Canvas(root, bg="#eef2f7")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

card_frame = tk.Frame(canvas, bg="#eef2f7")

card_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=card_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


refresh_cards()

root.mainloop()
