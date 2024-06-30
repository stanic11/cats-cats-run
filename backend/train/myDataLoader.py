import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical


class DataLoader:
    def __init__(self, processed_path="processed_data", classes_num=6) -> None:
        self.output_path = os.path.join(os.getcwd(), "dataset")
        self.input_path = os.path.join(self.output_path, processed_path)
        self.classes_num = classes_num

    def imgToMatrix(self, img, target_size=(64, 64)):
        image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"Error reading image {img}")
        resized_image = cv2.resize(image, target_size)
        data = (
                resized_image.astype("float32") / 255.0
        )  # 将图像数据转换为浮点数，并归一化到[0, 1]
        return data.flatten()

    def save_images_with_labels(self):
        data_with_labels = []
        label_counter = 0
        for subdir, dirs, files in os.walk(self.input_path):
            if subdir == self.input_path:
                continue  # 跳过顶层目录
            print(f"Processing directory: {subdir} with label: {label_counter}")
            for file in files:
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    file_path = os.path.join(subdir, file)
                    print(f"Reading file: {file_path}")
                    image = self.imgToMatrix(file_path)
                    data_with_labels.append((label_counter, image.flatten()))
            label_counter += 1

        if not data_with_labels:
            print("No data found!")
        else:
            print(f"Found {len(data_with_labels)} images.")

        labels = np.array([item[0] for item in data_with_labels])
        data = np.array([item[1] for item in data_with_labels])
        # 保存标签和数据为.npy文件
        np.save(os.path.join(self.output_path, "labels.npy"), labels)
        np.save(os.path.join(self.output_path, "data.npy"), data)
        print("Data and labels saved to disk.")

    def split_data(self, data, labels, test_size=0.15, validation_split=0.1):
        X_train, X_test, Y_train, Y_test = train_test_split(
            data, labels, test_size=test_size, random_state=42
        )

        X_train, X_valid, Y_train, Y_valid = train_test_split(
            X_train,
            Y_train,
            test_size=validation_split / (1 - test_size),
            random_state=42,
        )

        return X_train, Y_train, X_valid, Y_valid, X_test, Y_test

    def get_data(self):
        data = np.load(os.path.join(self.output_path, "data.npy"))
        labels = np.load(os.path.join(self.output_path, "labels.npy"))

        X_train, Y_train, X_valid, Y_valid, X_test, Y_test = self.split_data(
            data, labels
        )

        img_size = int(np.sqrt(X_train.shape[1]))
        X_train = X_train.reshape((X_train.shape[0], img_size, img_size, 1))
        X_test = X_test.reshape((X_test.shape[0], img_size, img_size, 1))
        X_valid = X_valid.reshape((X_valid.shape[0], img_size, img_size, 1))

        # 将标签转换为one-hot编码
        Y_train = to_categorical(Y_train, self.classes_num)
        Y_test = to_categorical(Y_test, self.classes_num)
        Y_valid = to_categorical(Y_valid, self.classes_num)

        return {
            "X_train": X_train,
            "Y_train": Y_train,
            "X_valid": X_valid,
            "Y_valid": Y_valid,
            "X_test": X_test,
            "Y_test": Y_test,
        }
