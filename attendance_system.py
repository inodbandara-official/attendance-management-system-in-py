# Inod Bandara Productions 

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import tkcalendar
import time
from datetime import datetime
import bcrypt
from typing import List, Tuple, Optional

class AttendanceSystem:
    def __init__(self):
        # Database configuration - Should be moved to a config file in production
        self.DB_CONFIG = {
            "host": "localhost",
            "user": "root",
            "password": "poudeL46@",
            "database": "pythonproject"
        }
        
        # Constants
        self.DIVISIONS = ("CEA", "CEB", "CEC", "CED", "CEE")
        self.WINDOW_SIZE = {
            "login": "500x300",
            "main": "450x450",
            "signup": "300x300"
        }
        
        # Initialize main window
        self.root = tk.Tk()
        self.setup_login_window()
        
        # Initialize database connection
        self.initialize_database()
        
        self.root.mainloop()

    def setup_login_window(self):
        """Setup the login window with improved UI"""
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        # Window configuration
        self.root.title("Attendance Management System")
        self.root.geometry(self.WINDOW_SIZE["login"])
        self.root.resizable(False, False)
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Attendance Management System",
            font=('Helvetica', 14, 'bold')
        )
        title_label.pack(pady=10)
        
        # Login frame
        login_frame = ttk.LabelFrame(main_frame, text="Login", padding="10")
        login_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Username
        ttk.Label(login_frame, text="Username:").pack(anchor=tk.W)
        username_entry = ttk.Entry(login_frame, textvariable=self.username_var)
        username_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Password
        ttk.Label(login_frame, text="Password:").pack(anchor=tk.W)
        password_entry = ttk.Entry(
            login_frame,
            textvariable=self.password_var,
            show="*"
        )
        password_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(login_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Login",
            command=self.handle_login
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Sign Up",
            command=self.show_signup_window
        ).pack(side=tk.LEFT)

    def initialize_database(self):
        """Initialize database connection with error handling"""
        try:
            self.connection = mysql.connector.connect(**self.DB_CONFIG)
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                f"Failed to connect to database: {err}"
            )
            self.root.destroy()

    def handle_login(self):
        """Handle login with secure password checking"""
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        try:
            cursor = self.connection.cursor(prepared=True)
            query = "SELECT password_hash FROM admins WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            
            if result and self.verify_password(password, result[0]):
                self.show_main_window(username)
            else:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password"
                )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Login failed: {err}")
        finally:
            cursor.close()

    def show_main_window(self, username: str):
        """Display main window after successful login"""
        self.root.withdraw()  # Hide login window
        
        # Create main window
        main_window = tk.Toplevel()
        main_window.title(f"Welcome {username}")
        main_window.geometry(self.WINDOW_SIZE["main"])
        main_window.resizable(False, False)
        
        # Create main container with padding
        main_frame = ttk.Frame(main_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header frame
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Date display
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        ttk.Label(
            header_frame,
            text=current_date,
            font=("Helvetica", 10)
        ).pack(side=tk.RIGHT)
        
        # User info
        ttk.Label(
            header_frame,
            text=f"Logged in as: {username}",
            font=("Helvetica", 11)
        ).pack(side=tk.LEFT)
        
        # Division selection
        division_frame = ttk.LabelFrame(
            main_frame,
            text="Select Division",
            padding="10"
        )
        division_frame.pack(fill=tk.X, pady=(0, 20))
        
        division_var = tk.StringVar(value=self.DIVISIONS[0])
        division_combo = ttk.Combobox(
            division_frame,
            textvariable=division_var,
            values=self.DIVISIONS,
            state="readonly"
        )
        division_combo.pack(fill=tk.X)
        
        # Create attendance frame
        attendance_frame = ttk.LabelFrame(
            main_frame,
            text="Attendance",
            padding="10"
        )
        attendance_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable frame for attendance
        canvas = tk.Canvas(attendance_frame)
        scrollbar = ttk.Scrollbar(
            attendance_frame,
            orient="vertical",
            command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Add buttons with improved layout
        buttons = [
            ("Get Students", lambda: self.get_student_details(
                scrollable_frame,
                division_var.get()
            )),
            ("Update Attendance", self.update_attendance),
            ("Add Student", self.show_add_student_window),
            ("Change Password", self.show_change_password_window),
            ("Logout", lambda: self.logout(main_window))
        ]
        
        for text, command in buttons:
            ttk.Button(
                button_frame,
                text=text,
                command=command
            ).pack(side=tk.LEFT, padx=5)

    @staticmethod
    def hash_password(password: str) -> bytes:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @staticmethod
    def verify_password(password: str, hashed: bytes) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode(), hashed)

    def get_student_details(self, frame: ttk.Frame, division: str):
        """Fetch and display student details"""
        # Clear existing widgets
        for widget in frame.winfo_children():
            widget.destroy()
            
        try:
            cursor = self.connection.cursor(prepared=True)
            query = f"SELECT enrollment, name FROM {division.lower()}"
            cursor.execute(query)
            students = cursor.fetchall()
            
            # Create header
            ttk.Label(frame, text="Enrollment").grid(row=0, column=0, padx=5)
            ttk.Label(frame, text="Name").grid(row=0, column=1, padx=5)
            ttk.Label(frame, text="Present").grid(row=0, column=2, padx=5)
            
            # Create student rows
            self.attendance_vars = []
            for i, (enrollment, name) in enumerate(students, 1):
                ttk.Label(frame, text=enrollment).grid(
                    row=i, column=0, padx=5, pady=2
                )
                ttk.Label(frame, text=name).grid(
                    row=i, column=1, padx=5, pady=2
                )
                
                var = tk.BooleanVar(value=True)
                self.attendance_vars.append((enrollment, var))
                ttk.Checkbutton(
                    frame,
                    variable=var
                ).grid(row=i, column=2, padx=5, pady=2)
                
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to fetch students: {err}")
        finally:
            cursor.close()

    def update_attendance(self):
        """Update attendance records"""
        try:
            cursor = self.connection.cursor(prepared=True)
            date = datetime.now().strftime("%Y-%m-%d")
            
            for enrollment, var in self.attendance_vars:
                status = "Present" if var.get() else "Absent"
                query = """
                    UPDATE students 
                    SET status = %s, date_day = %s 
                    WHERE enrollment = %s
                """
                cursor.execute(query, (status, date, enrollment))
            
            self.connection.commit()
            messagebox.showinfo("Success", "Attendance updated successfully")
            
        except mysql.connector.Error as err:
            self.connection.rollback()
            messagebox.showerror("Error", f"Failed to update attendance: {err}")
        finally:
            cursor.close()

    def logout(self, window: tk.Toplevel):
        """Handle logout"""
        window.destroy()
        self.root.deiconify()  # Show login window again

    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()

if __name__ == "__main__":
    app = AttendanceSystem()
