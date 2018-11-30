import face_recognition
from twilio.rest import Client
import cv2
a=""
video_capture = cv2.VideoCapture(0)
first_image = face_recognition.load_image_file(r"ravi.JPG")
first_face_encoding = face_recognition.face_encodings(first_image)[0]
second_image = face_recognition.load_image_file(r"jayanth.jpg")
second_face_encoding = face_recognition.face_encodings(second_image)[0]

known_face_encodings = [
    first_face_encoding,
    second_face_encoding
]
known_face_names = [
    "RaviTeja",
    "Jayanth"
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,0.54)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    
    for (top, right, bottom, left), name in zip(face_locations, face_names):
       
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

     
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)


        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        a=name
        #print(a)
        

    
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if a=="Unknown":
        client=Client("AC58001f46fbdb2c14aab8e9b12f9bfbe5", "51329ea5c6c53b3f2374d6fd41b0b641")
        client.messages.create(to="+919100709868", from_="+15028068544",body="Unsauthorized entry")    

video_capture.release()
cv2.destroyAllWindows()
