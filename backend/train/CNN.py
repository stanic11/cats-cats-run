import numpy as np
from myDataLoader import DataLoader
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Activation,
    Dense,
    Dropout,
    Flatten,
)
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adadelta


class CNN:
    def __init__(
            self,
            data_loader,
            batch_size=30,
            classes_num=6,
            epoch_num=50,
            filters_num=32,
            pool_num=2,
            conv_num=3,
    ):
        self.data_loader = data_loader
        self.batch_size = batch_size
        self.classes_num = classes_num
        self.epoch_num = epoch_num
        self.filters_num = filters_num
        self.pool_num = pool_num
        self.conv_num = conv_num

    def generate_model(self):
        data = self.data_loader.get_data()
        X_train = data.get("X_train")
        Y_train = data.get("Y_train")
        X_valid = data.get("X_valid")
        Y_valid = data.get("Y_valid")

        model = Sequential()
        model.add(
            Conv2D(
                self.filters_num,
                (self.conv_num, self.conv_num),
                padding="same",
                activation="relu",
                input_shape=(64, 64, 1),
            )
        )
        model.add(Conv2D(self.filters_num, (self.conv_num, self.conv_num)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(self.pool_num, self.pool_num)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128))
        model.add(Activation("relu"))
        model.add(Dropout(0.5))
        model.add(Dense(self.classes_num))
        model.add(Activation("softmax"))

        model.compile(
            loss="categorical_crossentropy", optimizer=Adadelta(), metrics=["accuracy"]
        )

        model.fit(
            X_train,
            Y_train,
            batch_size=self.batch_size,
            epochs=self.epoch_num,
            verbose=1,
            validation_data=(X_valid, Y_valid),
        )

        # 保存模型
        model_path = "my_cnn_model.h5"
        model.save(model_path)
        print(f"Model saved to {model_path}")
        return model

    def cal_score(self):
        model = self.generate_model()
        data = self.data_loader.get_data()
        X_test = data.get("X_test")
        Y_test = data.get("Y_test")
        score = model.evaluate(X_test, Y_test, verbose=0)
        print("Test score:", score[0])
        print("Test accuracy:", score[1])

    def predict(self):
        model = self.generate_model()
        X_test = self.data_loader.get_data().get("X_test")
        predictions = model.predict(X_test)
        rounded = [np.around(x) for x in predictions]
        print(rounded)
        print(predictions)
