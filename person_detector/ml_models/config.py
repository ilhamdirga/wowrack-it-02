import os

img_shape = (105,105,1)
batch_size = 32
epochs = 20

base_output = 'output'
model_path = os.path.sep.join([base_output, "siamese_model"])
plot_path = os.path.sep.join([base_output, "plot.png"])