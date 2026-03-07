import tkinter as tk
from tkinter import messagebox
import json

file_name = "contacts.json"


# Load contacts from file
def load_contacts():
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except:
        return []


# Save contacts
def save_contacts():
    with open(file_name, "w") as f:
        json.dump(contacts, f)


# Add contact
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    if name == "" or phone == "" or email == "":
        messagebox.showwarning("Input error", "Please fill all fields")
        return

    contact = {"name": name, "phone": phone, "email": email}
    contacts.append(contact)

    save_contacts()
    refresh_list()

    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


# Refresh contact list
def refresh_list():
    listbox.delete(0, tk.END)
    for c in contacts:
        listbox.insert(tk.END, f"{c['name']} | {c['phone']} | {c['email']}")


# Delete contact
def delete_contact():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Select", "Select a contact first")
        return

    contacts.pop(selected[0])
    save_contacts()
    refresh_list()


# Edit contact
def edit_contact():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Select", "Select a contact first")
        return

    index = selected[0]

    contacts[index]["name"] = name_entry.get()
    contacts[index]["phone"] = phone_entry.get()
    contacts[index]["email"] = email_entry.get()

    save_contacts()
    refresh_list()


# ---------------- GUI ---------------- #

contacts = load_contacts()

root = tk.Tk()
root.title("Contact Manager")
root.geometry("600x500")
root.configure(bg="#f4f6f8")   # light grey background


# Title
title = tk.Label(
    root,
    text="CONTACT MANAGER",
    font=("Arial Black", 26),
    bg="#f4f6f8",
    fg="#1f3c88"   # deep blue
)
title.pack(pady=20)


# Input Frame
frame = tk.Frame(root, bg="#f4f6f8")
frame.pack(pady=10)

tk.Label(frame, text="Name", bg="#f4f6f8", font=("Arial", 11)).grid(row=0, column=0, padx=5)
name_entry = tk.Entry(frame, width=25)
name_entry.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Phone", bg="#f4f6f8", font=("Arial", 11)).grid(row=1, column=0, padx=5)
phone_entry = tk.Entry(frame, width=25)
phone_entry.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Email", bg="#f4f6f8", font=("Arial", 11)).grid(row=2, column=0, padx=5)
email_entry = tk.Entry(frame, width=25)
email_entry.grid(row=2, column=1, pady=5)


# Button Frame
btn_frame = tk.Frame(root, bg="#f4f6f8")
btn_frame.pack(pady=15)

btn_style = {
    "bg": "#1f3c88",   # blue button
    "fg": "white",
    "width": 12,
    "font": ("Arial", 10, "bold")
}

tk.Button(btn_frame, text="Add", command=add_contact, **btn_style).grid(row=0, column=0, padx=6)
tk.Button(btn_frame, text="Edit", command=edit_contact, **btn_style).grid(row=0, column=1, padx=6)
tk.Button(btn_frame, text="Delete", command=delete_contact, **btn_style).grid(row=0, column=2, padx=6)


# Contact List
listbox = tk.Listbox(
    root,
    width=70,
    height=15,
    bg="white",
    fg="black",
    font=("Arial", 10)
)
listbox.pack(pady=10)

refresh_list()

root.mainloop()
