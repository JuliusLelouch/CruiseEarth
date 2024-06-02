import sqlite3
import tkinter as tk
from tkinter import ttk

# Connect to the database
conn = sqlite3.connect('cruise_info.db')
c = conn.cursor()

# Function to fetch and display data
def display_data():
    # Execute the SELECT statement
    c.execute("SELECT * FROM cruises")

    # Fetch all rows
    rows = c.fetchall()

    # Print all rows
    for row in rows:
        print(row)



display_data()



# Close the connection to the database
conn.close()