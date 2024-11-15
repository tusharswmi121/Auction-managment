import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Database connection setup
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password123',
    'database': 'AUCTION'
}

def open_admin_page():
    # Admin Dashboard Window
    admin_window = tk.Tk()
    admin_window.title("Admin Dashboard")
    admin_window.geometry("900x900")
    admin_window.configure(bg="gray")

    # Connect to database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Fetch data function
    def fetch_data(table):
        cursor.execute(f"SELECT * FROM {table}")
        return cursor.fetchall()

    # Get all table names
    def get_all_tables():
        cursor.execute("SHOW TABLES")
        return [table[0] for table in cursor.fetchall()]

    # Display data in Treeview
    def show_table_data(table_name, treeview):
        for item in treeview.get_children():
            treeview.delete(item)

        rows = fetch_data(table_name)
        for row in rows:
            treeview.insert('', 'end', values=row)

    # Function to create Treeview for each table
    def create_table_view(tab, table_name):
        # Table Frame
        table_frame = tk.Frame(tab, bg="gray")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cursor.execute(f"DESCRIBE {table_name}")
        fields = cursor.fetchall()  # Fetch column details
        column_names = [col[0] for col in fields]  # Extract column names

        # Treeview for table data
        treeview = ttk.Treeview(table_frame, columns=column_names, show='headings')
        for col in column_names:
            treeview.heading(col, text=col)
            treeview.column(col, width=150, anchor='center')  # Center align column values

        # Pack the treeview widget
        treeview.pack(fill="both", expand=True)

        # Initial data load
        show_table_data(table_name, treeview)

        # CRUD buttons
        button_frame = tk.Frame(tab, bg="gray")
        button_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(button_frame, text="Add", command=lambda: add_entry(table_name, treeview)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Update", command=lambda: update_entry(table_name, treeview)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete", command=lambda: delete_entry(table_name, treeview, fields)).pack(side="left", padx=5)

    # Add new entry function
    def add_entry(table, treeview):
        add_window = tk.Toplevel(admin_window)
        add_window.title(f"Add New Entry to {table}")
        add_window.geometry("400x600")

        # Get columns for the selected table
        cursor.execute(f"DESCRIBE {table}")
        fields = cursor.fetchall()

        entries = {}
        for i, (field_name, *_rest) in enumerate(fields):
            label = tk.Label(add_window, text=field_name)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(add_window, show="*" if field_name.lower() == "password" else None)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            entries[field_name] = entry

        def submit_entry():
            values = [entry.get() for entry in entries.values()]
            if all(values):
                try:
                    placeholders = ", ".join(["%s"] * len(values))
                    columns = ", ".join(entries.keys())
                    cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
                    connection.commit()
                    messagebox.showinfo("Success", "Entry added successfully")
                    add_window.destroy()
                    show_table_data(table, treeview)
                    update_user_count()
                    update_payment_count_by_mode()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error adding entry: {err}")
            else:
                messagebox.showerror("Error", "All fields are required")

        tk.Button(add_window, text="Submit", command=submit_entry).grid(row=len(fields), column=0, columnspan=2, pady=20)

    # Update entry function
    def update_entry(table, treeview):
        selected = treeview.selection()
        if not selected:
            messagebox.showerror("Update Entry", "No entry selected for update.")
            return
        selected_item = treeview.item(selected[0], 'values')
        
        update_window = tk.Toplevel(admin_window)
        update_window.title(f"Update Entry in {table}")
        update_window.geometry("400x500")

        cursor.execute(f"DESCRIBE {table}")
        fields = cursor.fetchall()

        entries = {}
        for i, (field_name, *_rest) in enumerate(fields):
            tk.Label(update_window, text=field_name).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(update_window)
            entry.insert(0, selected_item[i])
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            entries[field_name] = entry

        def save_update():
            values = [entry.get() for entry in entries.values()]
            primary_key_value = selected_item[0]
            set_clause = ", ".join([f"{field}=%s" for field in entries.keys()])
            try:
                cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {fields[0][0]}=%s", (*values, primary_key_value))
                connection.commit()
                messagebox.showinfo("Update Success", "Entry updated successfully")
                update_window.destroy()
                show_table_data(table, treeview)
                update_payment_count_by_mode()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error updating entry: {err}")

        tk.Button(update_window, text="Save", command=save_update).grid(row=len(fields), column=0, columnspan=2, pady=20)

    # Delete entry function
    def delete_entry(table, treeview, fields):
        selected = treeview.selection()
        if not selected:
            messagebox.showerror("Delete Entry", "No entry selected for deletion.")
            return
        confirm = messagebox.askyesno("Delete Entry", "Are you sure you want to delete this entry?")
        if confirm:
            primary_key_value = treeview.item(selected[0], 'values')[0]
            cursor.execute(f"DELETE FROM {table} WHERE {fields[0][0]} = %s", (primary_key_value,))
            connection.commit()
            show_table_data(table, treeview)
            update_user_count()
            update_payment_count_by_mode()

    # Count and display total users
    def update_user_count():
        cursor.execute("SELECT COUNT(*) FROM User")
        total_users = cursor.fetchone()[0]
        user_count_label.config(text=f"Total Users: {total_users}")

    # Count and display payment counts by mode of payment
    def update_payment_count_by_mode():
        cursor.execute("""
                       SELECT Mode_Of_Payment, COUNT(*) 
                       FROM Payment 
                       GROUP BY Mode_Of_Payment
                       """)
        payment_counts = cursor.fetchall()
        payment_count_text = " | ".join([f"{mode}: {count}" for mode, count in payment_counts])
        payment_count_label.config(text=f"Payment Counts: {payment_count_text}")

    # Notebook for tabs
    notebook = ttk.Notebook(admin_window)
    notebook.pack(fill="both", expand=True)

    # Create tabs for all tables
    table_names = get_all_tables()
    for table_name in table_names:
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=table_name)
        create_table_view(tab, table_name)

    # Label for displaying total user count
    user_count_label = tk.Label(admin_window, text="", bg="gray", font=("Arial", 12, "bold"))
    user_count_label.pack(side="bottom", pady=5)
    update_user_count()

    # Label for displaying payment counts by mode
    payment_count_label = tk.Label(admin_window, text="", bg="gray", font=("Arial", 12, "bold"))
    payment_count_label.pack(side="bottom", pady=5)
    update_payment_count_by_mode()

    admin_window.mainloop()
