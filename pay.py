import tkinter as tk
from tkinter import messagebox
import mysql.connector

def open_payment_page(item_id, bid_amount, bid_id):
    def create_connection():
        """Establish a new connection to the database."""
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="Password123",
                database="AUCTION"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Connection Error", f"Error connecting to database: {err}")
            return None

    db = create_connection()
    if not db:
        return  # Exit if connection fails
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            SELECT p.*
            FROM Payment p
            JOIN Bid b ON p.Bid_ID = b.Bid_ID
            WHERE b.Item_ID = %s
        """, (item_id,))
        payment_exists = cursor.fetchone()
        
        if payment_exists:
            messagebox.showinfo("Payment Already Made", "Payment has already been made for this item.")
            payment_window.destroy()
            return
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return
    finally:
        cursor.close()
        db.close()

    # Create a new window for the payment page
    payment_window = tk.Toplevel()
    payment_window.title("Make Payment")
    payment_window.geometry("400x400")
    payment_window.configure(bg="#4682B4")  # Background color for styling

    # Display the "Make Payment" label
    make_payment_label = tk.Label(
        payment_window,
        text="Make Payment",
        font=("Arial", 24, "bold"),
        bg="#4682B4",
        fg="white"
    )
    make_payment_label.pack(pady=30)

    # Function to handle payment and update the database
    def process_payment(method):
        db = create_connection()
        if not db:
            return  # Exit if connection fails
        cursor = db.cursor()
        try:
            # Call the stored procedure to insert the payment record
            cursor.callproc('insert_payment', (bid_id, bid_amount, method))
            db.commit()
            messagebox.showinfo("Payment Successful", f"Payment via {method} was successful!")
            payment_window.destroy()  # Close the window after payment
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    # Payment buttons
    cod_button = tk.Button(
        payment_window,
        text="COD",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="black",
        command=lambda: process_payment("COD")
    )
    cod_button.pack(pady=10)

    upi_button = tk.Button(
        payment_window,
        text="UPI",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="black",
        command=lambda: process_payment("UPI")
    )
    upi_button.pack(pady=10)

    card_button = tk.Button(
        payment_window,
        text="Card",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="black",
        command=lambda: process_payment("Card")
    )
    card_button.pack(pady=10)

    # Label to display the amount to be paid
    amount_label = tk.Label(
        payment_window,
        text=f"You have to pay: {bid_amount}",
        font=("Arial", 14, "bold"),
        bg="#4682B4",
        fg="white"
    )
    amount_label.pack(pady=20)

    payment_window.mainloop()
