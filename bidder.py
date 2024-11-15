#------------bidder.py
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import preview 

def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Password123',
        database='AUCTION'
    )




def fetch_available_items():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = """
        SELECT 
            Item.Item_ID, Item.Description, Item.Base_Price,
            CASE WHEN func1(Item.Item_ID) = 1 THEN 'On' ELSE 'Off' END AS Bid_Status
        FROM Item
        WHERE Item.Status = 'Available'
        """
        cursor.execute(query)
        items = cursor.fetchall()
        return items
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Variable to track the preview button's state
preview_enabled = False

# Function to enable preview button after delay
def enable_preview():
    global preview_enabled
    preview_enabled = True

# Function to fetch items on which the user has applied bids, including the highest bid amount for each item
def fetch_applied_bids(bidder_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = """
        SELECT 
            Bid.Bid_ID, Item.Item_ID, Item.Description, Item.Base_Price, 
            Bid.Amount AS Bid_Amount, Bid.Status,
            (SELECT MAX(B.Amount) FROM Bid B WHERE B.Item_ID = Item.Item_ID) AS Highest_Bid,
            CASE WHEN func1(Item.Item_ID) = 1 THEN 'On' ELSE 'Off' END AS Bid_Status
        FROM Item
        JOIN Bid ON Item.Item_ID = Bid.Item_ID
        JOIN Bidder_Bid ON Bid.Bid_ID = Bidder_Bid.Bid_ID
        WHERE Bidder_Bid.Bidder_ID = %s
        """
        cursor.execute(query, (bidder_id,))
        applied_bids = cursor.fetchall()
        return applied_bids
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to populate the applied bids table with items the user has bid on
def populate_applied_bids_table(bidder_id):
    applied_bids = fetch_applied_bids(bidder_id)
    for bid in applied_bids:
        applied_bids_table.insert("", "end", values=bid)

def refresh_applied_bids_table(bidder_id):
    for item in applied_bids_table.get_children():
        applied_bids_table.delete(item)
    populate_applied_bids_table(bidder_id)

## Function to update bid status based on the highest bid amount
def update_bid_status(item_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Find the bid with the highest amount for the given item_id
        query = """
        SELECT Bid_ID
        FROM Bid
        WHERE Item_ID = %s
        ORDER BY Amount DESC
        LIMIT 1
        """
        cursor.execute(query, (item_id,))
        highest_bid_id = cursor.fetchone()

        if highest_bid_id:
            highest_bid_id = highest_bid_id[0]

            # Update the status of the highest bid to "Won"
            cursor.execute(
                "UPDATE Bid SET Status = 'Won' WHERE Bid_ID = %s", (highest_bid_id,)
            )

            # Update the status of all other bids for the same item to "Not Won"
            cursor.execute(
                "UPDATE Bid SET Status = 'Not Won' WHERE Item_ID = %s AND Bid_ID != %s",
                (item_id, highest_bid_id)
            )
            connection.commit()
    except mysql.connector.Error as err:
        print(f"Error updating bid status: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def submit_bid(item_id, bid_amount, bidder_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Check if the bid is greater than or equal to the base price
        cursor.execute("SELECT Base_Price FROM Item WHERE Item_ID = %s", (item_id,))
        base_price = cursor.fetchone()[0]

        if bid_amount >= base_price:
            cursor.callproc('submit_bid', [item_id, bid_amount, 'Not Won'])
            connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            bid_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO Bidder_Bid (Bidder_ID, Bid_ID) VALUES (%s, %s)", (bidder_id, bid_id))
            connection.commit()

            update_bid_status(item_id)

            # Refresh the applied bids table to show the updated status
            refresh_applied_bids_table(bidder_id)

            messagebox.showinfo("Success", "Your bid has been submitted successfully.")
        else:
            messagebox.showwarning("Warning", f"Bid amount must be at least ${base_price:.2f}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to submit bid: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to open bid entry pop-up with updated styling and bidder ID
def open_bid_entry_popup(item_id, base_price, bidder_id):
    def submit_bid_action():
        global preview_enabled
        bid_amount = float(entry_amount.get())
        if bid_amount >= base_price:
            submit_bid(item_id, bid_amount, bidder_id)  # Assume this function exists to submit the bid
            bid_popup.destroy()
            
            # Disable the preview button initially and enable it after 10 seconds
            preview_enabled = False
            bidder_window.after(10000, enable_preview)  # Enable preview after 10 seconds
        else:
            messagebox.showwarning("Warning", f"Bid amount must be at least ${base_price:.2f}")

    # Create pop-up window for bid entry
    bid_popup = tk.Toplevel()
    bid_popup.title("Enter Bid Amount")
    bid_popup.geometry("600x400")
    bid_popup.configure(bg="#2C3E50")

    tk.Label(
        bid_popup, text=f"Enter bid for Item ID: {item_id}",
        font=("Arial", 20, "bold"), bg="#2C3E50", fg="white"
    ).pack(pady=10)
    tk.Label(
        bid_popup, text=f"Base Price: ${base_price:.2f}",
        font=("Arial", 14), bg="#2C3E50", fg="red"
    ).pack()

    entry_amount = tk.Entry(bid_popup, font=("Arial", 12), width=50)
    entry_amount.pack(pady=40)

    submit_button = tk.Button(
        bid_popup, text="Submit", command=submit_bid_action,
        font=("Arial", 12), 
        bg="#ffffff", 
        fg="black", 
        bd=3, 
        relief=tk.RAISED, 
        width=15
    )
    submit_button.pack(pady=10)


def apply_for_bid(bidder_id):
    selected_item_index = item_table.selection()
    if selected_item_index:
        selected_item = item_table.item(selected_item_index, "values")
        item_id = int(selected_item[0])
        base_price = float(selected_item[2].replace('$', ''))

        # Check if payment has already been made for this item
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("""
                           SELECT COUNT(*) 
                           FROM Payment 
                           WHERE Bid_ID IN 
                           (SELECT Bid_ID FROM Bid WHERE Item_ID = %s)
                           """,
                            (item_id,))
            payment_count = cursor.fetchone()[0]

            if payment_count > 0:
                messagebox.showinfo("Info", "Bid is over. Payment has already been made for this item.")
            else:
                open_bid_entry_popup(item_id, base_price, bidder_id)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to check payment status: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        messagebox.showwarning("Warning", "Please select an item to apply for bid.")

# Function to open the preview window for the selected bid in the applied bids table
def preview_bid():
    if preview_enabled:
        selected_bid_index = applied_bids_table.selection()
        if selected_bid_index:
            selected_bid = applied_bids_table.item(selected_bid_index, "values")
            preview.open_preview_window(selected_bid)  # Open preview window
        else:
            messagebox.showwarning("Warning", "Please select a bid to preview.")
    else:
        messagebox.showinfo("Info", "Please wait for 10 seconds after submitting a bid before previewing.")

# Function to populate the applied bids table with items the user has bid on
def populate_applied_bids_table(bidder_id):
    applied_bids = fetch_applied_bids(bidder_id)
    for bid in applied_bids:
        applied_bids_table.insert("", "end", values=bid)

# Function to refresh the applied bids table (clears and repopulates it)
def refresh_applied_bids_table(bidder_id):
    for item in applied_bids_table.get_children():
        applied_bids_table.delete(item)
    populate_applied_bids_table(bidder_id)

def open_bidder_page(bidder_id):
    global item_table, applied_bids_table,bidder_window
    available_items = fetch_available_items()

    bidder_window = tk.Tk()
    bidder_window.title("Bidder Page")
    bidder_window.geometry("1000x900")
    bidder_window.configure(bg="#09203f")

    bidder_label = tk.Label(
        bidder_window,
        text="Available Items for Bidding",
        font=("Arial", 20, "bold"),
        bg="#09203f",
        fg="white"
    )
    bidder_label.pack(pady=0)

    main_frame = tk.Frame(bidder_window, bg="#34495E", bd=10, relief=tk.GROOVE)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

    y_scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
    x_scroll = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)

    # Add the new "Bid Status" column in item_table
    item_table = ttk.Treeview(
        main_frame,
        columns=("Item ID", "Item", "Base Price", "Bid Status"),
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
    item_table.heading("Item ID", text="Item ID", anchor="center")
    item_table.heading("Item", text="Item Description", anchor="center")
    item_table.heading("Base Price", text="Base Price", anchor="center")
    item_table.heading("Bid Status", text="Bid Status", anchor="center")  # New column
    item_table.column("Item ID", anchor="center", width=100)
    item_table.column("Item", anchor="center", width=400)
    item_table.column("Base Price", anchor="center", width=150)
    item_table.column("Bid Status", anchor="center", width=100)  # New column
    item_table['show'] = 'headings'

    for item_id, description, price, bid_status in available_items:
        item_table.insert("", "end", values=(item_id, description, f"${price:.2f}", bid_status))

    item_table.pack(fill=tk.BOTH, expand=True)
    y_scroll.config(command=item_table.yview)
    x_scroll.config(command=item_table.xview)
    y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    apply_button = tk.Button(
        bidder_window,
        text="Apply for Bid",
        font=("Arial", 16, "bold"),
        bg="#ffffff", 
        fg="black", 
        bd=3, 
        relief=tk.RAISED, 
        width=20,
        command=lambda: apply_for_bid(bidder_id)
    )
    apply_button.pack(pady=20)
    
    applied_bids_label = tk.Label(
        bidder_window,
        text="Applied Bids",
        font=("Arial", 20, "bold"),
        bg="#09203f",
        fg="white"
    )
    applied_bids_label.pack(pady=10)

    applied_bids_table = ttk.Treeview(
        bidder_window,
        columns=("Bid ID", "Item ID", "Description", "Base Price", "Bid Amount", "Status", "Highest Bid"),
        height=8,
        show='headings'
    )
    applied_bids_table.heading("Bid ID", text="Bid ID", anchor="center")
    applied_bids_table.heading("Item ID", text="Item ID", anchor="center")
    applied_bids_table.heading("Description", text="Description", anchor="center")
    applied_bids_table.heading("Base Price", text="Base Price", anchor="center")
    applied_bids_table.heading("Bid Amount", text="Your Bid", anchor="center")
    applied_bids_table.heading("Status", text="Status", anchor="center")
    applied_bids_table.heading("Highest Bid", text="Highest Bid", anchor="center")
    applied_bids_table.column("Bid ID", anchor="center", width=80)
    applied_bids_table.column("Item ID", anchor="center", width=100)
    applied_bids_table.column("Description", anchor="center", width=250)
    applied_bids_table.column("Base Price", anchor="center", width=100)
    applied_bids_table.column("Bid Amount", anchor="center", width=100)
    applied_bids_table.column("Status", anchor="center", width=100)
    applied_bids_table.column("Highest Bid", anchor="center", width=100)
    applied_bids_table.pack()
    # Populate the table with the applied bids
    populate_applied_bids_table(bidder_id)

    preview_button = tk.Button(
        bidder_window,
        text="Preview",
        font=("Arial", 16, "bold"),
        bg="#ffffff", 
        fg="black", 
        bd=3, 
        relief=tk.RAISED, 
        width=20,
        command=preview_bid
    )
    preview_button.pack(pady=10)
    bidder_window.mainloop()