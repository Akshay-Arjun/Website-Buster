# Website-Buster
GUI Website scanner similar to dir-buster using python.

# Installation
- Python should be installed on your computer.
- Clone the git repo using ```git clone https://github.com/Akshay-Arjun/Website-Buster```.
- Install requirements using ```pip install -r requirements.txt```.
- Run the programm by ```python3 main.py```.

# Usage
- Enter the website url to scan in the Website URL feild.
- Select the suffixes wordlist by using browse button.
- Click scan to run the scan.

# Ouput
- Output displays the scanned url , response code & size of the response.

# Future Updates
- Improve the threading implementation to start requests as soon as a suffix is read from the file.
- Add option to check different HTTP Request Methods (e.g., GET, POST).
- Add options for customizing the scan parameters (e.g., timeout, user-agent).
- Add a feature for exporting the scan results to a file.
- Add support for scanning multiple websites at once.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more information.
