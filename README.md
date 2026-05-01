# 📚 Library Management System

A desktop library management application built with Python, using the **MVC architecture** (Model-View-Controller). It supports book management, OCR-based book recognition from images, and includes Unit, Integration, and System tests.

---

## Features

- List, Add, Delete, and Search books
- Sort books by Title, Author, or Year
- Update book status (Available, Lent out, Missing, Deleted)
- Upload a book cover image and recognize the title using OCR (Tesseract)
- Data is stored and persisted in a JSON file
- Unit, Integration, and System tests included

---

## Technologies

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Main language |
| Tkinter | GUI |
| Pillow (PIL) | Image handling |
| pyocr + Tesseract | OCR text recognition |
| JSON | Data storage |
| unittest | Testing |

---

## Project Structure

```
library-management-system/
│
├── main.py                  # Entry point
├── model.py                 # Data logic (Model)
├── view.py                  # GUI (View)
├── controller.py            # Application logic (Controller)
├── books.json               # Library data file
│
├── UniTestModel_.py         # Unit tests for model
├── IntegrationTestController.py  # Integration tests
├── system.py                # System tests
│
└── README.md
```

---

## Installation

**1. Clone the repository:**
```bash
git clone https://github.com/your-username/library-management-system.git
cd library-management-system
```

**2. Install dependencies:**
```bash
pip install pillow pyocr
```

**3. Install Tesseract OCR:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Make sure Tesseract is added to your system PATH

**4. Run the application:**
```bash
python main.py
```

---

## Run Tests

```bash
# Unit tests
python -m unittest UniTestModel_.py

# Integration tests
python -m unittest IntegrationTestController.py

# System tests
python -m unittest system.py
```

---

## Screenshots


<img width="1367" height="751" alt="image" src="https://github.com/user-attachments/assets/7f28f975-70df-4a26-b097-e6ff37b39818" />

---


## University

**Technische Hochschule Deggendorf (THD)**  
Programmierung 2 – Semester 2
