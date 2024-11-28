# prompt: write all my code in one cell and clean it and add explanation for each part

# Import necessary libraries
from tkinter import messagebox
import pandas as pd
from datetime import datetime
from tabulate import tabulate

#import jalali_pandas  # Install if not already installed
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


import tkinter as tk
from tkinter import ttk
import sys
import subprocess


#from msilib.schema import Class


"""# Mount Google Drive
drive.mount('/content/drive')
# Read data from the text file
with open('/content/drive/MyDrive/Lab DATA/LAB DATA 3.txt','r') as my_file:
  data_in_file = my_file.read()"""


def process_data(data_in_file):
  # Split the data into separate entries based on the separator
  data_in_file_Number = data_in_file.split('\n=============================\n\n')
  DATA_list = []
  # Clean up each entry by replacing newline characters with spaces
  for item in data_in_file_Number:
    new_item = item.replace('\n', '            ')
    new_item = new_item.replace('           ', '            ')
    new_item = new_item.replace('CBC :            ', 'CBC : type            ')
    new_item = new_item.replace('U/A :            ', 'U/A : type            ')
    new_item = new_item.replace('C.S.F Fluid Analysis :            ', 'C.S.F Fluid Analysis : type            ')
    # Check if the string contains "CBC" and replace "R.B.C" with "RBC"
    if "CBC" in new_item:
      new_item = new_item.replace("R.B.C", "RBC")
    # Check if the string contains "U/A" and replace "PH" with "P.H"
    if "U/A" in new_item:
      new_item = new_item.replace("PH", "P.H")
    # Check if the string contains "U/A" and replace "PH" with "P.H"
    if "C.S.F Fluid Analysis" in new_item:
      new_item = new_item.replace("Poly", "Poly CSF")
      new_item = new_item.replace("Lymph", "Lymph CSF")
    DATA_list.append(new_item)

  # Split each entry further by another separator
  data_in_file_Number_split = []
  for element in DATA_list:
    data_in_file_Number_split.append(element.split('                          '))
  # Remove empty elements from data_in_file_Number_split
  data_in_file_Number_split = data_in_file_Number_split[:-1]
  # Separate the date and lab information
  date_list = []
  lab_list = []
  for item in data_in_file_Number_split:
    date_list.append(item[0])
    lab_list.append(item[1])

    
  # Extract key-value pairs from lab information
  info_list = []
  for item in lab_list:
    cells = item.split('            ')
    info = {}
    for line in cells:
      if ':' in line:
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()
        if value:
          info[key] = value
    info_list.append(info)

  # Convert date strings to datetime objects
  date_list_datetime = []
  for date_str in date_list:
    try:
      date_obj = datetime.strptime(date_str, '%Y/%m/%d %H:%M')
      date_list_datetime.append(date_obj.strftime('%m/%d'))
    except ValueError:
      print(f"Could not parse date: {date_str}")
      date_list_datetime.append(None)
  # Create a list of dictionaries combining dates and lab information
  data = []
  for date, info in zip(date_list_datetime, info_list):
      data.append({'Date': date, **info})


  # Create a pandas DataFrame from the list of dictionaries
  df = pd.DataFrame(data)
  # Replace NaN values with empty strings
  df = df.fillna('')
  # Set the 'Date' column as the index and sort by it
  df = df.set_index(df.columns[0])
  df = df.sort_index()
  # Transpose the DataFrame
  df_t = df.T

  def update_row(df, index_name, number_value):
    """
    Updates or adds a row in the DataFrame.

    If a row with the given index_name exists and has 'type' in ANY column,
    it deletes the row and adds a new row with the specified number_value
    in the 'number' column and "test" in the first non-"number" column.

    If the index_name does not exist, it adds a new row with the
    specified number_value in the 'number' column and "test"
    in the first non-"number" column.
    """
    if index_name in df.index:
      if 'type' in df.loc[index_name].values:
        df = df.drop(index_name)
        df.loc[index_name] = ['' for _ in range(df.shape[1])]
        df.loc[index_name, 'number'] = number_value
        # Find the first column that is not "number" and assign "test"
        for col in df.columns:
          if col != 'number':
            df.loc[index_name, col] = "TYPE"
            break  # Exit the loop after assigning "test"
    else:
      # Index doesn't exist, add a new row
      df.loc[index_name] = ['' for _ in range(df.shape[1])]
      df.loc[index_name, 'number'] = number_value
      # Find the first column that is not "number" and assign "test"
      for col in df.columns:
        if col != 'number':
          df.loc[index_name, col] = "TYPE"
          break  # Exit the loop after assigning "test"
    return df

  def number_row(df, index_name, value):
    """Assigns a value to a specific column of a row if the index exists."""
    if index_name in df.index:
      df.loc[index_name, "number"] = value
    return df



  df_t.insert(0, 'number', 1000)


  df_t = update_row(df_t, 'CBC', 100)

  df_t = number_row(df_t, 'WBC', 101)
  df_t = number_row(df_t, 'Hb', 102)
  df_t = number_row(df_t, 'PLT', 103)
  df_t = number_row(df_t, 'Poly', 104)
  df_t = number_row(df_t, 'Lymph', 105)

  df_t = update_row(df_t, 'Biochemistry', 200)
  df_t = number_row(df_t, 'B.S', 200.5)
  df_t = number_row(df_t, 'Na', 201)
  df_t = number_row(df_t, 'K', 202)
  df_t = number_row(df_t, 'Bun', 203)
  df_t = number_row(df_t, 'Creatinine', 204)
  df_t = number_row(df_t, 'Calcium', 205)
  df_t = number_row(df_t, 'AST', 206)
  df_t = number_row(df_t, 'ALT', 207)
  df_t = number_row(df_t, 'ALP', 208)
  df_t = number_row(df_t, 'Bill.T', 209)
  df_t = number_row(df_t, 'Bili D', 210)
  df_t = number_row(df_t, 'CRP N', 211)
  df_t = number_row(df_t, 'ESR', 212)
  df_t = number_row(df_t, 'Alb', 213)
  df_t = number_row(df_t, 'T-pro', 214)
  df_t = number_row(df_t, 'TG', 215)
  df_t = number_row(df_t, 'Chol', 216)


  df_t = update_row(df_t, 'U/A', 300)

  df_t = number_row(df_t, 'P.H', 301)
  df_t = number_row(df_t, 'Specific Gravity', 302)
  df_t = number_row(df_t, 'Urine Proteins', 303)
  df_t = number_row(df_t, 'W.B.C', 304)
  df_t = number_row(df_t, 'R.B.C', 305)
  df_t = number_row(df_t, 'Nitrite', 306)
  df_t = number_row(df_t, 'Glucose', 307)


  df_t = update_row(df_t, 'Culture', 400)

  df_t = number_row(df_t, 'Blood Culture', 401)
  df_t = number_row(df_t, 'U/C Culture', 402)
  df_t = number_row(df_t, 'Stool Culture', 403)


  df_t = update_row(df_t, 'VBG', 500)

  df_t = number_row(df_t, 'PH', 501)
  df_t = number_row(df_t, 'PCO2', 502)
  df_t = number_row(df_t, 'HCO3', 503)
  df_t = number_row(df_t, 'BE', 504)


  df_t = update_row(df_t, 'C.S.F Fluid Analysis', 600)

  df_t = number_row(df_t, 'Protein csf', 601)
  df_t = number_row(df_t, 'Glucose CSF', 602)
  df_t = number_row(df_t, 'W.B.C CSF', 603)
  df_t = number_row(df_t, 'R.B.C CSF', 604)
  df_t = number_row(df_t, 'Poly CSF', 605)
  df_t = number_row(df_t, 'Lymph CSF', 606)



  df_t = update_row(df_t, 'other lab test', 700)


  df_t = df_t.sort_values(by=['number'])
  df_t = df_t.drop(columns=['number'])
  df_t = df_t[df_t.apply(lambda row: row.astype(str).str.strip().any(), axis=1)]
  return df_t


# MAKE GUI FILE

# MAKE GUI FILE
# prompt: use Tkinter library to make a .exe for my code. i want a place that can enter txet for i use it as data_in_file and a button after click on that run my code(i add it manualy) and a place that i show df_t_str 

import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import shutil

def run_code():
  """Runs the code and displays the output."""
  global df_t_str

  # Get the input text from the text widget
  data_in_file = text_input.get("1.0", tk.END)

  # Your existing code to process the data and create df_t
  # (Replace this with your actual code)
  # ... (Your existing data processing functions and logic) ...
  # ... (After processing, df_t should be your DataFrame) ...
  df_t = process_data(data_in_file)
  # Convert df_t to a string for display in the output area
  df_t_str = df_t.to_csv(sep='\t',lineterminator='\n')
  #df_t_str = tabulate(df_t, headers='keys', tablefmt='fancy_grid')
  #df_t_str = "DATE"+ df_t_str
  # Clear previous output and insert the new output
  output_text.delete("1.0", tk.END)
  output_text.insert(tk.END, df_t_str)
  """Copies the output to the clipboard."""
  root.clipboard_clear()
  root.clipboard_append(df_t_str)
  root.update()  

'''def browse_file():
    """Opens a file dialog to select a file."""
    filepath = filedialog.askopenfilename()
    if filepath:
        with open(filepath, "r") as file:
            text_input.delete("1.0", tk.END)
            text_input.insert(tk.END, file.read())'''

def paste_clipboard():
    """Pastes the text from the clipboard into the input text widget."""
    clipboard_text = root.clipboard_get()  # Get the clipboard content
    text_input.delete("1.0", tk.END)  # Clear any existing content
    text_input.insert(tk.END, clipboard_text)  # Insert the clipboard content into the Text widget

def copy_output():
    """Copies the output to the clipboard."""
    root.clipboard_clear()
    root.clipboard_append(df_t_str)
    root.update()

def show_info():
    """Function to show information in a message box."""
    info_text = """About This App
This application is designed to streamline the process of handling lab data with ease and efficiency. It allows users to input data, process it, and view the results all in one place.

Developed By:
Sina Samieefard, a dedicated medical student with a passion for integrating technology with healthcare. This app reflects my goal to create tools that support data-driven decision-making in medical and scientific contexts.

November 2024"""
    
    messagebox.showinfo("Information", info_text)  # Show the message in a popup

root = tk.Tk()
root.title("Lab Data Processor")

# Create the menu bar
menu_bar = tk.Menu(root)

# Create the "Hospital" section (just for show, no action)
hospital_menu = tk.Menu(menu_bar, tearoff=0)
hospital_menu.add_command(label="Taleghani Pediatric Hospital-Gorgan", state="disabled")  # Label only, no action
menu_bar.add_cascade(label="Hospital", menu=hospital_menu)

# Create the "Info" section
info_menu = tk.Menu(menu_bar, tearoff=0)
info_menu.add_command(label="Information", command=show_info)  # Clicking triggers the show_info function
menu_bar.add_cascade(label="Info", menu=info_menu)

# Configure the window to display the menu bar
root.config(menu=menu_bar)

# Input Text Area
input_label = tk.Label(root, text="Enter Lab Data:")
input_label.pack()
text_input = tk.Text(root, height=10, width=70)
text_input.pack(padx=10)

# Frame to hold the buttons in one line
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Run Button
run_button = tk.Button(button_frame, text=" Paste↑ ", command=paste_clipboard)
run_button.pack(side='left', padx=5)

# Run Button
run_button = tk.Button(button_frame, text="  Run  ", command=run_code)
run_button.pack(side='left', padx=5)

# Copy Button
copy_button = tk.Button(button_frame, text=" Copy↓ ", command=copy_output)
copy_button.pack(side='left', padx=5)

# Output Text Area
output_label = tk.Label(root, text="Output:")
output_label.pack()
output_text = tk.Text(root, height=10, width=70)
output_text.pack(pady=10,padx=10)



root.mainloop()








#pyinstaller --onefile tk.py
