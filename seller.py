import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

# MySQL connection setup
def connect_to_db():
    return mysql.connector.connect(
        host="localhost", 
        user="root",      
        password="Password123",  
        database="AUCTION"  
    )

# ----------------------- Open Seller Page function 

def open_seller_page(user_id, username):
    seller_window = tk.Toplevel()
    seller_window.title("Seller Page")
    seller_window.geometry("800x800")
    seller_window.configure(bg="#537895")

    # ------------------- frame for title -------------------------
    title_frame = tk.Frame(seller_window, bg="#485563", width=800, height=200)
    title_frame.pack(fill="x", side="top")


    # ----------------- title ----------------------------
    title_label = tk.Label(
        title_frame, text="Enter Item Details", font=("Helvetica", 24, "bold"),
        bg="#485563", fg="white"
    )
    title_label.pack(expand=True)

    entry_frame = tk.Frame(seller_window, bg="#13547a", width=600, height=800) 
    entry_frame.place(relx=0.5, rely=0.4, anchor='center') 

   #---------------label for entry frame ---------------------------
    def create_fancy_label(frame, text, row, column):
        label = tk.Label(frame, text=text, font=("Helvetica", 16, "bold"), bg="#13547a", fg="black")
        label.grid(row=row, column=column, padx=10, pady=(10, 5), sticky="e")  

    # -------------------- Description  ------------------------
    create_fancy_label(entry_frame, "Description:", 0, 0)
    description_entry = ttk.Entry(entry_frame, font=("Helvetica", 15), width=30)
    description_entry.grid(row=0, column=1, padx=10, pady=(40, 40)) 

    #------------base price----------------------
    create_fancy_label(entry_frame, "Base Price:", 20, 0) 
    price_entry = ttk.Entry(entry_frame, font=("Helvetica", 15), width=30)
    price_entry.grid(row=20, column=1, padx=10, pady=(30, 30))  

    #------------button---------------------
    submit_button = tk.Button(
        entry_frame, 
        text="Submit",
        font=("Arial", 18,"bold"), fg="black", bd=0, width=15, relief=tk.GROOVE,
        command=lambda: submit_details(description_entry.get(), price_entry.get(),user_id, username)
    )
    submit_button.grid(row=40, columnspan=2, pady=60)  # Centered below the entry fields

def submit_details(description, base_price,user_id, username):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Define the parameters for the stored procedure
        status = 'Active'
        item_status = 'Available'

        # Execute the stored procedure
        cursor.callproc("AddSellerItem", (user_id, username, status, base_price, description, item_status))

        # Commit the transaction
        db.commit()

        # Show a success message
        messagebox.showinfo("Success", "Item details submitted successfully.")

    except mysql.connector.Error as e:
        print("Error:", e)
        messagebox.showerror("Error", f"Failed to submit item details: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()






