"""
    This file is unrelated and just used for debugging of the models.
    To make sure everything is going smothly, like the architecture and
    the weights.

"""










# import tensorflow as tf
# import os
# from pathlib import Path

# # paths
# keras_path = "./main_Models/Final-binary.keras"   # your keras-format model
# export_path = "./exported_model/binary_classifier/1"

# # load
# model = tf.keras.models.load_model(keras_path)
# print("Model input shape:", model.input_shape)   # should print (None, 77, 1)
# print("Model output shape:", model.output_shape)

# # build serving fn with exact 3-D input signature
# @tf.function(input_signature=[tf.TensorSpec([None, 77, 1], tf.float32, name="input")])
# def serving_fn(x):
#     # ensure float32 and proper shape inside function
#     x = tf.cast(x, tf.float32)
#     # model(x) returns a tensor; put it under predictable key "outputs"
#     return {"outputs": model(x)}

# # remove old export if exists, create directories, then save
# Path(export_path).parent.mkdir(parents=True, exist_ok=True)  # ensure parent folder exists
# if Path(export_path).exists():
#     import shutil
#     shutil.rmtree(export_path)

# tf.saved_model.save(model, export_path, signatures={"serving_default": serving_fn})
# print(f"SavedModel exported to: {export_path}")





# Testing, to make sure the model is working
# import tensorflow as tf
# loaded = tf.saved_model.load("./exported_model/binary_classifier/1")
# print(list(loaded.signatures.keys()))   # should include 'serving_default'




"""
    Modifing the json file
"""


# import json

# # single dummy instance: 77 timesteps each with 1 feature
# instance = [[0.0] for _ in range(77)]   # shape (77,1)
# request = {"instances": [instance]}     # batch size 1

# with open("request.json", "w") as f:
#     json.dump(request, f)
# print("wrote request.json (contains 1 instance of shape 77x1)")

    
    
    
"""
    Using python request for checking the model
"""
    
import requests, json

url = "http://localhost:8501/v1/models/binary_classifier:predict"
with open("request.json") as f:
    data = json.load(f)
r = requests.post(url, json=data)
print(r.status_code, r.text)





# # export_from_keras.py
# import tensorflow as tf
# from pathlib import Path
# import shutil

# keras_path = r"./main_Models/Final-binary.keras"            # <- update
# export_dir = r"./binary_classifier/1"  # <- update

# # load Keras model (full model with weights)
# model = tf.keras.models.load_model(keras_path)
# print("Keras model input_shape:", model.input_shape)
# print("Keras model output_shape:", model.output_shape)

# # remove previous export if exists
# p = Path(export_dir)
# if p.exists():
#     shutil.rmtree(p)


# input_shape = model.input_shape[1:]   # e.g. (77, 1)
# spec = tf.TensorSpec([None, *input_shape], tf.float32, name="input")
# @tf.function(input_signature=[spec])
# def serving_fn(x):
#     x = tf.cast(x, tf.float32)    # ensure tf.float32
#     preds = model(x)
#     # return dict — key becomes the output tensor name in signature
#     return {"outputs": preds}
# # Save full model in TF SavedModel format (includes weights + signatures)
# tf.saved_model.save(model, str(export_dir), signatures={"serving_default": serving_fn})
# print(f"SavedModel written to: {export_dir}")

# # quick check of saved variables (optional)
# loaded = tf.saved_model.load(export_dir)

# print("Signatures:", list(loaded.signatures.keys()))
# print("SavedModel variables count:", len(loaded.variables))
# print variable names if you want to inspect
# for v in loaded.variables[:10]:
#     print(v.name, v.shape)





"""
    Checking whather the weights and architecture of the model is working properly
"""

# import tensorflow as tf

# model = tf.keras.models.load_model("./main_Models/Final-binary.h5")

# layer = model.layers[0]
# weights = layer.get_weights()


# if weights:
#     for i, w in enumerate(weights):
#         print(f"  Component {i} shape: {w.shape}")
#         print(f"  First 5 values of component {i}: {w.flatten()[:5]}")
# else:
#     print("  This layer has no weights.")

# # 3. Iterate through all layers to get weights and configuration
# print("\nInspecting all layers and their configurations...")
# for layer in model.layers:
#     print(f"\n--- Layer Name: {layer.name}")
#     print(f"  Config: {layer.get_config()}")
    
#     layer_weights = layer.get_weights()
#     if layer_weights:
#         print(f"  Number of weight components: {len(layer_weights)}")
#         for i, w in enumerate(layer_weights):
#             print(f"  Weight component {i} shape: {w.shape}")







"""
    Exporting the model into TensorFlow Serving    
"""
import tensorflow as tf
from pathlib import Path
import shutil

EXPORT_BASE = Path("./final_bin")
EXPORT_PATH = EXPORT_BASE / "1"

# Clean old export
if EXPORT_PATH.exists():
    shutil.rmtree(EXPORT_PATH)

# Load your Keras model
model = tf.keras.models.load_model("./main_models/Final-binary.h5")

# Build a serving function
@tf.function(input_signature=[tf.TensorSpec([None, 77, 1], tf.float32, name="input")])
def serving_fn(x):
    return {"outputs": model(x)}

# Export to SavedModel format
tf.saved_model.save(model, str(EXPORT_PATH), signatures={"serving_default": serving_fn})

print("✅ Exported SavedModel at:", EXPORT_PATH)



   
   