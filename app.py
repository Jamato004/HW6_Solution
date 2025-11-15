import tkinter as tk
from tkinter import ttk, messagebox
from database import Student, SessionLocal

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Manager")

        # DB session
        self.db = SessionLocal()

        # -------- GUI Layout -------- 

        tk.Label(root, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(root, text="Major:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.name_entry = tk.Entry(root, width=30)
        self.major_entry = tk.Entry(root, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.major_entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(root, text="Add Student", command=self.add_student).grid(row=2, column=0, pady=10)
        tk.Button(root, text="View Students", command=self.view_students).grid(row=2, column=1, pady=10)
        tk.Button(root, text="Delete Selected", command=self.delete_selected).grid(row=2, column=2, padx=5)

        # Treeview Table
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Major"), show="headings", height=10)
        self.tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Major", text="Major")

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Major", width=150)

    # -------- Functions -------- 

    def add_student(self):
        name = self.name_entry.get().strip()
        major = self.major_entry.get().strip()

        if not name or not major:
            messagebox.showerror("Error", "Name and Major cannot be empty.")
            return

        student = Student(name=name, major=major)
        self.db.add(student)
        self.db.commit()

        messagebox.showinfo("Success", f"Student '{name}' added successfully.")
        self.name_entry.delete(0, tk.END)
        self.major_entry.delete(0, tk.END)

    def view_students(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        students = self.db.query(Student).all()
        for s in students:
            self.tree.insert("", "end", values=(s.id, s.name, s.major))

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No student selected.")
            return

        item = self.tree.item(selected[0])
        student_id = item["values"][0]

        student = self.db.query(Student).filter_by(id=student_id).first()
        if not student:
            messagebox.showerror("Error", "Student not found in database.")
            return

        self.db.delete(student)
        self.db.commit()

        self.view_students()
        messagebox.showinfo("Success", "Student deleted successfully.")

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
