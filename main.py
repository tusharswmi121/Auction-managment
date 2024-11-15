import tkinter as tk
import mysql.connector  
import seller 
import bidder  

def insert_seller(user_id, username):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password123",
            database="AUCTION"
        )

        cursor = connection.cursor()

        # Check if the user is already a seller
        cursor.execute("SELECT COUNT(*) FROM Seller WHERE User_ID = %s", (user_id,))
        result = cursor.fetchone()

        if result[0] > 0:
            print("User already exists in the seller table.")
        else:
            cursor.callproc('AddSeller', (user_id, username))
            connection.commit()  # Commit the transaction
            print("Current user processed and seller updated.")

        seller.open_seller_page(user_id, username)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def insert_bidder(user_id, username):
    connection = None
    cursor = None
    bidder_id = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password123",
            database="AUCTION"
        )
        cursor = connection.cursor()

        cursor.execute("SELECT Bidder_ID FROM Bidder WHERE User_ID = %s", (user_id,))
        result = cursor.fetchone()

        if result:
            print("User already exists in the bidder table.")
            bidder_id = result[0]  
        else:

            cursor.callproc('AddBidder', (user_id, username))
            connection.commit()  
            print("Current user processed and bidder updated.")

            cursor.execute("SELECT Bidder_ID FROM Bidder WHERE User_ID = %s", (user_id,))
            result = cursor.fetchone()
            if result:
                bidder_id = result[0]

        if bidder_id:
            bidder.open_bidder_page(bidder_id)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def func1(user_id, username):
    insert_seller(user_id, username)  

def func2(user_id, username):
    insert_bidder(user_id, username) 

def open_main_page(user_id, username):
    main_window = tk.Tk()
    main_window.title("Main Page")
    main_window.geometry("650x550")
    main_window.configure(bg="#d3d3d3")
    
    main_label = tk.Label(main_window, text="Welcome to the Main Page!", font=("Arial", 24), bg="#d3d3d3", fg="black")
    main_label.pack(pady=10)

    # Frame for Sell Button
    sell_frame = tk.Frame(main_window, bg="#4c535c")
    sell_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Sell Button
    sell_button = tk.Button(
        sell_frame, 
        text="Sell", 
        font=("Arial", 16), 
        bg="#ffffff", 
        fg="black", 
        bd=3, 
        relief=tk.RAISED, 
        width=10, 
        command=lambda: func1(user_id, username)  # Using lambda to pass arguments
    )
    sell_button.pack(expand=True, padx=10, pady=10)  # Center the button in the frame

    # Frame for Bid Button
    bid_frame = tk.Frame(main_window, bg="#a3846c")
    bid_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Bid Button
    bid_button = tk.Button(bid_frame, 
        text="Bid", 
        font=("Arial", 16), 
        bg="#ffffff", 
        fg="black", 
        bd=3, 
        relief=tk.RAISED, 
        width=10, 
        command=lambda: func2(user_id, username)  # Using lambda to pass arguments
    )
    bid_button.pack(expand=True, padx=10, pady=10)  # Center the button in the frame

    # Run the main loop
    main_window.mainloop()