import tkinter as tk
from tkinter import messagebox
import sqlite3 as sdb
import webbrowser
import pyperclip
from tkinter import filedialog

Contacts = tk.Tk()
Contacts.title("Contacts Book")
Contacts.geometry('650x300')
background = '#121212'
Contacts.config(bg=background)
first_name_inp = tk.StringVar()
last_name_inp = tk.StringVar()
phone_inp = tk.StringVar()
email_inp = tk.StringVar()

listbox = tk.Listbox(Contacts, width=50, height=16)

def communication(interface, *args):
    con = sdb.connect('Contacts.db')
    cur = con.cursor()
    cur.execute(interface, args)
    data = cur.fetchall()
    con.commit()
    con.close()
    return data

def create():
    interface = "CREATE TABLE IF NOT EXISTS CONTACT(id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, phone TEXT, email TEXT)"
    communication(interface)

create()

def insert():
    data = add_info()
    interface = "INSERT INTO CONTACT(first_name, last_name, phone, email) VALUES (?, ?, ?, ?)"
    communication(interface, *data)

def delete():
    selected_contact = listbox.get(tk.ANCHOR)
    contact_id = selected_contact.split(':')[0].strip()
    interface = "DELETE FROM CONTACT WHERE id=?"
    communication(interface, contact_id)

def add_info():
    string_add = first_name_entry.get() + ' ' + last_name_entry.get() + ': ' + phone_entry.get() + ' , ' + email_entry.get()
    listbox.insert(tk.END, string_add)
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    return (first_name_entry.get(), last_name_entry.get(), phone_entry.get(), email_entry.get())

def save_info():
    with open('saved.txt', 'w') as file:
        list_tuple = listbox.get(0, tk.END)
        for i in list_tuple:
            if i.endswith('\n'):
                file.write(i)
            else:
                file.write(i + '\n')

save_info()

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            file_content = file.readlines()  # Read all lines from the file

        # Clear the listbox before adding new content
        listbox.delete(0, tk.END)

        # Insert the file content into the listbox
        for line in file_content:
            listbox.insert(tk.END, line.strip())  # Add each line to the listbox

def delete_info():
    choice = messagebox.askquestion('Delete Contact', "Are you sure you want to delete the contact?")
    if choice == 'yes':
        listbox.delete(tk.ANCHOR)
    else:
        return
    
def copy_info():
    selected_contact = listbox.get(tk.ACTIVE)  # Use tk.ACTIVE to get the active selection
    contact_parts = selected_contact.split(': ')
    if len(contact_parts) > 1:
        phone_email_parts = contact_parts[1].split(' , ')
        if len(phone_email_parts) > 0:
            phone_number = phone_email_parts[0].strip()
            pyperclip.copy(phone_number)


def exit_app():
    choice = messagebox.askquestion('Exit Application', "Are you sure you want to close the application?")
    if choice == 'yes':
        Contacts.destroy()
    else:
        return

# Function to create labels
def create_label(text, row, column):
    label = tk.Label(Contacts, text=text, bg=background, fg="white", font=('Calibri', 12), anchor='w', justify='left')
    label.grid(row=row, column=column, padx=15, pady=5, sticky='w')
    return label

# Function to create entry fields
def create_entry(textvariable, row, column):
    entry = tk.Entry(Contacts, bg='white', fg=background, textvariable=textvariable, width=30, borderwidth=2)
    entry.grid(row=row, column=column, padx=10, pady=5, sticky='ew')
    return entry

# Function to create buttons
def create_button(text, command, row, column, columnspan):
    button = tk.Button(Contacts, text=text, command=command, bg=background, fg='white', borderwidth=3)
    button.grid(row=row, column=column, columnspan=columnspan, padx=10, pady=5, sticky='ew')
    return button

# Create labels
first_name_label = create_label("First name:", 1, 0)  # Changed row position from 0 to 1
last_name_label = create_label("Last name: ", 2, 0)   # Row position remains the same
phone_label = create_label("Phone:       ", 3, 0)
email_label = create_label("Email:        ", 4, 0)
# Create entry fields
first_name_entry = create_entry(first_name_inp, 1 , 1)  # Changed row position from 0 to 1
last_name_entry = create_entry(last_name_inp, 2, 1)    # Row position remains the same
phone_entry = create_entry(phone_inp, 3, 1)
email_entry = create_entry(email_inp, 4, 1)
# Create buttons
add_button = create_button("Add Contact", add_info, 5, 0, 2)
delete_button = create_button("Delete Contact", delete_info, 6, 0, 2)
save_button = create_button("Save List", save_info, 7, 0, 2)
copy_button = create_button("Copy Phone Number", copy_info, 8, 0, 2)
open_button = create_button("Open Saved File", open_file, 9, 0, 2)
exit_button = create_button("Exit App", exit_app, 10, 0, 2)
listbox.grid(row=0, column=2, rowspan=10, padx=10, pady=5, sticky='nsew')
Contacts.grid_rowconfigure(0, weight=1)
Contacts.grid_columnconfigure(2, weight=1)

Contacts.mainloop()
