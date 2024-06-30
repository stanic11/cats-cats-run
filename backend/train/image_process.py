import cv2
import os


class ImageProcessor:
    def __init__(self) -> None:
        self.haarCatXML = "../haarcascade_frontalcatface.xml"
        self.face_cascade = cv2.CascadeClassifier(self.haarCatXML)
        self.dataset_path = os.getcwd() + "\\dataset"

    def has_images(self):
        processed_data_path = os.path.join(self.dataset_path, "processed_data")
        # 遍历 processed_data 目录下的所有文件和文件夹
        for root, dirs, files in os.walk(processed_data_path):
            for file in files:
                if file.lower().endswith(
                        (".png", ".jpg", ".jpeg")
                ):  # 检查是否是图像文件
                    return True
        return False

    def recognize_face(self, img):
        if img is None or img.size == 0:
            return []
        # 获取猫脸
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.02,
            minNeighbors=3,
            minSize=(150, 150),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )
        return faces

    def process(self):
        input_path = os.path.join(self.dataset_path, "origin_data")
        output_path = os.path.join(self.dataset_path, "processed_data")

        folders = [
            f
            for f in os.listdir(input_path)
            if os.path.isdir(os.path.join(input_path, f))
        ]

        for folder in folders:
            folder_path = os.path.join(input_path, folder)
            count = 1
            for img_name in sorted(os.listdir(folder_path)):
                if img_name.lower().endswith(
                        (".png", ".jpg", ".jpeg")
                ):
                    img_path = os.path.join(folder_path, img_name)
                    image = cv2.imread(img_path)
                    faces = self.recognize_face(image)
                    if len(faces):
                        for x, y, w, h in faces:
                            cut_img = image[y : y + h, x : x + w]
                            save_dir = os.path.join(output_path, folder)
                            if not os.path.exists(save_dir):
                                os.makedirs(save_dir)
                            save_path = os.path.join(save_dir, f"{count}.jpg")
                            cv2.imwrite(save_path, cut_img)
                            count += 1  
