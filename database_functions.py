import tkinter as tk
import tkinter.font as font
from tkinter import ttk, messagebox
import sqlite3
from tkinter import PhotoImage, Label
from PIL import Image, ImageTk


# Connect to the database
conn = sqlite3.connect('cruise_info.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS cruises
            (id, Price, Location, Dates, ton, shipURL, shipName)''')

#Insert data into the table
# Check if the table is empty
c.execute("SELECT COUNT(*) FROM cruises")
number_of_rows = c.fetchone()[0]

# If the table is empty, initalize(must keep the table with at least one row)
if number_of_rows == 0:
    c.execute("INSERT INTO cruises VALUES (?, ?, ?, ?, ?, ?, ?)", 
              ('NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'))


#c.execute("INSERT INTO cruises VALUES (?, ?, ?, ?, ?, ?, ?)", 
#          ('24', '$199', 'New York City (Brooklyn) New York; Newport; Boston United States; P... New York City (Brooklyn) New York', 'May 04-May 12, 2024', '29', 'https://www.cruisewatch.com/cruise/8-night-caribbean/404618', 'MSC Meraviglia'))

#c.execute("INSERT INTO cruises VALUES (?, ?, ?, ?, ?, ?, ?)", 
#          ('28', '$199', 'Seward (Anchorage), Alaska; Juneau, Alaska; Skagway; Ketchikan (Ward Cove), Ak; Vancouver', 'May 06-May 13, 2024', '37', 'https://www.cruisewatch.com/cruise/7-night-alaska/373160', 'Norwegian Jewel'))
# Save (commit) the changes
conn.commit()


# Declare the Entry widgets as global variables
id_entry = None
price_entry = None
location_entry = None
ton_entry=None
shipURL_entry=None
shipname_entry=None

id=None
price=None
location=None
ton=None
shipURL=None
shipname=None


# Function to insert data
def insert_data():
    # Insert data into the database
    id = id_entry.get()
    price = price_entry.get()
    location = location_entry.get()
    ton=ton_entry.get()
    shipURL=shipURL_entry.get()
    shipname=shipname_entry.get()
    c.execute("INSERT INTO cruises VALUES (?, ?, ?, ?, ?, ?, ?)", (id, price, location,'NA',ton,shipURL,shipname))
    conn.commit()

    # Show a success message
    messagebox.showinfo("Success", "Data inserted successfully")




# Function to delete data
def delete_data():
    # Delete data from the database
    id = id_entry.get()

    shipname=shipname_entry.get()
    
    c.execute("DELETE FROM cruises WHERE id = ?", (id,))
    c.execute("DELETE FROM cruises WHERE shipName = ?", (shipname,))
    conn.commit()

    # Show a success message
    messagebox.showinfo("Success", "Data deleted successfully")



# Function to lookup data
def lookup_data():
    # Lookup data from the database
    id = id_entry.get()
    shipname = shipname_entry.get()
    if id:
        c.execute("SELECT * FROM cruises WHERE id = ?", (id,))
    elif location:
        c.execute("SELECT * FROM cruises WHERE shipName = ?", (shipname,))
    else:
        return

    rows = c.fetchall()

    # Show the retrieved data
    for row in rows:
        print(row)

# Function to create a new window for data insertion
def open_insert_window():
    
    global id_entry, price_entry, location_entry, ton_entry, shipURL_entry, shipname_entry
    global id, price, location, ton, shipURL, shipname


    insert_window = tk.Toplevel(window)
    insert_window.title("Insert Data")
    insert_window.geometry("800x600")  # Increase the window size

    id_label = ttk.Label(insert_window, text="id", font=("Arial", 20))  # Increase the font size
    id_label.pack()
    id_entry = ttk.Entry(insert_window, font=("Arial", 20))  # Increase the font size
    id_entry.pack()

    price_label = ttk.Label(insert_window, text="Price", font=("Arial", 20))  # Increase the font size
    price_label.pack()
    price_entry = ttk.Entry(insert_window, font=("Arial", 20))  # Increase the font size
    price_entry.pack()

    location_label = ttk.Label(insert_window, text="Location", font=("Arial", 20))  # Increase the font size
    location_label.pack()
    location_entry = ttk.Entry(insert_window, font=("Arial", 20))  # Increase the font size
    location_entry.pack()

    ton_label=ttk.Label(insert_window, text="ton", font=("Arial", 20))
    ton_label.pack()
    ton_entry=ttk.Entry(insert_window, font=("Arial", 20))
    ton_entry.pack()

    shipURL_label=ttk.Label(insert_window, text="shipURL", font=("Arial", 20))
    shipURL_label.pack()
    shipURL_entry=ttk.Entry(insert_window, font=("Arial", 20))
    shipURL_entry.pack()

    shipname_label=ttk.Label(insert_window, text="shipname", font=("Arial", 20))
    shipname_label.pack()
    shipname_entry=ttk.Entry(insert_window, font=("Arial", 20))
    shipname_entry.pack()


    

    insert_button = tk.Button(insert_window, text="Insert Data", command=insert_data)
    insert_button.pack()

    

# Function to create a new window for data lookup
def open_lookup_window():
    global id_entry, price_entry, location_entry, ton_entry, shipURL_entry, shipname_entry
    global id, price, location, ton, shipURL, shipname


    lookup_window = tk.Toplevel(window)
    lookup_window.title("Lookup Data")
    lookup_window.geometry("800x600")  # Increase the window size

    id_label = ttk.Label(lookup_window, text="id", font=("Arial", 20))  # Increase the font size
    id_label.pack()
    id_entry = ttk.Entry(lookup_window, font=("Arial", 20))  # Increase the font size
    id_entry.pack()

    shipname_label=ttk.Label(lookup_window, text="shipname", font=("Arial", 20))
    shipname_label.pack()
    shipname_entry=ttk.Entry(lookup_window, font=("Arial", 20))
    shipname_entry.pack()

    lookup_button = tk.Button(lookup_window, text="Lookup Data", command=lookup_data)
    lookup_button.pack()


# Function to create a new window for data deletion
def open_delete_window():
    global id_entry, price_entry, location_entry, ton_entry, shipURL_entry, shipname_entry
    global id, price, location, ton, shipURL, shipname

    delete_window = tk.Toplevel(window)
    delete_window.title("Delete Data")
    delete_window.geometry("800x600")  # Increase the window size

    id_label = ttk.Label(delete_window, text="id", font=("Arial", 20))  # Increase the font size
    id_label.pack()
    id_entry = ttk.Entry(delete_window, font=("Arial", 20))  # Increase the font size
    id_entry.pack()

    shipname_label=ttk.Label(delete_window, text="shipname", font=("Arial", 20))
    shipname_label.pack()
    shipname_entry=ttk.Entry(delete_window, font=("Arial", 20))
    shipname_entry.pack()


    delete_button = tk.Button(delete_window, text="Delete Data", command=delete_data)
    delete_button.pack()


# Create the main window
window = tk.Tk()

window.title("SQL Operator")
window.geometry("600x400")  # Increase the window size

# Load the image file
image = Image.open("background.bmp")
bg_image = ImageTk.PhotoImage(image)

# Create a label with the image
bg_label = Label(window, image=bg_image)

# Place the label on the window
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

font.nametofont("TkDefaultFont").configure(size=20)  # default the font size
insert_button = ttk.Button(window, text="Insert Data", command=open_insert_window, width=20)  # Increase the font size
insert_button.pack(side='bottom', pady=20)

delete_button = ttk.Button(window, text="Delete Data", command=open_delete_window, width=20)  # Increase the font size
delete_button.pack(side='bottom', pady=20)

lookup_button = ttk.Button(window, text="Lookup Data", command=open_lookup_window, width=20)  # Increase the font size
lookup_button.pack(side='bottom', pady=20)
window.mainloop()
conn.close()