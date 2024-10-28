# Simple Attendance Management System in Python

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![MySQL](https://img.shields.io/badge/mysql-v8.0+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)

A robust and user-friendly Attendance Management System built with Python and MySQL. This desktop application helps educational institutions manage student attendance efficiently with features like multiple division support, secure authentication, and detailed attendance tracking.

## 🚀 Features

- **Secure Authentication System**
  - User registration and login
  - Password hashing for security
  - Session management

- **Student Management**
  - Add new students
  - Manage student records
  - Multiple division support (CEA, CEB, CEC, CED, CEE)

- **Attendance Tracking**
  - Mark attendance with checkboxes
  - Date-wise attendance records
  - Automatic timestamp recording

- **User-Friendly Interface**
  - Clean and intuitive GUI
  - Easy navigation
  - Division-wise student lists
  - Scrollable attendance view

- **Administrative Features**
  - Password change functionality
  - User account management
  - Data persistence with MySQL

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

```bash
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package installer)
```

## 🔧 Required Python Packages

```bash
- tkinter
- mysql-connector-python
- tkcalendar
- bcrypt
```

## 💻 Installation

1. Clone the repository:
```bash
git clone https://github.com/inodbandara-official/attendance-management-system-in-py.git
cd attendance-management-system-in-py
```

2. Install required packages:
```bash
pip install mysql-connector-python tkcalendar bcrypt
```

3. Set up the MySQL database:
```sql
CREATE DATABASE pythonproject;
USE pythonproject;

CREATE TABLE admins (
    username VARCHAR(50) PRIMARY KEY,
    password_hash BINARY(60) NOT NULL
);

-- Create tables for each division
CREATE TABLE cea (
    enrollment VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    status ENUM('Present', 'Absent') DEFAULT NULL,
    date_day DATE
);

-- Repeat similar table creation for ceb, cec, ced, cee
```

4. Update database configuration:
Edit the `DB_CONFIG` dictionary in the code with your MySQL credentials:
```python
self.DB_CONFIG = {
    "host": "localhost",
    "user": "your_username",
    "password": "your_password",
    "database": "pythonproject"
}
```

## 🎯 Usage

1. Run the application:
```bash
python attendance_system.py
```

2. Login/Sign up:
   - Create a new account if first time user
   - Login with existing credentials

3. Main Features:
   - Select division from dropdown
   - Click "Get Students Details" to view student list
   - Mark attendance using checkboxes
   - Click "Update Attendance" to save records
   - Use "Add Student" to register new students
   - "Change Password" for account security

## 📁 Project Structure

```
attendance-management-system-in-py/
├── attendance_system.py    # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── database/
    └── schema.sql        # Database schema
```

## 🔒 Security Features

- Password hashing using bcrypt
- SQL injection prevention with prepared statements
- Secure session management
- Input validation
- Error handling for database operations

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Inod Bandara**
- [:octocat:](https://github.com/inodbandara-official)
- [:mailbox_with_mail:](in.banu.ban@gmail.com)

## ⭐ Support

If you find this project helpful, please consider giving it a star on GitHub!

## 📧 Contact

For any queries or suggestions, please reach out through:
- GitHub Issues
- Pull Requests
- Project Discussion Board

---
Made with ❤️ by Inod Bandara
