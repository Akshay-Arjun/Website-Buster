import tkinter as tk
from tkinter import ttk, filedialog
import requests
from bs4 import BeautifulSoup
import threading
import queue
import time

def scan_website():
    website = website_entry.get()
    suffix_file = suffix_file_entry.get()

    # Read the suffixes from the file
    with open(suffix_file, 'r') as f:
        suffixes = f.read().splitlines()

    # Create a queue to collect the results
    result_queue = queue.Queue()

    # Define a worker function for threading
    def scan_suffix(suffix):
        url = website + suffix
        try:
            response = requests.get(url)
            status_code = response.status_code
            size = len(response.content)
        except requests.exceptions.RequestException as e:
            status_code = 'Error'
            size = 'N/A'
        result_queue.put((url, status_code, size))

    # Use threading to run the worker function for each suffix
    threads = []
    for suffix in suffixes:
        t = threading.Thread(target=scan_suffix, args=(suffix,))
        t.start()
        threads.append(t)

    # Periodically check the queue for new results and update the treeview
    while any(t.is_alive() for t in threads) or not result_queue.empty():
        try:
            result = result_queue.get(block=False)
        except queue.Empty:
            pass
        else:
            treeview.insert('', 'end', values=result)
        time.sleep(0.1)

def select_suffix_file():
    suffix_file = filedialog.askopenfilename(filetypes=(('Text files', '*.txt'),))
    suffix_file_entry.delete(0, 'end')
    suffix_file_entry.insert(0, suffix_file)

# Create the main window
root = tk.Tk()
root.title('Website Scanner')

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
