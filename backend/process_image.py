import cv2
import numpy as np
import os


def cat_face_recognize(img_path):
    cat_haar_path = "haarcascade_frontalcatface.xml"
    # 读取Haar特征分类器XML文件
    face_cascade = cv2.CascadeClassifier(cat_haar_path)
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError("Image could not be loaded")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 使用Haar特征分类器检测猫脸
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.02,
        minNeighbors=3,
        minSize=(150, 150),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    if len(faces) == 0:
        return None
    x, y, w, h = faces[0]
    cut_img = gray[y : y + h, x : x + w]
    # 调整图像大小以适应模型输入
    cut_img = cv2.resize(cut_img, (64, 64))
    img_array = np.array(cut_img, dtype=np.float32)
    return img_array
