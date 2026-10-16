# TechVault — Smart Technical Inventory System

Hello! I am a 9th-grade Technical High School student specializing in Information Technology. I am currently studying at Yahya Gürsül Vocational and Technical Anatolian High School, and I previously studied at ODTÜ Development Foundation Schools.

I enjoy building practical projects to improve my programming skills and develop real-world software solutions.

This repository features **TechVault**, a Python-based technical inventory management system with both a Command-Line Interface (CLI) and a Graphical User Interface (GUI). The project supports device management and JSON-based data storage.

## Key Features & Software Architecture

- **Device Registration:** Add technical equipment by entering its name, brand, and model.
- **Unique Inventory IDs:** Automatically generate identifiers such as `TV-001`, `TV-002`, and more.
- **Inventory Listing:** Display registered devices and their details.
- **Device Deletion:** Remove devices using their unique inventory IDs.
- **Device Search:** Find specific devices by their inventory IDs.
- **Data Persistence:** Store inventory information in JSON files.
- **Backup Support:** Keep backup data for inventory recovery.
- **Input Handling:** Handle invalid menu choices and missing devices.
- **Interactive CLI:** Manage inventory through a command-line menu.
- **Graphical User Interface:** Manage inventory through a desktop window built with Python and Tkinter.
- **Incremental Development:** Develop and improve the project while learning Python programming concepts.

## Core Features

- Add new devices to the inventory.
- View all registered devices.
- Search for devices by inventory ID.
- Delete devices by inventory ID.
- Generate sequential inventory IDs automatically.
- Save and load inventory data using JSON.
- Handle missing devices and invalid input.
- Use either the CLI or GUI version.

## Tech Stack

- **Language:** Python 3
- **GUI Framework:** Tkinter and ttk
- **Data Storage:** JSON
- **Data Structures:** Lists and dictionaries
- **Control Flow:** Loops, conditional statements, and functions
- **File Handling:** Python file operations and `pathlib`
- **Version Control:** Git and GitHub
- **Development Environment:** Visual Studio Code

## Project Structure

```text
TechVault/
├── TechVault.py
├── gui.py
├── devices.json
├── techvault_meta.json
├── devices_backup.json
└── README.md
```

- `TechVault.py` — Command-line version of TechVault.
- `gui.py` — Graphical version of TechVault.
- `devices.json` — Stores inventory data.
- `techvault_meta.json` — Stores inventory metadata.
- `devices_backup.json` — Backup inventory data.
- `README.md` — Project documentation.

## How to Run

### CLI Version

1. Install Python 3.
2. Clone this repository.
3. Open a terminal in the project directory.
4. Run the application:

   ```bash
   python TechVault.py
   ```

### GUI Version

1. Make sure Python 3 is installed.
2. Open a terminal in the project directory.
3. Run the graphical application:

   ```bash
   python gui.py
   ```

## AI Assistance & Development Transparency

I believe in being transparent about how this project was developed.

- **CLI Version:** I developed the command-line version and its core inventory management features myself while learning Python.
- **GUI Version:** The graphical interface and its initial implementation were generated with the assistance of AI. As a 9th-grade Information Technology student, I have not yet learned enough about GUI development to build the entire interface independently.
- **My Learning Goal:** I am using this project to improve my programming skills, understand software architecture, and gradually learn how to implement more advanced features myself.

The GUI includes the following credit:

**Made with AI • Built with Python**

AI assistance is acknowledged to clearly distinguish my own work from AI-generated contributions.

## Future Improvements

- Improve JSON data validation and error handling.
- Add more advanced search and filtering options.
- Improve the GUI design and usability.
- Add inventory categories and sorting.
- Expand the system as my Python skills develop.

## Copyright & Usage Restrictions

Copyright (c) 2026 TechVault Project Author. All rights reserved.

No permission is granted to copy, redistribute, republish, modify, or reuse this project's code without prior written permission from the copyright holder, except as permitted by applicable law.

Viewing the repository for educational purposes, evaluation, or code review does not grant permission to reuse or redistribute the code.

No open-source license is granted by this notice. The copyright status and permitted use of AI-generated contributions may depend on applicable law and the relevant service terms.

---

**TechVault** is an ongoing learning project focused on Python programming, inventory management, and practical software development.
