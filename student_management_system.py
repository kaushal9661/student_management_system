import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------- DATABASE ----------------
# The database file is created automatically in the same folder.
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    course TEXT NOT NULL,
    marks REAL NOT NULL
)
""")
conn.commit()


# ---------------- FUNCTIONS ----------------
def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    id_entry.focus()


def load_students():
    for item in student_table.get_children():
        student_table.delete(item)

    cursor.execute("SELECT student_id, name, course, marks FROM students ORDER BY student_id")
    for row in cursor.fetchall():
        student_table.insert("", tk.END, values=row)


def add_student():
    student_id = id_entry.get().strip()
    name = name_entry.get().strip()
    course = course_entry.get().strip()
    marks_text = marks_entry.get().strip()

    if not student_id or not name or not course or not marks_text:
        messagebox.showwarning("Missing Information", "Please fill in all fields.")
        return

    try:
        marks = float(marks_text)
        if marks < 0 or marks > 100:
            messagebox.showwarning("Invalid Marks", "Marks must be between 0 and 100.")
            return
    except ValueError:
        messagebox.showwarning("Invalid Marks", "Please enter marks as a number.")
        return

    try:
        cursor.execute(
            "INSERT INTO students (student_id, name, course, marks) VALUES (?, ?, ?, ?)",
            (student_id, name, course, marks)
        )
        conn.commit()
        load_students()
        clear_fields()
        messagebox.showinfo("Success", "Student added successfully.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Duplicate ID", "This Student ID already exists.")


def select_student(event=None):
    selected = student_table.selection()
    if not selected:
        return

    values = student_table.item(selected[0], "values")
    clear_fields()
    id_entry.insert(0, values[0])
    name_entry.insert(0, values[1])
    course_entry.insert(0, values[2])
    marks_entry.insert(0, values[3])


def update_student():
    student_id = id_entry.get().strip()
    name = name_entry.get().strip()
    course = course_entry.get().strip()
    marks_text = marks_entry.get().strip()

    if not student_id or not name or not course or not marks_text:
        messagebox.showwarning("Missing Information", "Select a student or fill in all fields.")
        return

    try:
        marks = float(marks_text)
        if marks < 0 or marks > 100:
            messagebox.showwarning("Invalid Marks", "Marks must be between 0 and 100.")
            return
    except ValueError:
        messagebox.showwarning("Invalid Marks", "Please enter marks as a number.")
        return

    cursor.execute(
        "UPDATE students SET name = ?, course = ?, marks = ? WHERE student_id = ?",
        (name, course, marks, student_id)
    )
    conn.commit()

    if cursor.rowcount == 0:
        messagebox.showwarning("Not Found", "No student found with this ID.")
    else:
        load_students()
        clear_fields()
        messagebox.showinfo("Success", "Student record updated successfully.")


def search_student():
    student_id = id_entry.get().strip()
    if not student_id:
        messagebox.showwarning("Student ID Required", "Enter a Student ID to search.")
        return

    cursor.execute(
        "SELECT student_id, name, course, marks FROM students WHERE student_id = ?",
        (student_id,)
    )
    row = cursor.fetchone()

    for item in student_table.get_children():
        student_table.delete(item)

    if row:
        student_table.insert("", tk.END, values=row)
        clear_fields()
        id_entry.insert(0, row[0])
        name_entry.insert(0, row[1])
        course_entry.insert(0, row[2])
        marks_entry.insert(0, row[3])
    else:
        messagebox.showinfo("Search Result", "No student found with this ID.")
        load_students()


def delete_student():
    student_id = id_entry.get().strip()
    if not student_id:
        messagebox.showwarning("Student ID Required", "Select a student or enter a Student ID.")
        return

    answer = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete student {student_id}?"
    )
    if not answer:
        return

    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()

    if cursor.rowcount == 0:
        messagebox.showwarning("Not Found", "No student found with this ID.")
    else:
        load_students()
        clear_fields()
        messagebox.showinfo("Success", "Student record deleted successfully.")


# ---------------- GUI WINDOW ----------------
root = tk.Tk()
root.title("Student Management System")
root.geometry("850x570")
root.minsize(760, 520)
root.configure(bg="#eef2f7")

title_label = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 19, "bold"),
    bg="#263b63",
    fg="white",
    pady=14
)
title_label.pack(fill="x")

form_frame = tk.Frame(root, bg="#eef2f7", padx=20, pady=15)
form_frame.pack(fill="x")

tk.Label(form_frame, text="Student ID", font=("Arial", 10, "bold"),
         bg="#eef2f7").grid(row=0, column=0, sticky="w", padx=5, pady=6)
id_entry = tk.Entry(form_frame, width=27, font=("Arial", 10))
id_entry.grid(row=0, column=1, padx=5, pady=6)

tk.Label(form_frame, text="Student Name", font=("Arial", 10, "bold"),
         bg="#eef2f7").grid(row=0, column=2, sticky="w", padx=5, pady=6)
name_entry = tk.Entry(form_frame, width=27, font=("Arial", 10))
name_entry.grid(row=0, column=3, padx=5, pady=6)

tk.Label(form_frame, text="Course", font=("Arial", 10, "bold"),
         bg="#eef2f7").grid(row=1, column=0, sticky="w", padx=5, pady=6)
course_entry = tk.Entry(form_frame, width=27, font=("Arial", 10))
course_entry.grid(row=1, column=1, padx=5, pady=6)

tk.Label(form_frame, text="Marks (0-100)", font=("Arial", 10, "bold"),
         bg="#eef2f7").grid(row=1, column=2, sticky="w", padx=5, pady=6)
marks_entry = tk.Entry(form_frame, width=27, font=("Arial", 10))
marks_entry.grid(row=1, column=3, padx=5, pady=6)

button_frame = tk.Frame(root, bg="#eef2f7", pady=5)
button_frame.pack(fill="x")

button_style = {
    "font": ("Arial", 10, "bold"),
    "width": 13,
    "pady": 7,
    "relief": "flat",
    "cursor": "hand2"
}

tk.Button(button_frame, text="Add Student", bg="#287a4b", fg="white",
          command=add_student, **button_style).pack(side="left", padx=9)
tk.Button(button_frame, text="Update", bg="#2864a6", fg="white",
          command=update_student, **button_style).pack(side="left", padx=9)
tk.Button(button_frame, text="Search by ID", bg="#6c4aa0", fg="white",
          command=search_student, **button_style).pack(side="left", padx=9)
tk.Button(button_frame, text="Delete", bg="#b83b42", fg="white",
          command=delete_student, **button_style).pack(side="left", padx=9)
tk.Button(button_frame, text="Clear", bg="#596579", fg="white",
          command=clear_fields, **button_style).pack(side="left", padx=9)

table_frame = tk.Frame(root, bg="white", padx=15, pady=10)
table_frame.pack(fill="both", expand=True, padx=20, pady=(10, 15))

columns = ("student_id", "name", "course", "marks")
student_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
student_table.heading("student_id", text="Student ID")
student_table.heading("name", text="Student Name")
student_table.heading("course", text="Course")
student_table.heading("marks", text="Marks")

student_table.column("student_id", width=120, anchor="center")
student_table.column("name", width=220, anchor="w")
student_table.column("course", width=220, anchor="w")
student_table.column("marks", width=100, anchor="center")

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=student_table.yview)
student_table.configure(yscrollcommand=scrollbar.set)
student_table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
student_table.bind("<<TreeviewSelect>>", select_student)

load_students()
id_entry.focus()

def close_app():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_app)
root.mainloop()
