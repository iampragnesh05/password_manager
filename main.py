import tkinter as tk
from email.policy import default
from tkinter import font, messagebox, simpledialog
from PIL import  Image, ImageTk
import random
import pyperclip  # Import pyperclip for clipboard functionality
import json
import os

default_email = None;
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
def generate_password():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = "".join(password_list)
    return password

def on_generate_password():
    # Generate random password
    password = generate_password()
    # Set the password into the password entry field
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    # Copy the password to the clipboard
    pyperclip.copy(password)
    print(f"Password {password} copied to clipboard.")
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if website and email and password:
        data_line = {website: {"email": email, "password": password}}

        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        except json.JSONDecodeError:
            # If there's an error decoding JSON (e.g., if the file is corrupted), also start fresh
            messagebox.showerror("Error", "Data file is corrupted. Starting with a new file.")
            data = {}

        data.update(data_line)

        try:
            # Save the updated data back to the file
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
            confirmation = messagebox.askquestion(
                "Data Saved",
                f"Details Saved Successfully!\n\nWebsite: {website}\nEmail: {email}\nPassword: {password}\n\nIs this correct?",
            )
            # If the user clicks 'Yes', clear the fields; otherwise, keep them filled
            if confirmation == 'yes':
                website_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
            else:
                print("Details not saved.")
        except IOError:
            messagebox.showerror("Error", "Please fill in all fields.")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")


def search_data():
    website = website_entry.get().strip()
    if website:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo("Error", "No data file found.")
            return
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Data file is corrupted.")
            return

        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo("Search Result", f"Website: {website}\nEmail: {email}\nPassword: {password}")
        else:
            messagebox.showinfo("Search Result", f"No data found for '{website}'.")
    else:
        messagebox.showwarning("Input Error", "Please enter a website name to search.")

def prompt_for_default_email():
    global default_email
    if default_email is None:
        default_email = simpledialog.askstring("Set Default Email", "Enter default email/username:")
        if default_email:
            email_entry.insert(0, default_email)
        else:
            default_email = ""


# ---------------------------- UI SETUP ------------------------------- #
root = tk.Tk()
root.title("Password Manager.")
root.configure(bg="white")  # Set main window background to white

label_font = font.Font(family="Helvetica", size=12, weight="bold")
button_font = font.Font(family="Helvetica", size=10, weight="bold")


# Define dimensions and padding for the image
canvas_width = 200
canvas_height = 200
padding = 20

root.columnconfigure([0, 1, 2], weight=1, minsize=100)
root.rowconfigure([0, 1, 2, 3, 4], weight=1, minsize=50)

image_path = "logo.png"
canvas = tk.Canvas(root, width=canvas_width + 2 * padding, height=canvas_height + 2 * padding, bg="white", highlightthickness=0)
canvas.grid(row=0, column=1)

original_image = Image.open(image_path)
resized_image = original_image.resize((canvas_width, canvas_height))
tk_image = ImageTk.PhotoImage(resized_image)

canvas.create_image(padding, padding, anchor=tk.NW, image=tk_image)


# 2. Website text and input (second row)
website_label = tk.Label(root, text="Website:", bg="white", font=label_font, fg="black")
website_label.grid(row=1, column=0, sticky="e", padx=5)
website_entry = tk.Entry(root, width=35, font=("Arial", 10))
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=2)

search_button = tk.Button(root, text="Search", font=button_font, bg="#2196F3", fg="white", command=search_data)
search_button.grid(row=1, column=2, padx=5, sticky="w")

# 3. Email/Username text and input (third row)
email_label = tk.Label(root, text="Email/Username:", bg="white", font=label_font, fg="black")
email_label.grid(row=2, column=0, sticky="e", padx=5)
email_entry = tk.Entry(root, width=35, font=("Arial", 10))
email_entry.grid(row=2, column=1, sticky="w", padx=5, pady=2)

# 4. Password text, input, and Generate button (fourth row)
password_label = tk.Label(root, text="Password:", bg="white", font=label_font, fg="black")
password_label.grid(row=3, column=0, sticky="e", padx=5)
password_entry = tk.Entry(root, font=("Arial", 10), width=35)
password_entry.grid(row=3, column=1, sticky="w", padx=5, pady=2)
generate_button = tk.Button(root, text="Generate Password", font=button_font, bg="#4CAF50", fg="white", command=on_generate_password)
generate_button.grid(row=3, column=2, padx=5)

# 5. Add button (fifth row)
add_button = tk.Button(root, text="Add", width=36, font=button_font, bg="white", fg="black", command=save_data)
add_button.grid(row=4, column=1, columnspan=2, pady=10)

root.after(100, prompt_for_default_email)
root.mainloop()
