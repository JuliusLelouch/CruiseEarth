import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import customtkinter

from tkintermapview import TkinterMapView
import webbrowser
import sqlite3
from geopy.geocoders import Nominatim



Arr = []
global df


# Function to convert an address to coordinates
def address_to_coordinates_latitude(address):
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(address)
    return location.latitude

def address_to_coordinates_longitude(address):
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(address)
    return location.longitude


# Create a SQLite database
conn = sqlite3.connect('cruise_info.db')

# Create a cursor object
c = conn.cursor()



# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()



# Scrape the data from the local database
def scrape_cruise(tupleArr):
    tempArrTuples = []
    
    # Connect to the SQLite database
    conn = sqlite3.connect('cruise_info.db')
    c = conn.cursor()

    # Fetch data from the database
    c.execute("SELECT * FROM cruises")
    rows = c.fetchall()

    # Close the connection
    conn.close()

    # Process the data
    for row in rows:
        # Each row is a tuple (month, price, link)
        tempArrTuples.append(row)

    return tempArrTuples

def first(myArr):
    
    myArr = scrape_cruise(myArr)
    df = pd.DataFrame(myArr, columns=['id', 'Price', 'Location', 'Dates', 'ton', 'shipURL', 'shipName'])
    df = df.drop_duplicates(subset=["Location", "Dates"], keep='first')
    df = df.sort_values(by='id')
    return df


customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    APP_NAME = "Cruise Earth"
    WIDTH = 1000
    HEIGHT = 780

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)
        self.destNum = 0
        self.marker_list = []
        self.poly_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(3, weight=1)

        self.button_next = customtkinter.CTkButton(master=self.frame_left,
                                                   text="Next CruiseLine",
                                                   command=self.next_marker_event)
        self.button_next.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_prev = customtkinter.CTkButton(master=self.frame_left,
                                                   text="Previous CruiseLine",
                                                   command=self.prev_marker_event)
        self.button_prev.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.cruiseName = customtkinter.CTkLabel(master=self.frame_left, corner_radius=6,
                                                 text="Click Next Destination",
                                                 height=100,
                                                 fg_color=["gray90", "gray13"])
        self.cruiseName.grid(pady=(20, 0), padx=(20, 20), row=2, column=0)

        self.button_prev = customtkinter.CTkButton(master=self.frame_left,
                                                   text="GoTo source",
                                                   command=self.listing_url_event)
        self.button_prev.grid(pady=(20, 0), padx=(20, 20), row=3, column=0)

        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=4, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["Google streetmap", "Google satellite"],
                                                           command=self.change_map)
        self.map_option_menu.grid(row=5, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")

        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Set default values
        self.map_widget.set_zoom(6)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
        self.map_widget.set_position(31, 121)  # Shanghai
        self.map_option_menu.set("Google streetMap")
        self.appearance_mode_optionemenu.set("Dark")
        customtkinter.set_appearance_mode("Dark")

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def next_marker_event(self):
        self.destNum += 1
        for poly in self.poly_list:
            poly.delete()
        for marker in self.marker_list:
            marker.delete()
        aa = df.at[self.destNum, 'shipName']
        b = df.at[self.destNum, 'ton']
        c = df.at[self.destNum, 'id']
        d = df.at[self.destNum, 'Dates']
        e = df.at[self.destNum, 'Price']
        a = df.at[self.destNum, 'Location'].split(';')
        a = [s.strip() for s in a]
        tempStr='Shipname: '+ aa +'\nTons: '+ b + '\nLine: '
        for i in a:
            tempStr += '\n' + i
        self.cruiseName.configure(text=tempStr)
        tempBool = False
        x = len(a)
        if a[0] == a[len(a)-1]:
            tempBool = True
            x -= 1
        tempArr = []
        for j in range(x):
            tempMarker = self.map_widget.set_address(a[j], marker=True)   ##描点
            if tempMarker:
                if tempBool and not j:
                        tempStr = str(j + 1) + '-' + str(len(a)) +'. '+ str(a[j])
                        tempMarker.set_text(tempStr)
                        self.marker_list.append(tempMarker)
                        tempArr.append(tempMarker.position)
                else:
                    tempStr = str(j+1) + '. '+ str(a[j])
                    tempMarker.set_text(tempStr)
                    self.marker_list.append(tempMarker)
                    tempArr.append(tempMarker.position)

        tempPoly = app.map_widget.set_polygon(tempArr, outline_color="red",
                                              border_width=12,
                                              name="switzerland_polygon")
        self.poly_list.append(tempPoly)
        self.map_widget.set_zoom(4)

    def prev_marker_event(self):
        for poly in self.poly_list:
            poly.delete()
        for marker in self.marker_list:
            marker.delete()
        self.destNum -= 1
        a = df.at[self.destNum, 'shipName']
        b = df.at[self.destNum, 'ton']
        c = df.at[self.destNum, 'id']
        d = df.at[self.destNum, 'Dates']
        e = df.at[self.destNum, 'Price']
        tempStr='Shipname: '+ aa +'\nTons: '+ b + '\nLine: '
        self.cruiseName.configure(text=tempStr)
        a = df.at[self.destNum, 'Location'].split(';')
        a = [s.strip() for s in a]
        tempBool = False
        x = len(a)
        if a[0] == a[len(a)-1]:
            tempBool = True
            x -= 1
        tempArr = []
        for j in range(x):
            tempMarker = self.map_widget.set_address(a[j], marker=True)   ##描点
            if tempMarker:
                if tempBool and not j:
                        tempStr = str(j + 1) + '-' + str(len(a)) +'. '+ str(a[j])
                        tempMarker.set_text(tempStr)
                        self.marker_list.append(tempMarker)
                        tempArr.append(tempMarker.position)
                else:
                    tempStr = str(j+1) + '. '+ str(a[j])
                    tempMarker.set_text(tempStr)
                    self.marker_list.append(tempMarker)
                    tempArr.append(tempMarker.position)
        tempPoly = app.map_widget.set_polygon(tempArr, outline_color="red",
                                              border_width=12,
                                              name="switzerland_polygon")    ##描线,多边形
        self.poly_list.append(tempPoly)
        self.map_widget.set_zoom(5)

    def listing_url_event(self):

        # The URL to open
        url = df.at[self.destNum, 'shipURL']

        # Open the URL in the user's default web browser
        webbrowser.open(url)

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "Google StreetMap":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                            max_zoom=22)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    df = first(Arr)
    app = App()
    app.start()
