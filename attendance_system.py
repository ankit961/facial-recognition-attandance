import os
import cv2
import face_recognition
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
from PIL import Image, ImageTk

# Paths
KNOWN_FACES_DIR = "known_faces"
ATTENDANCE_FILE = "attendance.csv"

# Global variables
known_face_encodings = []
known_face_names = []
attendance_set = set()
video_capture = None

# -------------------- Core Functions --------------------

def load_known_faces():
    global known_face_encodings, known_face_names
    known_face_encodings = []
    known_face_names = []

    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR)

    for person in os.listdir(KNOWN_FACES_DIR):
        person_dir = os.path.join(KNOWN_FACES_DIR, person)
        for img_name in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_name)
            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(person)

def mark_attendance(name):
    if name not in attendance_set:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ATTENDANCE_FILE, "a", newline="") as f:
            csv.writer(f).writerow([name, now])
        attendance_set.add(name)

# -------------------- GUI Functions --------------------

def start_recognition():
    load_known_faces()
    if not known_face_encodings:
        messagebox.showwarning("No Faces", "No known faces found. Please add students first.")
        return

    status_var.set("Starting camera... Press Q to stop.")
    global video_capture
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match = np.argmin(face_distances)
            if matches[best_match]:
                name = known_face_names[best_match]
                mark_attendance(name)

                top, right, bottom, left = [v * 4 for v in face_location]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Attendance Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    status_var.set("Camera stopped.")

def add_new_student():
    name = name_entry.get().strip().replace(" ", "_")
    if not name:
        messagebox.showerror("Error", "Please enter a valid student name.")
        return

    save_path = os.path.join(KNOWN_FACES_DIR, name)
    os.makedirs(save_path, exist_ok=True)

    status_var.set("Capturing face images...")
    cap = cv2.VideoCapture(0)

    count = 0
    while count < 5:
        ret, frame = cap.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)
        if face_locations:
            count += 1
            img_path = os.path.join(save_path, f"{count}.jpg")
            cv2.imwrite(img_path, frame)
            cv2.rectangle(frame, (face_locations[0][3], face_locations[0][0]),
                          (face_locations[0][1], face_locations[0][2]), (0, 255, 0), 2)
            cv2.putText(frame, f"Captured {count}/5", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Adding New Student", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    status_var.set(f"Captured 5 images for {name}.")
    messagebox.showinfo("Done", f"{name} added successfully!")

# -------------------- UI Setup --------------------

root = tk.Tk()
root.title("📷 Smart Attendance System")
root.geometry("600x400")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 11))
style.configure("Header.TLabel", font=("Arial", 16, "bold"))

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# --- Attendance Tab ---
tab_attendance = ttk.Frame(notebook)
notebook.add(tab_attendance, text="🎓 Attendance")

ttk.Label(tab_attendance, text="Face Recognition Attendance", style="Header.TLabel").pack(pady=20)
ttk.Button(tab_attendance, text="Start Camera & Recognize", command=start_recognition).pack(pady=10)

# --- Add Student Tab ---
tab_add = ttk.Frame(notebook)
notebook.add(tab_add, text="➕ Add Student")

ttk.Label(tab_add, text="Add New Student", style="Header.TLabel").pack(pady=20)
ttk.Label(tab_add, text="Student Name:").pack(pady=5)
name_entry = ttk.Entry(tab_add, width=30)
name_entry.pack(pady=5)
ttk.Button(tab_add, text="Capture Face Images", command=add_new_student).pack(pady=10)

# --- Status ---
status_var = tk.StringVar()
ttk.Label(root, textvariable=status_var, foreground="gray").pack(pady=5)

# Start
root.mainloop()
