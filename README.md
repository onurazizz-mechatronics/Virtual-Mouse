🖐️ Virtual Mouse Control via Hand Gestures
This project is a Human-Machine Interface (HMI) application that allows users to control the computer mouse cursor and trigger system commands using real-time hand gestures. It leverages Mediapipe for skeletal tracking and OpenCV for image processing.

🚀 Key Features
Adaptive Cursor Mapping: Uses np.interp to map camera coordinates to screen resolution, ensuring smooth and precise cursor movement.

Object-Oriented Architecture: Built with a modular class Finger structure for easy scalability and maintenance.

Dynamic Gesture Recognition: Calculates Euclidean distances between landmarks (self.dist) to detect clicks, scrolls, and system shortcuts (e.g., Windows+D).

Ergonomic ROI: Operates within a defined Region of Interest (ROI) to minimize physical strain and optimize tracking stability.

🛠️ Tech Stack
Python 3.x: Core logic and system integration.

OpenCV: Computer vision and real-time visualization.

Mediapipe: High-fidelity skeletal hand tracking (21 Landmark points).

PyAutoGUI / Pynput: OS-level mouse and keyboard event triggering.

NumPy: Mathematical normalization and coordinate transformation.

📐 Technical Overview
The system tracks 21 hand landmarks in real-time. By using the Wrist (Landmark 0) as a reference and the Index Finger Tip (Landmark 8) as the primary pointer, the algorithm achieves high stability even with low-cost webcams.

Note: Developed as a term project for the MEK114 course at Istanbul Health and Technology University.

📸 Demo
(Visuals to be updated) ![Demo Video Coming Soon](https://via.placeholder.com/640x360?text=Demo+Video+Coming+Soon)

💻 Installation
Clone the repository:

Bash

git clone https://github.com/yourusername/virtual-mouse.git
Install dependencies:

Bash

pip install -r requirements.txt
Run the application:

Bash

python main.py
