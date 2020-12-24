import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import time
#import pickle

#initalize and load tf runtime with tflite iterpreter

Interpreter = tf.lite.Interpreter(model_path = 'tflite_model.tflite')
Interpreter.allocate_tensors()

output_details = Interpreter.get_output_details()
input_details = Interpreter.get_input_details()
input_shape = input_details[0]['shape']

#set input and output scalers
X = np.loadtxt('X.csv',delimiter = ',')
Y = np.loadtxt('Y.csv',delimiter = ',')
#print(Y[0])
input_scaler = MinMaxScaler()
output_scaler = MinMaxScaler()

input_scaler.fit_transform(X)
output_scaler.fit_transform(Y)


def predict_tflite(input_data):
  input_data = np.array(input_data,dtype = np.float32)
  Interpreter.set_tensor(input_details[0]['index'],input_data)
  Interpreter.invoke()
  output_data = Interpreter.get_tensor(output_details[0]['index'])
  return output_data
  
test_input = np.zeros([1,X.shape[1]])
test_input[:] = 1

st = time.time()
tflite_predicted =  output_scaler.inverse_transform(predict_tflite(input_scaler.fit_transform(test_input)))
print('Inference time:',time.time()-st,'inference:',tflite_predicted)

