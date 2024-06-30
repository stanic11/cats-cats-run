import image_process
import myDataLoader
from CNN import CNN

if __name__ == "__main__":
    image_processor = image_process.ImageProcessor()
    if not image_processor.has_images():
        image_processor.process()
        print("Image processing finished.")
    data_loader = myDataLoader.DataLoader()
    data_loader.save_images_with_labels()
    data = data_loader.get_data()
    cnn = CNN(
        data_loader,
        batch_size=30,
        classes_num=6,
        epoch_num=50,
        filters_num=32,
        pool_num=2,
        conv_num=3,
    )
    model = cnn.generate_model()
    cnn.cal_score()
    cnn.predict()
