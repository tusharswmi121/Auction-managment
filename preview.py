import tkinter as tk
from tkinter import messagebox
import mysql.connector
import pay  


def open_preview_window(bid_details):
    # Unpack the bid details
    bid_id, item_id, description, base_price, bid_amount, status, highest_bid, bid_status = bid_details

    # Create a new window for the preview
    preview_window = tk.Toplevel()
    preview_window.title("Bid Preview")
    preview_window.geometry("700x800")
    preview_window.configure(bg="#4c535c")

    # Display "Won" or "Not Won" label in a top light gray frame spanning the width of the window
    status_frame = tk.Frame(preview_window, bg="lightgray", width=700, height=100)
    status_frame.pack(fill="x")

    won_label = tk.Label(
        status_frame,
        text="WON" if status.lower() == "won" else "Not Won",
        font=("Arial", 36, "bold"),
        bg="lightgray",
        fg="gray"
    )
    won_label.pack(pady=25)

    # Create a frame for item details in a black box
    details_frame = tk.Frame(preview_window, bg="black", width=650, height=300)
    details_frame.pack(pady=20)

    item_info_label = tk.Label(
        details_frame,
        text=(
            f"Item ID: {item_id}\n"
            f"Description: {description}\n"
            f"Base Price: ${base_price}\n"
            f"Bid Amount: ${bid_amount}\n"
            f"Status: {status}"
        ),
        font=("Arial", 14),
        bg="black",
        fg="white",
        justify="left",
        anchor="w"
    )
    item_info_label.pack(padx=20, pady=20, anchor="w")

    def open_payment_page():
        pay.open_payment_page(item_id, bid_amount, bid_id)

    if status.lower() == "won":
        payment_button = tk.Button(
            preview_window,
            text="Payment",
            font=("Arial", 16, "bold"),
            bg="#ffffff", 
            fg="black",
            command=open_payment_page
        )
        payment_button.pack(pady=20)

        separator = tk.Frame(preview_window, bg="black", height=2, width=650)
        separator.pack(pady=10)

        review_prompt_label = tk.Label(
            preview_window,
            text="Want to give Review on Item?",
            font=("Arial", 16, "italic"),
            bg="#4c535c",
            fg="white"
        )
        review_prompt_label.pack(pady=10)

        review_frame = tk.Frame(preview_window, bg="#4c535c")
        review_frame.pack(pady=10)

        overview_label = tk.Label(
            review_frame,
            text="Overview:",
            font=("Arial", 12),
            bg="#4c535c",
            fg="white"
        )
        overview_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        overview_entry = tk.Entry(review_frame, width=50)
        overview_entry.grid(row=0, column=1, padx=5, pady=5)

        description_label = tk.Label(
            review_frame,
            text="Description:",
            font=("Arial", 12),
            bg="#4c535c",
            fg="white"
        )
        description_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        description_entry = tk.Entry(review_frame, width=50)
        description_entry.grid(row=1, column=1, padx=5, pady=5)

        def submit_review():
            overview = overview_entry.get()
            description = description_entry.get()

            try:
                
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Password123",
                    database="AUCTION"
                )
                cursor = conn.cursor()

                cursor.execute("INSERT INTO Review (Bid_ID, Overview, Description) VALUES (%s, %s, %s)",
                               (bid_id, overview, description))
                conn.commit()

                messagebox.showinfo("Review Submitted", "Thank you for your review!")
                preview_window.destroy()  # Close the window after submission

            except mysql.connector.Error as err:
                if err.errno == 1644:  # Error code for trigger failure
                    messagebox.showerror("Error", "Review already exists for this item.")
                else:
                    messagebox.showerror("Database Error", f"Error: {err}")

            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

        submit_button = tk.Button(
            preview_window,
            text="Submit Review",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="black",
            command=submit_review
        )
        submit_button.pack(pady=20)

    preview_window.mainloop()
