import numpy as np
import matplotlib.pyplot as plt
import cv2

def resize_image(image):
    new_width = 300 
    new_height = int(image.shape[0] * (new_width / image.shape[1]))
    image = cv2.resize(image, (new_width, new_height))
    return image

def get_ycrcb_mask(image):
    # convert to YCrCb
    image_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    # set threshold
    lower_thresh_Y = np.array([25, 135, 85], dtype=np.uint8)
    upper_thresh_Y = np.array([255, 180, 135], dtype=np.uint8)

    # create mask
    msk_ycrcb = cv2.inRange(image_ycrcb, lower_thresh_Y, upper_thresh_Y)
    
    # morphology
    kernel = np.ones((4, 3), np.uint8)
    # msk_ycrcb_morpho = cv2.erode(msk_ycrcb, kernel, iterations=4)
    # msk_ycrcb_morpho = cv2.morphologyEx(msk_ycrcb, cv2.MORPH_ERODE, kernel=kernel, iterations=4)
    msk_ycrcb_morpho = cv2.morphologyEx(msk_ycrcb, cv2.MORPH_OPEN, kernel=kernel, iterations=2)
    msk_ycrcb_morpho = cv2.morphologyEx(msk_ycrcb, cv2.MORPH_CLOSE, kernel=kernel, iterations=2)
    
    return msk_ycrcb, msk_ycrcb_morpho
    

def get_contour_coord(image):
    mask_img = get_ycrcb_mask(image)[1]
    
    contours, _ = cv2.findContours(mask_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)
 
    # get coord contour
    x, y, w, h = cv2.boundingRect(max_contour)

    return x, y, w, h, max_contour

def detect_face_with_template(image, template):
    mask_ycrcb = get_ycrcb_mask(image)[1]
    x, y, w, h, _ = get_contour_coord(image)
    
    # template matching
    template = cv2.resize(template, (130, 130))
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    mask_crop = mask_ycrcb[y:y + h, x:x + w]
    result = cv2.matchTemplate(mask_crop, template, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Draw rect around face detect
    face_detect = np.copy(image)
    top_left = (max_loc[0] + x, max_loc[1] + y)
    bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
    cv2.rectangle(face_detect, top_left, bottom_right, (0, 0, 255), 2)

    face_crop = image[(max_loc[1] + y) : (top_left[1] + template.shape[0]), (max_loc[0] + x) : (top_left[0] + template.shape[1]), :]

    return face_detect, face_crop


    