import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from ttkthemes import ThemedTk
import pyodbc

# Database connection
connection = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-QNA2V5M\\SQLEXPRESS;'
    'Database=projectTTMS;'
    'Trusted_connection=yes;'
)
cursor = connection.cursor()

# Main Menu
def main_menu():
    root = ThemedTk(theme="arc")
    root.title("TOUR MANAGEMENT SYSTEM")
    root.geometry('1200x900')
    root['background'] = '#75142B'

    # Header section
    header_image = PhotoImage(file="header.png")  # Add a header image for aesthetics
    tk.Label(root, image=header_image, bg='#75142B').pack(pady=10)

    tk.Label(
        root,
        text="Tour Management System",
        font=('Helvetica', 30, 'bold', 'underline'),
        fg='#ffffff', bg='#75142B'
    ).pack(pady=10)

    tk.Label(
        root,
        text="Welcome to the Tour Management System!\nWe are glad to have you here.\nExcited to help you plan your tour!",
        font=('Arial', 18),
        fg='#ffffff', bg='#75142B'
    ).pack(pady=20)

    def open_packages():
        root.destroy()
        display_packages()

    def open_booking():
        root.destroy()
        booking_portal()

    def open_admin_portal():
        root.destroy()
        admin_portal()

    def open_user_portal():
        root.destroy()
        user_portal()

    ttk.Button(
        root,
        text="Tour Packages",
        command=open_packages,
        style="Main.TButton"
    ).pack(pady=10)

    ttk.Button(
        root,
        text="Book Tour",
        command=open_booking,
        style="Main.TButton"
    ).pack(pady=10)

    ttk.Button(
        root,
        text="Admin Portal",
        command=open_admin_portal,
        style="Main.TButton"
    ).pack(pady=10)

    ttk.Button(
        root,
        text="User Profile",
        command=open_user_portal,
        style="Main.TButton"
    ).pack(pady=10)

    # Style configurations
    style = ttk.Style()
    style.configure(
        "Main.TButton",
        font=('Arial', 15, 'bold'),
        foreground='#75142B',
        padding=10
    )

    root.mainloop()

# Display Packages
def display_packages():
    root = ThemedTk(theme="arc")
    root.title("TOUR PACKAGES")
    root.geometry('1200x900')
    root['background'] = '#75142B'

    tk.Label(
        root,
        text="Tour Packages",
        font=('Helvetica', 30, 'bold', 'underline'),
        fg='#ffffff', bg='#75142B'
    ).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(
        root,
        text="These are the available tour packages:",
        font=('Arial', 15, 'italic'),
        fg='#ffffff', bg='#75142B'
    ).grid(row=1, column=0, columnspan=2, pady=5)

    def fetch_packages():
        cursor.execute("SELECT package_id, package_name, package_description, package_price, package_duration FROM Tour_Package")
        return cursor.fetchall()

    packages = fetch_packages()
    for idx, package in enumerate(packages):
        tk.Label(
            root,
            text=f"Package {idx + 1}",
            font=('Arial', 15, 'bold'),
            fg='#ffffff', bg='#75142B'
        ).grid(row=2 + idx * 2, column=0, sticky='w', padx=10, pady=5)

        package_info = f"Name: {package[1]}\nDescription: {package[2]}\nPrice: {package[3]}\nDuration: {package[4]}"
        tk.Label(
            root,
            text=package_info,
            font=('Arial', 12),
            fg='#ffffff', bg='#75142B'
        ).grid(row=3 + idx * 2, column=0, sticky='w', padx=10, pady=5)

    ttk.Button(
        root,
        text="Back to Main Menu",
        command=lambda: [root.destroy(), main_menu()]
    ).grid(row=3 + len(packages) * 2, column=0, pady=10)

    root.mainloop()

# Booking Portal
def booking_portal():
    root = ThemedTk(theme="arc")
    root.title("BOOK TOUR")
    root.geometry('1000x800')
    root['background'] = '#75142B'

    tk.Label(
        root,
        text="Book Your Tour",
        font=('Helvetica', 30, 'bold', 'underline'),
        fg='#ffffff', bg='#75142B'
    ).pack(pady=10)

    tk.Label(
        root,
        text="Enter details below to book your tour:",
        font=('Arial', 15, 'italic'),
        fg='#ffffff', bg='#75142B'
    ).pack(pady=10)

    # Form fields
    fields = ['Customer Name', 'Hotel', 'Booking Date (YYYY-MM-DD)', 'Package', 'Place', 'Transport', 'Special Requests']
    entries = {}

    for field in fields:
        tk.Label(
            root,
            text=f"{field}:",
            font=('Arial', 12, 'bold'),
            fg='#ffffff', bg='#75142B'
        ).pack(anchor='w', padx=20, pady=5)
        entry = ttk.Entry(root, width=40)
        entry.pack(padx=20, pady=5)
        entries[field] = entry

    def book_tour():
        details = {field: entry.get() for field, entry in entries.items()}
        if all(details.values()):
            try:
                # Example query (update this with real insert logic)
                cursor.execute(
                    "INSERT INTO Tour_Booking (customer_name, hotel, booking_date, package, place, transport, special_requests) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    tuple(details.values())
                )
                connection.commit()
                messagebox.showinfo("Success", "Tour booked successfully!")
                root.destroy()
                main_menu()
            except Exception as e:
                messagebox.showerror("Error", f"Booking failed: {e}")
        else:
            messagebox.showwarning("Warning", "All fields are required!")

    ttk.Button(
        root,
        text="Book Tour",
        command=book_tour
    ).pack(pady=20)

    ttk.Button(
        root,
        text="Back to Main Menu",
        command=lambda: [root.destroy(), main_menu()]
    ).pack(pady=10)

    root.mainloop()

# Admin Portal
def admin_portal():
    root = ThemedTk(theme="arc")
    root.title("ADMIN PORTAL")
    root.geometry('1000x800')
    root['background'] = '#75142B'

    tk.Label(
        root,
        text="Admin Portal",
        font=('Helvetica', 30, 'bold', 'underline'),
        fg='#ffffff', bg='#75142B'
    ).pack(pady=10)

    # Options for admin
    options = ['Add User', 'Remove User', 'Update Tour Packages', 'Manage Bookings', 'View Reports', 'Manage Discounts']
    for option in options:
        ttk.Button(
            root,
            text=option,
            command=lambda opt=option: messagebox.showinfo("Info", f"{opt} functionality coming soon!")
        ).pack(pady=10)

    ttk.Button(
        root,
        text="Back to Main Menu",
        command=lambda: [root.destroy(), main_menu()]
    ).pack(pady=20)

    root.mainloop()

# User Portal
def user_portal():
    root = ThemedTk(theme="arc")
    root.title("USER PROFILE")
    root.geometry('1000x800')
    root['background'] = '#75142B'

    tk.Label(
        root,
        text="User Profile",
        font=('Helvetica', 30, 'bold', 'underline'),
        fg='#ffffff', bg='#75142B'
    ).pack(pady=10)

    tk.Label(
        root,
        text="Manage your profile, view bookings, and preferences",
        font=('Arial', 15, 'italic'),
        fg='#ffffff', bg='#75142B'
    ).pack(pady=10)

    ttk.Button(
        root,
        text="Edit Profile",
        command=lambda: messagebox.showinfo("Info", "Edit Profile functionality coming soon!")
    ).pack(pady=10)

    ttk.Button(
        root,
        text="View Booking History",
        command=lambda: messagebox.showinfo("Info", "Booking History functionality coming soon!")
    ).pack(pady=10)

    ttk.Button(
        root,
        text="Back to Main Menu",
        command=lambda: [root.destroy(), main_menu()]
    ).pack(pady=20)

    root.mainloop()

# Run the main menu
main_menu()
