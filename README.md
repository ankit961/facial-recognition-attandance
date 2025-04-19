# Face Recognition Attendance System

This project is a Tkinter-based desktop application for automated attendance using real-time face recognition. It uses `OpenCV`, `dlib`, and `face_recognition` libraries for detection and recognition.

---

## 💡 Features

- Live face detection using webcam
- Real-time face recognition
- Attendance marking with date and time
- Tkinter GUI with user-friendly interface
- Option to register new students
- Multiple images per student for robust recognition
- Auto-creation of CSV attendance files

---

## 📁 Project Structure

```
Face_recognition_based_attendance_system/
├── attendance.csv
├── attendance_system.py
├── haarcascade_frontalface_default.xml
├── known_faces/
│   ├── person1.jpg
│   ├── person2.jpg
│   └── ...
├── LICENSE
├── README.md
├── requirements.txt
├── StudentDetails/
│   └── Student Details.csv
├── TrainingImage/
│   └── (captured face images for training)
```

---

## 🔧 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Face_recognition_based_attendance_system.git
cd Face_recognition_based_attendance_system
```

### 2. Setup virtual environment
```bash
python3 -m venv facial-recognition-env
source facial-recognition-env/bin/activate  # Linux/macOS
facial-recognition-env\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install numpy Pillow dlib opencv-python face_recognition git+https://github.com/ageitgey/face_recognition_models
```

> **Note**: Make sure `cmake`, `build-essential`, `libopenblas-dev`, `liblapack-dev`, and `libx11-dev` are installed (Ubuntu).

```bash
sudo apt-get update
sudo apt-get install build-essential cmake libopenblas-dev liblapack-dev libx11-dev
```

---

## 🚀 Usage

### Run the app
```bash
python3 attendance_system.py
```

### ✍️ To Take Attendance
- Launch the app using the command above.
- Click the **"Take Attendance"** button in the GUI.
- The webcam will start and recognize known faces.
- Attendance is recorded in `attendance.csv` with timestamp.

### ➕ To Add a New Student
- Click the **"Register New Student"** button in the GUI.
- Enter the student's name when prompted.
- The system will capture multiple images from the webcam.
- Captured images are saved in `TrainingImage/` and encoded for future recognition.
- Student info is saved in `StudentDetails/Student Details.csv`.

---

## 📦 Requirements

To regenerate:
```bash
pip freeze > requirements.txt
```

---

## 🧠 How it works

- Uses `face_recognition` to encode all known faces from the `TrainingImage/` folder.
- During runtime, camera frames are compared with known encodings.
- Matches trigger attendance recording.

---

## 🙋 Contributing

Feel free to fork this project, open issues, or submit pull requests!

---

## 📝 License

MIT License

---

## 🔗 Credits
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [OpenCV](https://opencv.org)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)

