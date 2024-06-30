import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
import numpy as np
from process_image import cat_face_recognize

app = Flask(__name__)

# 模型文件路径
model_path = "train/my_cnn_model.h5"
model = load_model(model_path)
class_labels = ["饼干", "斑马", "手套", "电饭煲", "爪子", "馒头"]

# 上传文件夹
UPLOAD_FOLDER = "uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def predict_image(img_array):
    if img_array is None:
        raise ValueError("Received None as input to predict_image function")
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_index]
    return predicted_class_index, confidence


@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "未收到图像文件，请重新上传文件！"}), 400
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "选择图像失败，请重新上传文件！"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        try:
            processed_img_array = cat_face_recognize(file_path)
            if processed_img_array is None:
                return jsonify({"error": "没有寻找到猫脸"}), 400
            # 使用模型进行预测
            prediction_index, confidence = predict_image(processed_img_array)
            predicted_label = class_labels[prediction_index]
            os.remove(file_path)
            return (
                jsonify(
                    {
                        "predicted_class": predicted_label,
                        "confidence": float(confidence),
                    }
                ),
                200,
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
