import tkinter as tk
from tkinter import messagebox
import mysql.connector
import main 
import admin  

# ------------------Database connection setup
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password123',
    'database': 'AUCTION'
}

# ---------------login page functions -------------

def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Input Error", "Please enter both Username and Password.")
        return False

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        query = "SELECT User_ID, Role FROM User WHERE Username = %s AND Password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        if user:
            user_id, role = user
            if role == 'admin':
                messagebox.showinfo("Admin Login Success", "Welcome, Admin!")
                admin.open_admin_page()
            else:
                messagebox.showinfo("Login Success", f"Welcome, {username}!")
                root.destroy()
                main.open_main_page(user_id, username)
            return True
        else:
            messagebox.showerror("Login Failed", "Invalid credentials, please try again.")
            return False
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
# -----------------sign up page function ----------------

def open_registration_window():
    # Create a new window for registration
    reg_window = tk.Toplevel(root)
    reg_window.title("User Registration")
    reg_window.geometry("800x800")
    reg_window.configure(bg="#09203f")

    #-------------title frame ---------------------------
    title_frame = tk.Frame(reg_window, bg="#09203f", width=800, height=200)
    title_frame.pack(fill="x", side="top")
    
    # ----------------- title ----------------------------
    title_label = tk.Label(
        title_frame, text="Online Auction !!", font=("Helvetica", 24, "bold"),
        bg="#09203f", fg="gray"
    )
    title_label.pack(expand=True)
    
    # Center frame
    center_frame = tk.Frame(reg_window, bg="#09203f")
    center_frame.pack(expand=True)
    
    # Fonts
    label_font = ("Arial", 12,"bold")
    entry_font = ("Arial", 12)
    
    # Registration Fields
    fields = [
        ("Username", "username"),
        ("Password", "password"),
        ("First Name", "f_name"),
        ("Middle Name", "m_name"),
        ("Last Name", "l_name"),
        ("Year of Birth", "year_of_birth"),
        ("City", "city"),
        ("Street", "street"),
        ("State", "state"),
        ("Pincode", "pincode"),
        ("Email", "email")
    ]
    
    entries = {}
    
    for idx, (label_text, var_name) in enumerate(fields):
        tk.Label(center_frame, text=label_text +"  :", font=label_font, bg="#09203f", fg="gray").grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(center_frame, font=entry_font, width=30, bd=2, relief="solid")
        if var_name == "password":
            entry.config(show="*")
        entry.grid(row=idx, column=1, padx=10, pady=10, sticky="w")
        entries[var_name] = entry
    
    def register_user():
        # Retrieve all input data
        username = entries['username'].get()
        password = entries['password'].get()
        f_name = entries['f_name'].get()
        m_name = entries['m_name'].get()
        l_name = entries['l_name'].get()
        year_of_birth = entries['year_of_birth'].get()
        city = entries['city'].get()
        street = entries['street'].get()
        state = entries['state'].get()
        pincode = entries['pincode'].get()
        email = entries['email'].get()
        
        # Basic validation
        if not username or not password or not city or not state or not pincode or not email:
            messagebox.showerror("Input Error", "Please fill in all required fields.")
            return
        
        try:
            year_of_birth = int(year_of_birth) if year_of_birth else None
        except ValueError:
            messagebox.showerror("Input Error", "Year of Birth must be a number.")
            return
        
        try:
            pincode = int(pincode)
        except ValueError:
            messagebox.showerror("Input Error", "Pincode must be a number.")
            return
        
        # Insert into database using stored procedure
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            
            # Call the stored procedure
            cursor.callproc('AddNewUser', [
                username, password, f_name, m_name, l_name,
                year_of_birth, city, street, state, pincode, email
            ])
            
            connection.commit()
            messagebox.showinfo("Registration Success", "User successfully registered!")
            reg_window.destroy()
            
        except mysql.connector.Error as err:
            if err.errno == 1062:
                # Duplicate entry error
                messagebox.showerror("Registration Error", "Username or Email already exists.")
            else:
                messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    # Register Button
    register_button = tk.Button(
    center_frame, 
    text="Register", 
    command=register_user, 
    font=("Arial", 18, "bold"), 
    fg="black", 
    bg="black", 
    bd=4,  
    width=20, 
    relief=tk.RAISED  
    )
    register_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

# ------------------------------GUI for login page --------------------------

# Set up the main window
root = tk.Tk()
root.title("Login Form")
root.geometry("800x800") 
root.configure(bg="#09203f")

title_frame = tk.Frame(root, bg="#09203f", width=800, height=200)
title_frame.pack(fill="x", side="top")

# ----------------- title ----------------------------
title_label = tk.Label(
        title_frame, text="Online Auction !!", font=("Helvetica", 24, "bold"),
        bg="#09203f", fg="gray"
    )
title_label.pack(expand=True)

#--------------login frame---------------------------------------
login_frame = tk.Frame(root, bg="#09203f",borderwidth=2, padx=20, pady=0)  # New frame with a light gray background
login_frame.pack(expand=True)

# Labels and Entry fields for Login (only username and password)
tk.Label(login_frame, text="USER NAME",font=("Arial", 14, "bold"), fg="GRAY",bg="#09203f").grid(row=0, column=0, padx=10, pady=0, sticky="e")
entry_username = tk.Entry(login_frame, font=("Arial", 14, "bold"), width=25, bd=2, relief="solid")
entry_username.grid(row=0, column=1, padx=10, pady=0, sticky="w")

tk.Label(login_frame, text="PASSWORD", font=("Arial", 14, "bold"), fg="GRAY",bg="#09203f").grid(row=1, column=0, padx=10, pady=30, sticky="e")
entry_password = tk.Entry(login_frame, show="*",font=("Arial", 14, "bold"), width=25, bd=2, relief="solid")
entry_password.grid(row=1, column=1, padx=10, pady=20, sticky="w")

# Login Button
login_button = tk.Button(login_frame, text="Login", command=validate_login, font=("Arial", 14, "bold"), fg="black",bg="black", bd=0, width=15)
login_button.grid(row=2, column=1, padx=10, pady=20)

# Sign Up Button
signup_button = tk.Button(login_frame, text="Sign Up", command=open_registration_window, font=("Arial", 14, "bold"), fg="black",bg="black", bd=0, width=15)
signup_button.grid(row=3, column=1, padx=10, pady=20)

# Start the Tkinter event loop
root.mainloop()
