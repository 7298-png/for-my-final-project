
#here i am going discuss about most important part for my app and those are:tkinter,messagebox,json and os.
import tkinter as tk
from tkinter import messagebox
import json
import os

# Load and save it in memory
# this part is for just save the data of users and after registration while i am back to log in i just need to give him the details and i will be abale to log in again.
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

# changing the color style and font style 
# while we will be able to run our app then you can find this important things like color configuaration and font style 
BG_COLOR = "#f2e9f7"
BTN_COLOR = "#d291bc"
FONT_BIG = ("Arial", 20)
FONT_NORMAL = ("Arial", 16)
FONT_SMALL = ("Arial", 14)

# Register and Login for Functions
# this is the first step to entry app where if the user data has already saved then just have to give the correct information to the app and do the log in or if we dont have any saved data before so we register as a new user and save it as before .
def register_user():
    username = entry_user.get()
    password = entry_password.get()
    if username and password:
        data = load_data()
        if username in data:
            messagebox.showerror("Error", "User already exists!")
        else:
            data[username] = {"password": password, "info": {}}
            save_data(data)
            messagebox.showinfo("Success", "User Registered!")
    else:
        messagebox.showerror("Error", "Please enter username and password!")

def login_user():
    username = entry_user.get()
    password = entry_password.get()
    data = load_data()
    if username in data and data[username]["password"] == password:
        messagebox.showinfo("Success", "Login Successful!")
        open_dashboard(username)
    else:
        messagebox.showerror("Error", "Invalid Credentials!")

# Dashboard for Function
# after log in there will be a different background and other things and this is actually called dashboard .
def open_dashboard(username):
    login_window.destroy()
    dashboard_window = tk.Tk()
    dashboard_window.title("Dashboard")
    dashboard_window.configure(bg=BG_COLOR)

    tk.Label(dashboard_window, text="I AM WELCOMING YOU !", font=FONT_BIG, bg=BG_COLOR).pack(pady=20)
#at the previous stage there was no viewing section now i just added the viewing section so while we make a log in then you can see our saved details that we have saved .
    buttons = [
        ("View My Info", view_saved_data),
        ("Add Bank Details", add_bank_details),
        ("Add Extra Information", add_extra_info),
        ("Add Emergency Info", add_emergency_info),
        ("Add Notes", add_notes),
        ("Add User Data", add_user_data),
        ("Logout", dashboard_window.destroy)
    ]

    for text, command in buttons:
        tk.Button(dashboard_window, text=text, command=lambda cmd=command: cmd(username),
                  font=FONT_NORMAL, bg=BTN_COLOR, fg="white").pack(pady=10, ipadx=10, ipady=5)

    dashboard_window.mainloop()

# creating and renewable info window generate
def create_info_window(title, labels_entries, save_callback):
    window = tk.Toplevel()
    window.title(title)
    entries = {}
    for label_text in labels_entries:
        tk.Label(window, text=label_text, font=FONT_SMALL).pack(pady=2)
        entry = tk.Entry(window, font=FONT_SMALL)
        entry.pack()
        entries[label_text] = entry
    tk.Button(window, text="Save", command=lambda: save_callback(entries, window),
              font=FONT_NORMAL, bg=BTN_COLOR, fg="white").pack(pady=10)
    return entries

# section for viewing 
def view_saved_data(username):
    data = load_data()
    user_info = data.get(username, {}).get("info", {})

    view_window = tk.Toplevel()
    view_window.title("My Saved Information")
    view_window.configure(bg=BG_COLOR)

    canvas = tk.Canvas(view_window, bg=BG_COLOR)
    scrollbar = tk.Scrollbar(view_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
#canvas part from here 
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    tk.Label(scrollable_frame, text="My Saved Info", font=("Arial", 24, "bold"), bg=BG_COLOR).pack(pady=10)

    if not user_info:
        tk.Label(scrollable_frame, text="No saved information found.", font=FONT_NORMAL, bg=BG_COLOR).pack(pady=10)
    else:
        for section, details in user_info.items():
            tk.Label(scrollable_frame, text=section.replace("_", " ").title(), font=("Arial", 18, "underline"), bg=BG_COLOR).pack(pady=(15, 5))
            for key, value in details.items():
                tk.Label(scrollable_frame, text=f"{key.replace('_', ' ').title()}: {value}", font=FONT_SMALL, bg=BG_COLOR).pack(anchor="w", padx=20)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# Features for Functions
def add_bank_details(username):
    def save(entries, win):
        data = load_data()
        bank_details = {k.lower().replace(" ", "_").replace(":", ""): v.get() for k, v in entries.items()}
        data[username]["info"]["bank_details"] = bank_details
        save_data(data)
        messagebox.showinfo("Success", "Bank Details Saved!")
        win.destroy()

    create_info_window("Add Bank Details", [
        "Card Number:", "Expiry Date:", "Card CVV:", "Card Owner Name:"
    ], save)

def add_extra_info(username):
    def save(entries, win):
        data = load_data()
        extra_info = {k.lower().replace(" ", "_").replace(":", ""): v.get() for k, v in entries.items()}
        data[username]["info"]["extra_info"] = extra_info
        save_data(data)
        messagebox.showinfo("Success", "Extra Information Saved!")
        win.destroy()

    create_info_window("Add Extra Information", [
        "Passport Details:", "Home Address:", "Blood Group:", "Permanent Address:"
    ], save)

def add_emergency_info(username):
    def save(entries, win):
        data = load_data()
        emergency_info = {k.lower().replace(" ", "_").replace(":", ""): v.get() for k, v in entries.items()}
        data[username]["info"]["emergency_info"] = emergency_info
        save_data(data)
        messagebox.showinfo("Success", "Emergency Information Saved!")
        win.destroy()

    create_info_window("Add Emergency Info", [
        "Trustable Person Name:", "Trustable Person Contact:", "Present Address:", "Family Name:"
    ], save)

def add_notes(username):
    def save(entries, win):
        data = load_data()
        notes = {k.lower().replace(" ", "_").replace(":", ""): v.get() for k, v in entries.items()}
        data[username]["info"]["notes"] = notes
        save_data(data)
        messagebox.showinfo("Success", "Notes Saved!")
        win.destroy()

    create_info_window("Add Notes", [
        "Day Routine:", "Next Planning:", "Occasion Timing:", "Exam Timing:"
    ], save)

def add_user_data(username):
    def save(entries, win):
        data = load_data()
        user_data = {k.lower().replace(" ", "_").replace(":", ""): v.get() for k, v in entries.items()}
        data[username]["info"]["user_data"] = user_data
        save_data(data)
        messagebox.showinfo("Success", "User Data Saved!")
        win.destroy()

    create_info_window("Add User Data", [
        "Social Accounts:", "Apple/Google ID:", "Gmail:"
    ], save)

# Login for next steps Window
login_window = tk.Tk()
login_window.title("OPOP - Personal Info Storage")
login_window.configure(bg=BG_COLOR)

tk.Label(login_window, text="OPOP - Personal Info Storage", font=("Arial", 26, "bold"), bg=BG_COLOR).pack(pady=30)
tk.Label(login_window, text="Hi, I'm glad to have you again!", font=FONT_BIG, bg=BG_COLOR).pack(pady=10)

tk.Label(login_window, text="Username:", font=FONT_NORMAL, bg=BG_COLOR).pack()
entry_user = tk.Entry(login_window, font=FONT_NORMAL)
entry_user.pack(pady=5)

tk.Label(login_window, text="Password:", font=FONT_NORMAL, bg=BG_COLOR).pack()
entry_password = tk.Entry(login_window, show="*", font=FONT_NORMAL)
entry_password.pack(pady=5)

tk.Button(login_window, text="Login", command=login_user, font=FONT_NORMAL, bg=BTN_COLOR, fg="white").pack(pady=10)
tk.Button(login_window, text="Register", command=register_user, font=FONT_NORMAL, bg=BTN_COLOR, fg="white").pack(pady=10)

login_window.mainloop()
