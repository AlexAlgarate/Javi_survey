# Selenium Survey Automation Project

## Overview

This project is based on automation using Selenium. The objective is to create entries in a survey by automating the process. The program opens a specified URL, searches for the survey element that meets the given criteria, and then clicks the "Finish" button. The process is enclosed within an infinite `while` loop to continuously create entries for as long as the program is running.

## Files

- `main.py`: The initial version of the automation script.
- `main_oop.py`: A refactored version of `main.py` with improved structure and maintainability using Object-Oriented Programming (OOP) principles.

## Example

The example provided in this project uses a different webpage to demonstrate the functionality.

## Requirements

Ensure you have the following dependencies installed. You can manage these dependencies using the provided `requirements.txt` file.

## Updating config.py file

Update config.py with the appropriate URL and web element locators for your survey.

### Dependencies

- `selenium`
- `chromedriver-autoinstaller`

To install the required dependencies, run:

```sh
pip install -r requirements.txt
```

To run the project (check the variables of config.py file fist):

```python
python ./main.py
```

### Important Notes

The script is designed to run indefinitely. To stop the script, you will need to manually terminate the process.

### Contributions

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
