import tensorflow as tf

 # Converting the model into Tensorflow serving
def Model_convertor(model_path, path): # sending model and the path to save
    
    model = tf.keras.models.load_model(model_path) # loading the model
    tf.saved_model.save(model, path) # saving the model as TensorFlow Serving


Model_convertor("./Models/Full_data_LSTM_app.h5", "./app_classifier/attack_model/1")