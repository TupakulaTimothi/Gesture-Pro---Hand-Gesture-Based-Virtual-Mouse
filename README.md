# Gesture-Pro---Hand-Gesture-Based-Virtual-Mouse
Gesture Pro is a real-time AI virtual mouse that lets users control their computer using hand gestures. Built with OpenCV, MediaPipe, and Flask, it supports cursor movement, clicks, scrolling, gesture customization, and a live web dashboard for seamless touchless interaction.

Gesture Pro is a real-time computer vision application that enables users to control their computer using hand gestures instead of a physical mouse. The system uses a webcam to detect hand movements and translates them into mouse actions such as cursor movement, clicking, and scrolling.

This project combines AI, computer vision, and web technologies to create a touchless human-computer interaction system.

🚀 Features:
🎯 Real-time hand tracking using MediaPipe

🖱️ Cursor movement using index finger

👆 Left click using thumb + index pinch

✌️ Right click using index + middle pinch

⬆️⬇️ Scroll using hand movement

🎛️ Gesture customization via web interface

📷 Live camera feed in browser

📊 Real-time action display

🤖 Built-in assistant for gesture help

🌐 Flask-based web dashboard

🛠️ Tech Stack:

Python – Core programming

OpenCV – Video capture & processing

MediaPipe – Hand tracking & landmark detection

PyAutoGUI – Mouse control automation

Flask – Web backend

HTML / CSS / JavaScript – Frontend UI

⚙️ How It Works:

Webcam captures real-time video

MediaPipe detects hand landmarks (21 points)

System identifies gestures based on finger positions

Gesture engine maps gestures to actions

PyAutoGUI executes mouse operations

Flask dashboard displays live feed and status

📂 Project Structure:

Gesture Pro/
│
├── app.py                  # Flask backend
├── gesture_engine.py       # Gesture detection logic
├── templates/
│   ├── index.html          # Main dashboard
│   └── customize.html      # Gesture customization UI
│
├── static/
│   └── style.css           # UI styling
│
└── README.md               # Project documentation
▶️ Installation & Setup
# Create environment
conda create -n gesture_env python=3.9
conda activate gesture_env

# Install dependencies
pip install opencv-python mediapipe pyautogui flask numpy

# Run the app
python app.py
Open browser:

http://127.0.0.1:5000

🎮 Gesture Controls:

Gesture	Action
Index Finger Move	Cursor Move
Thumb + Index Pinch	Left Click
Index + Middle Pinch	Right Click
Move Hand Up	Scroll Up
Move Hand Down	Scroll Down

💡 Use Cases:

Touchless computer control

Smart presentations

Accessibility tools

Interactive systems

AI-based HCI research


🚧 Limitations:

Requires good lighting conditions

Accuracy depends on camera quality

Single-hand detection only


🔮 Future Improvements:

Voice + gesture control

Custom gesture training (AI-based)

Multi-hand support

Save gesture settings permanently

Mobile integration

⭐ Conclusion
Gesture Pro demonstrates how computer vision and AI can replace traditional input devices, enabling a more natural and futuristic way of interacting with computers.
