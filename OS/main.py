import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jeeva@123",
    database="flight_booking"
)
cursor = conn.cursor()

# Function to fetch available flights
def fetch_available_flights():
    cursor.execute("SELECT flight_id, flight_number, start_location, destination, price, flight_time FROM available_flights")
    return cursor.fetchall()

# Function to fetch booked flights for a user
def fetch_booked_flights(user_name):
    query = """
    SELECT booked_flights.booking_id, available_flights.flight_number, available_flights.start_location, available_flights.destination, available_flights.price, available_flights.flight_time
    FROM booked_flights
    JOIN available_flights ON booked_flights.flight_id = available_flights.flight_id
    WHERE booked_flights.user_name = %s
    """
    cursor.execute(query, (user_name,))
    return cursor.fetchall()

# Function to book a flight
def book_flight():
    selected_flight = flight_tree.focus()
    if not selected_flight:
        messagebox.showerror("Error", "Please select a flight to book.")
        return

    user_name = user_name_entry.get()
    if not user_name:
        messagebox.showerror("Error", "Please enter your name.")
        return

    flight_id = flight_tree.item(selected_flight)['values'][0]
    
    # Insert into booked flights
    cursor.execute("INSERT INTO booked_flights (flight_id, user_name) VALUES (%s, %s)", (flight_id, user_name))
    conn.commit()
    
    messagebox.showinfo("Success", "Flight booked successfully!")
    update_booked_flights(user_name)

# Function to cancel a booked flight
def cancel_flight():
    selected_booking = booked_tree.focus()
    if not selected_booking:
        messagebox.showerror("Error", "Please select a booked flight to cancel.")
        return

    booking_id = booked_tree.item(selected_booking)['values'][0]
    cursor.execute("DELETE FROM booked_flights WHERE booking_id = %s", (booking_id,))
    conn.commit()
    
    messagebox.showinfo("Success", "Flight cancelled successfully!")
    update_booked_flights(user_name_entry.get())

# Function to update the available flights list
def update_available_flights():
    flights = fetch_available_flights()
    for row in flight_tree.get_children():
        flight_tree.delete(row)
    for flight in flights:
        flight_tree.insert('', 'end', values=flight)

# Function to update the booked flights list
def update_booked_flights(user_name):
    booked_flights = fetch_booked_flights(user_name)
    for row in booked_tree.get_children():
        booked_tree.delete(row)
    for flight in booked_flights:
        booked_tree.insert('', 'end', values=flight)

# Tkinter GUI
root = tk.Tk()
root.title("Flight Booking System")

# User name label and entry
user_name_label = tk.Label(root, text="User Name:")
user_name_label.grid(row=0, column=0, padx=10, pady=10)
user_name_entry = tk.Entry(root)
user_name_entry.grid(row=0, column=1, padx=10, pady=10)

# Available flights list
flight_frame = tk.Frame(root)
flight_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Add a new "Flight Time" column to the Treeview for available flights
flight_tree = ttk.Treeview(flight_frame, columns=("ID", "Flight Number", "Start", "Destination", "Price", "Flight Time"), show="headings")
flight_tree.heading("ID", text="ID")
flight_tree.heading("Flight Number", text="Flight Number")
flight_tree.heading("Start", text="Start")
flight_tree.heading("Destination", text="Destination")
flight_tree.heading("Price", text="Price")
flight_tree.heading("Flight Time", text="Flight Time")
flight_tree.column("ID", width=50)
flight_tree.column("Price", width=100)
flight_tree.column("Flight Time", width=100)
flight_tree.pack()

# Book flight button
book_button = tk.Button(root, text="Book Flight", command=book_flight)
book_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Booked flights list
booked_frame = tk.Frame(root)
booked_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Add a new "Flight Time" column to the Treeview for booked flights
booked_tree = ttk.Treeview(booked_frame, columns=("Booking ID", "Flight Number", "Start", "Destination", "Price", "Flight Time"), show="headings")
booked_tree.heading("Booking ID", text="Booking ID")
booked_tree.heading("Flight Number", text="Flight Number")
booked_tree.heading("Start", text="Start")
booked_tree.heading("Destination", text="Destination")
booked_tree.heading("Price", text="Price")
booked_tree.heading("Flight Time", text="Flight Time")
booked_tree.column("Booking ID", width=100)
booked_tree.column("Price", width=100)
booked_tree.column("Flight Time", width=100)
booked_tree.pack()

# Cancel flight button
cancel_button = tk.Button(root, text="Cancel Flight", command=cancel_flight)
cancel_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Initialize the available flights list
update_available_flights()

root.mainloop()
