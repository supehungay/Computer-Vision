import cv2
import detect_face
import numpy as np

cap = cv2.VideoCapture(0) 

if not cap.isOpened():
    print("Không thể mở camera.")
    exit()

template = cv2.imread('./image/input/template2.png')

# Lặp để đọc và hiển thị video
while True:
    ret, frame = cap.read()

    if not ret:
        print("Không thể đọc frame.")
        break

    flipped_frame = cv2.flip(frame, 1)
    detect = detect_face.detect_face_with_template(flipped_frame, template)
    mask_img = detect_face.get_ycrcb_mask(flipped_frame)
    
    # Hiển thị frame
    cv2.imshow('Video1', detect[0])
    cv2.imshow('Video2', detect[1])
    cv2.imshow('Video3', mask_img[1])
    

    # Đợi 1 milisecond và kiểm tra xem người dùng có bấm 'q' để thoát không
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
