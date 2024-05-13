import os 
import configparser
import mysql.connector
import csv
import subprocess
import tkinter as tk
import webbrowser
import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkinter import simpledialog
from smartcard.System import readers
from PIL import Image, ImageTk
from smartcard.Exceptions import CardConnectionException
from io import BytesIO
from tksheet import Sheet
from datetime import datetime, timedelta
from customtkinter import *
from CTkMenuBar import *

#database
DB_HOST = 'localhost'
DB_USER = 'auto'
DB_PASSWORD = 'password'
DB_NAME = 'auto'

try:
    db_connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = db_connection.cursor()
except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)

# Configuration file path
CONFIG_FILE_PATH = "config_IDCARD.ini"

# Function to save configuration to a file
def save_config(directory):
    config = configparser.ConfigParser() 
    config['DEFAULT'] = {'Directory': directory}
    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)

# Function to load configuration from file
def load_config():
    if os.path.exists(CONFIG_FILE_PATH):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)
        if 'DEFAULT' in config and 'Directory' in config['DEFAULT']:
            return config['DEFAULT']['Directory']
    print("Config file not found or directory not specified.")
    return ""


selected_directory = load_config()  # Load the directory from the config file


def select_directory(): 
    global selected_directory
    directory = filedialog.askdirectory()
    if directory:
        selected_directory = directory
        dir_label.configure(text=f"Selected Directory: {selected_directory}")
        c_url_label.configure(text=f"Current Web URL :  {selected_web_url}")
        messagebox.showinfo("Directory Selected", f"Selected directory: {selected_directory}")
        save_config(selected_directory)


# Thailand ID Smartcard
def thai2unicode(data):
    result = bytes(data).decode('tis-620')
    return result.strip()

def getData(connection, cmd, req=[0x00, 0xc0, 0x00, 0x00]):
    data, sw1, sw2 = connection.transmit(cmd)
    data, sw1, sw2 = connection.transmit(req + [cmd[-1]])
    return [data, sw1, sw2]

def gregorian_to_buddhist(gregorian_date):
    year_buddhist = gregorian_date.year + 543
    return year_buddhist, gregorian_date.month, gregorian_date.day

def is_card_expired(expire_date_str):
    expire_date = datetime.strptime(expire_date_str, '%Y%m%d')
    return expire_date < datetime.now()

def write_csv(card_data, file_path):
    fieldnames = ['CID', 'EN Fullname', 'TH Fullname', 'Gender', 'Date of Birth', 'Issue Date', 'Expire Date', 'Address']
    
    with open(file_path, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerow({
            'CID': card_data['CID'],
            'EN Fullname': card_data['EN Fullname'],
            'TH Fullname': card_data['TH Fullname'],
            'Gender': card_data['Gender'],
            'Date of Birth': card_data['Date of Birth'],
            'Issue Date': card_data['Issue Date'],
            'Expire Date': card_data['Expire Date'],
            'Address': card_data['Address']
        })
# Function to save the phone number to the database
def save_phone_number():
    phone_number = phone_var.get()
    cid = cid_var.get()  # Get the CID of the person whose card is currently inserted
    
    # Check if the phone number is empty or does not have 10 characters
    if not phone_number or len(phone_number) != 10:
        messagebox.showerror("Error", "กรุณาใส่เบอร์โทรศัพท์ 10 หลัก")
        return

    try:
        # Update the database with the phone number for the person with the given CID
        cursor.execute("UPDATE ID_CARD SET PHONE_NUMBER = %s WHERE CID = %s", (phone_number, cid))
        db_connection.commit()
        messagebox.showinfo("Success", "Phone number saved to the database.")
    except mysql.connector.Error as error:
        print("Error updating phone number in the database:", error)

GENDER_MAPPING = {"1": "M", "2": "F", "3": "O"}

def cid_already_exists(cid):
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        # Check if CID exists in the database
        cursor.execute("SELECT * FROM ID_CARD WHERE CID = %s", (cid,))
        existing_cid = cursor.fetchone()

        connection.close()

        return existing_cid is not None
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return False  # Return False on error

def read_card_data_and_display_photo():
    if not selected_directory:
        messagebox.showerror("Error", "กรุณาเลือกตำแหน่งเซฟภาพก่อนเริ่มอ่านค่า")
        return  
    
    try:
        connection = wait_for_card_insertion()
        if connection is None:
            messagebox.showinfo("Card Insertion", "โปรดเสียบการ์ด")
            return
        
        atr = connection.getATR()
        if atr[0] == 0x3B and atr[1] == 0x67:
            req = [0x00, 0xc0, 0x00, 0x01]
        else:
            req = [0x00, 0xc0, 0x00, 0x00]
            
        data, sw1, sw2 = connection.transmit(SELECT + THAI_CARD)
        # CID
        data = getData(connection, CMD_CID, req)
        cid_var.set(thai2unicode(data[0]))
        data = getData(connection, CMD_THFULLNAME, req)

        # TH
        thn_var.set(thai2unicode(data[0]).replace('#', ' '))
        data = getData(connection, CMD_ENFULLNAME, req)
        enn_var.set(thai2unicode(data[0]).replace('#', ' '))
        # EN
        data = getData(connection, CMD_BIRTH, req)
        dob_date_str = thai2unicode(data[0])
        dob_date = datetime.strptime(dob_date_str, '%Y%m%d').strftime('%Y-%m-%d')
        dob_var.set(dob_date)
        # GENDER
        data = getData(connection, CMD_GENDER, req)
        gender_var.set(thai2unicode(data[0]))
        # ISSUE
        data = getData(connection, CMD_ISSUE, req)
        issue_date_str = thai2unicode(data[0])
        issue_date = datetime.strptime(issue_date_str, '%Y%m%d').strftime('%Y-%m-%d')
        issue_var.set(issue_date)
        # Expire
        data = getData(connection, CMD_EXPIRE, req)
        expire_date_str = thai2unicode(data[0])
        expire_date = datetime.strptime(expire_date_str, '%Y%m%d').strftime('%Y-%m-%d')
        expire_date_var.set(expire_date)
        # Address
        data = getData(connection, CMD_ADDRESS, req)
        address_var.set(thai2unicode(data[0]).replace('#', ' '))
        
        # Gender
        data = getData(connection, CMD_GENDER, req)
        gender_value = thai2unicode(data[0])
        gender_label = GENDER_MAPPING.get(gender_value, "Unknown")
        gender_var.set(gender_label)

        # Save photo to file with full name without prefix "Mr." and without underscores
        full_name = enn_var.get().replace("Mr. ", "")  # Remove "Mr." and underscores

        # Photo retrieval
        photo_data = b''  
        for apdu in APDU_PHOTO:
            data = getData(connection, apdu['apdu'], req)
            photo_data += bytearray(data[0])

        # Save photo to file
        with open(os.path.join(selected_directory, f"{full_name}.jpg"), "wb") as f:
            f.write(photo_data)

        # Display photo
        image = Image.open(BytesIO(photo_data))
        photo = ImageTk.PhotoImage(image)
        photo_label.config(image=photo)
        photo_label.image = photo  

        # Get current date and time in the Buddhist calendar
        current_date_time = datetime.now()
        buddhist_year = current_date_time.year + 543
        buddhist_date_time = current_date_time.replace(year=buddhist_year)

        # Convert expiration date to datetime object
        expire_date_obj = datetime.strptime(expire_date, '%Y-%m-%d')

        # Calculate days until expiration
        days_until_expire = (expire_date_obj - buddhist_date_time).days


        
        card_data = {
            "CID": cid_var.get(),
            "TH Fullname": thn_var.get(),
            "EN Fullname": enn_var.get(),
            "Date of Birth": dob_var.get(),
            "Gender": gender_var.get(),
            "Issue Date": issue_var.get(),
            "Expire Date": expire_date_var.get(),
            "Address": address_var.get()
        }
        
        # Display pop-up message
        if days_until_expire < 0:
            messagebox.showinfo("Card Expired", "บัตรหมดอายุแล้ว !")
        else:
            messagebox.showinfo("Card Expiration Status", f"บัตรจะหมดอายุใน {expire_date}. "
                                                          f"\nบัตรจะหมดอายุในอีก: {days_until_expire} วัน.")
        
        file_path = "ID_CARD.csv"
        write_csv(card_data, file_path)  
        save_to_database(card_data)
        
                        # Fetching card data...
        cid = cid_var.get()

        if cid_already_exists(cid):
            messagebox.showinfo("Welcome", f"Welcome , {thn_var.get()}!")
        else:
            messagebox.showinfo("Welcome", f"Welcome, {thn_var.get()}!")

        connection.disconnect()
    
    except CardConnectionException as e:            
        messagebox.showerror("Error", "Error reading card: " + str(e))

        
def gregorian_to_buddhist(date):
    # Convert a Gregorian date to a Buddhist date
    year = date.year + 543
    return year, date.month, date.day

def wait_for_card_insertion():
    card_inserted = False
    while not card_inserted:
        try:
            reader = readers()[0]
            connection = reader.createConnection()
            connection.connect()
            atr = connection.getATR()
            if atr[0] == 0x3B and atr[1] == 0x67:
                req = [0x00, 0xc0, 0x00, 0x01]
            else:
                req = [0x00, 0xc0, 0x00, 0x00]

            data, sw1, sw2 = connection.transmit(SELECT + THAI_CARD)
            card_inserted = True
            return connection
        except Exception as e:
            continue

# Check card
SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08]
THAI_CARD = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]
CMD_CID = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]
CMD_THFULLNAME = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0x64]
CMD_ENFULLNAME = [0x80, 0xb0, 0x00, 0x75, 0x02, 0x00, 0x64]
CMD_BIRTH = [0x80, 0xb0, 0x00, 0xD9, 0x02, 0x00, 0x08]
CMD_GENDER = [0x80, 0xb0, 0x00, 0xE1, 0x02, 0x00, 0x01]
CMD_ISSUER = [0x80, 0xb0, 0x00, 0xF6, 0x02, 0x00, 0x64] 
CMD_ISSUE = [0x80, 0xb0, 0x01, 0x67, 0x02, 0x00, 0x08]
CMD_EXPIRE = [0x80, 0xb0, 0x01, 0x6F, 0x02, 0x00, 0x08]
CMD_ADDRESS = [0x80, 0xb0, 0x15, 0x79, 0x02, 0x00, 0x64]

APDU_PHOTO = [
    {'key':'APDU_PHOTO1','apdu':[0x80, 0xb0, 0x01, 0x7B, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO2','apdu':[0x80, 0xb0, 0x02, 0x7A, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO3','apdu':[0x80, 0xb0, 0x03, 0x79, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO4','apdu':[0x80, 0xb0, 0x04, 0x78, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO5','apdu':[0x80, 0xb0, 0x05, 0x77, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO6','apdu':[0x80, 0xb0, 0x06, 0x76, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO7','apdu':[0x80, 0xb0, 0x07, 0x75, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO8','apdu':[0x80, 0xb0, 0x08, 0x74, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO9','apdu':[0x80, 0xb0, 0x09, 0x73, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO10','apdu':[0x80, 0xb0, 0x0A, 0x72, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO11','apdu':[0x80, 0xb0, 0x0B, 0x71, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO12','apdu':[0x80, 0xb0, 0x0C, 0x70, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO13','apdu':[0x80, 0xb0, 0x0D, 0x6F, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO14','apdu':[0x80, 0xb0, 0x0E, 0x6E, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO15','apdu':[0x80, 0xb0, 0x0F, 0x6D, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO16','apdu':[0x80, 0xb0, 0x10, 0x6C, 0x02, 0x00, 0xFF]},
    {'key':'APDU_PHOTO17','apdu':[0x80, 0xb0, 0x11, 0x6B, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO18','apdu':[0x80, 0xb0, 0x12, 0x6A, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO19','apdu':[0x80, 0xb0, 0x13, 0x69, 0x02, 0x00, 0xFF] },
    {'key':'APDU_PHOTO20','apdu':[0x80, 0xb0, 0x14, 0x68, 0x02, 0x00, 0xFF] },
]


def save_to_database(card_data):
    try:
        sql = "INSERT INTO ID_CARD (CID, EN_FULLNAME, TH_FULLNAME, GENDER,DATE_OF_BIRTH, ISSUE_DATE, EXPIRE_DATE, ADDRESS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (card_data["CID"], card_data["EN Fullname"], card_data["TH Fullname"], card_data["Gender"],card_data["Date of Birth"], card_data["Issue Date"], card_data["Expire Date"], card_data["Address"])
        cursor.execute(sql, val)
        db_connection.commit()
        print("Record inserted successfully into ID_CARD table")
    except mysql.connector.Error as error:
        print("Error inserting record into ID_CARD table:", error)
# Function to fetch data from the database
# Function to fetch data from the database
def fetch_data():
    cursor.execute("SELECT * FROM ID_CARD")
    data = cursor.fetchall()
    return data
# Function to adjust column widths to fit content

# Function to search for data based on CID
def search_data(cid):
    cursor.execute("SELECT * FROM ID_CARD WHERE CID LIKE %s", ('%' + cid + '%',))
    searched_data = cursor.fetchall()
    return searched_data
# Function to update the Sheet with data
def update_sheet(data):
    sheet.set_sheet_data(data)
    sheet.headers([f[0] for f in cursor.description])
    sheet.fit_columns()

def open_another_program():
    try:
        subprocess.Popen(["/usr/bin/python3", "/home/auto/Desktop/FullApp/com_encodings.py"])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def open_set_url():
    global selected_directory

    def save_web_url():
        web_url = url_entry.get()
        c_url_label.configure(text=f"Current Web URL :  {web_url}")
        # Save the web URL to the config file
        save_config_web_url(web_url)
        messagebox.showinfo("Web URL Updated", f"Web URL updated: {web_url}")

    settings_window = tk.Toplevel()
    settings_window.title("Set Web URL")
    settings_window.configure(bg="gray10")

    url_label = tk.Label(settings_window, text="Enter Web URL:", font=("Helvetica", 12), bg="gray10", fg="white")
    url_label.grid(row=0, column=0, padx=10, pady=5)

    url_entry = tk.Entry(settings_window, font=("Helvetica", 12))
    url_entry.grid(row=0, column=1, padx=10, pady=5)

    save_button = CTkButton(settings_window, text="Save", command=save_web_url, font=("Helvetica", 16))
    save_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    settings_window.mainloop()
def save_config_web_url(web_url):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'Directory': selected_directory, 'WebURL': web_url}
    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)

def load_config_web_url():
    if os.path.exists(CONFIG_FILE_PATH):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)
        if 'DEFAULT' in config and 'WebURL' in config['DEFAULT']:
            return config['DEFAULT']['WebURL']
    print("Config file not found or Web URL not specified.")
    return ""

selected_directory = load_config()
selected_web_url = load_config_web_url()

def open_website():
    web_url = load_config_web_url()
    if web_url:
        webbrowser.open(web_url)
    else:
        messagebox.showerror("Error", "Web URL not found. Please set a Web URL first.")

def load_config_web_url():
    if os.path.exists(CONFIG_FILE_PATH):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)
        if 'DEFAULT' in config and 'WebURL' in config['DEFAULT']:
            return config['DEFAULT']['WebURL']
    print("Config file not found or Web URL not specified.")
    return ""
def save_to_csv():
    global sheet  # Add this line to make the sheet global within this function

    if sheet is None:
        messagebox.showerror("Error", "กรุณาเปิดตารางก่อน")
        return

    try:
        # Get the data from the sheet
        sheet_data = sheet.get_sheet_data()

        # Ask user for the directory to save the CSV file
        save_directory = filedialog.askdirectory()
        if not save_directory:
            messagebox.showerror("Error", "No directory selected. CSV file not saved.")
            return

        # Generate the file name with the current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        csv_file_name = f"id_data_{current_date}.csv"
        csv_file_path = os.path.join(save_directory, csv_file_name)

        # Write the data to the CSV file
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # Write headers
            writer.writerow([header for header in sheet_data[0]])
            # Write data
            writer.writerows(sheet_data[1:])

        messagebox.showinfo("Success", f"CSV file saved successfully: {csv_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save CSV file: {e}")
set_appearance_mode("dark")
root = ctk.CTk()
root.title("Thai ID Card Reader")
root.geometry("1200x800")

menu = CTkMenuBar(root)
button_1 = menu.add_cascade("File")
button_3 = menu.add_cascade("Settings")
button_4 = menu.add_cascade("About")

dropdown1 = CustomDropdownMenu(widget=button_1)
dropdown1.add_option(option="Export to CSV", command=save_to_csv)
dropdown1.add_option(option="Exit", command=root.destroy)
dropdown1.add_separator()

dropdown3 = CustomDropdownMenu(widget=button_3)
dropdown3.add_option(option="Save Photos Directory", command=select_directory)
dropdown3.add_option(option="Set Web URL", command=open_set_url)


dropdown4 = CustomDropdownMenu(widget=button_4)
def open_user_guide():
    instructions = "HOW TO USE:\n\n1. Click 'Settings' to select where to save images.\n2. Click 'Read Card' to read the card data.\n3. Click 'Open FaceRec' to enter Face Recognition step."
    tk.messagebox.showinfo("User Guide", instructions)

dropdown4.add_option(option="User Guide", command=open_user_guide)

tabs = ctk.CTkFrame(root)
tabs.pack(fill="both", expand=True, padx=10, pady=10)


cid_var = tk.StringVar()
thn_var = tk.StringVar()
enn_var = tk.StringVar()
dob_var = tk.StringVar()
gender_var = tk.StringVar()
issue_var = tk.StringVar()
expire_date_var = tk.StringVar()
address_var = tk.StringVar()
phone_var = tk.StringVar()

labels = ["CID:", "TH Fullname:", "EN Fullname:", "Date of Birth:", "Gender:", "Issue Date:", "Expire Date:", "Address:", "Phone Number"]
for i, label_text in enumerate(labels):
    label = CTkLabel(tabs, text=label_text, font=("Helvetica", 20))
    label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

display_labels = []
vars = [cid_var, thn_var, enn_var, dob_var, gender_var, issue_var, expire_date_var, address_var, phone_var]
for i, var in enumerate(vars):
    display_label = CTkLabel(tabs, textvariable=var, font=("Helvetica", 20))
    display_label.grid(row=i, column=1, sticky="w", padx=10, pady=5)
    display_labels.append(display_label)

photo_label = ttk.Label(tabs)
photo_label.grid(row=0, column=2, rowspan=10, padx=15, pady=5)

dir_label = CTkLabel(tabs, text=f"Selected Directory: {selected_directory}", font=("Helvetica", 20))
dir_label.grid(row=12, column=0, columnspan=2, padx=10, pady=5)

c_url_label = CTkLabel(tabs, text=f"Current Web URL : {selected_web_url} ", font=("Helvetica", 20))
c_url_label.grid(row=13, column=0, columnspan=2, padx=10, pady=5)

read_button = CTkButton(tabs, text="Read Card", command=read_card_data_and_display_photo, font=("Helvetica", 20))
read_button.grid(row=10, column=0, columnspan=1, padx=10, pady=15, sticky="ew")

phone_label = CTkLabel(tabs, text="Enter Phone Number:", font=("Helvetica", 20))
phone_label.grid(row=9, column=0, sticky="ew", padx=10, pady=5)

phone_entry = ttk.Entry(tabs, textvariable=phone_var, font=("Helvetica", 20))
phone_entry.grid(row=9, column=1, sticky="w", padx=10, pady=5)

save_phone_button = CTkButton(tabs, text="Save Phone Number", command=save_phone_number, font=("Helvetica", 20))
save_phone_button.grid(row=9, column=2, padx=10, pady=10)

open_program_button = CTkButton(tabs, text="Open FaceRecognition", command=open_another_program, font=("Helvetica", 20))
open_program_button.grid(row=10, column=1, padx=10, pady=10)

open_website_button = CTkButton(tabs, text="Open Report Website", command=open_website, font=("Helvetica", 20))
open_website_button.grid(row=10, column=2, padx=10, pady=10)


# instructions_label = CTkLabel(root, text="HOW TO USE:\n\n1. Click 'Setting' to select where to save images.\n2. Click 'Read Card' to read the card data.\n3. Click 'Open FaceRec' to enter Face Recognition step.", font=("Helvetica", 20))
# instructions_label.pack(side="bottom", pady=10) 

sheet = None

def open_information_window():
    global sheet  # Add this line to make the sheet global

    info_window = tk.Toplevel(root)
    info_window.title("Information Window")
    info_window.configure(bg="gray10")

    # Create the sheet widget
    sheet = Sheet(info_window, show_row_index=True, headers=["CID", "EN Fullname", "TH Fullname", "Gender", "Date of Birth", "Issue Date", "Expire Date", "Address", "Phone Number"])
    sheet.enable_bindings(("single_select", "row_select", "column_select", "row_width_resize", "column_width_resize", "arrowkeys", "right_click_popup_menu", "rc_select", "rc_insert_row", "rc_delete_row", "copy", "cut", "paste", "undo", "expand_grid"))

    # Add the Sheet to the window
    sheet.pack(fill="both", expand=True, padx=10, pady=10)

    # Function to update the Sheet with data
    def update_sheet(data):
        sheet.set_sheet_data(data)
        sheet.headers([f[0] for f in cursor.description])

    # Function to handle searching based on CID
    def search_cid():
        cid = search_var.get()
        data = search_data(cid)
        update_sheet(data)

    # Fetch all data from the database initially
    initial_data = fetch_data()

    # Update the Sheet with initial data
    update_sheet(initial_data)

    # Add the Sheet to the window
    sheet.pack(fill="both", expand=True, padx=10, pady=10)

    # Add a search box for CID
    search_var = tk.StringVar(info_window)
    search_entry = ttk.Entry(info_window, textvariable=search_var)
    search_entry.pack(padx=10, pady=(10, 0), fill="x")

    search_button = ttk.Button(info_window, text="Search", command=search_cid)
    search_button.pack(padx=10, pady=(5, 10), anchor="e")



open_info_button = ctk.CTkButton(root, text="Open Sheet", command=open_information_window, font=("Helvetica", 20))
open_info_button.pack(padx=10, pady=10)

root.mainloop()
