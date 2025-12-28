import cv2

def load_face_cascade():
    """Load the face cascade from the XML file."""
    face_cascade = cv2.CascadeClassifier('eye/haarcascade_eye.xml')  
    return face_cascade

def detect_faces(frame, face_cascade):
    """Detect faces in the given frame using the provided face cascade."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)  
    return faces
