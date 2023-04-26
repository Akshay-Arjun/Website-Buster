import tkinter as tk
from tkinter import ttk, filedialog
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import urllib.parse

def scan_website():
    website = website_entry.get()
    suffix_file = suffix_file_entry.get()

    # Read the suffixes from the file
    with open(suffix_file, 'r') as f:
        suffixes = f.read().splitlines()

    # Create a thread pool
    max_workers = 10
    pool = ThreadPoolExecutor(max_workers=max_workers)

    # Create a list to store the results
    results = []

    # Define a worker function for the thread pool
    def scan_suffix(suffix):
        suffix = urllib.parse.quote(suffix, safe='')

        url = website + suffix

        try:
            response = requests.get(url)
            status_code = response.status_code
            size = len(response.content)
        except requests.exceptions.RequestException as e:
            status_code = 'Error'
            size = 'N/A'

        results.append((url, status_code, size))

    # Use the thread pool to run the worker function for each suffix
    for suffix in suffixes:
        pool.submit(scan_suffix, suffix)

    # Wait for all threads to finish
    pool.shutdown()

    # Update the treeview with the results
    treeview.delete(*treeview.get_children())
    for result in results:
        treeview.insert('', 'end', values=result)

def select_suffix_file():
    suffix_file = filedialog.askopenfilename(filetypes=(('Text files', '*.txt'),))
    suffix_file_entry.delete(0, 'end')
    suffix_file_entry.insert(0, suffix_file)

# Create the main window
root = tk.Tk()
root.title('Website Enumeration')

# Create the input fields
website_label = tk.Label(root, text='Website URL:')
website_label.pack()
website_entry = tk.Entry(root)
website_entry.pack()

suffix_frame = tk.Frame(root)
suffix_frame.pack()

suffix_label = tk.Label(suffix_frame, text='Suffix file:')
suffix_label.pack(side='left')
suffix_file_entry = tk.Entry(suffix_frame)
suffix_file_entry.pack(side='left')
suffix_file_button = tk.Button(suffix_frame, text='Browse', command=select_suffix_file)
suffix_file_button.pack(side='left')

scan_button = tk.Button(root, text='Scan', command=scan_website)
scan_button.pack()

# Create the results table
columns = ('URL', 'Status Code', 'Size')
treeview = ttk.Treeview(root, columns=columns, show='headings')
treeview.heading('URL', text='URL')
treeview.heading('Status Code', text='Status Code')
treeview.heading('Size', text='Size')
treeview.pack()

root.mainloop()
