from PIL import Image
import os, glob
import numpy as np
from sklearn import model_selection

##########################データセット要素定義#######################################
list_ = ['ramen', 'star']　　　　　　　　　　　　　　　
num = len(list_)
##########################VGG16のサイズに合わせた####################################
IMAGE_SIZE = 224 

X = []  #画像格納用
Y = []  #ラベル格納用

for label, name in enumerate(list_):
    dir = './data/' + name  #path指定                 
    files = glob.glob(photo_dir + '/*.jpg')
    for i, file in enumerate(files):
        img = Image.open(file)
        img = img.convert('RGB')
        img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
        data_set = np.asarray(img)
        print(data_set.shape)
        data_set = data_set.astype("float32")
        
        X.append(data_set)
        Y.append(index)

X = np.array(X)
Y = np.array(Y)

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)
xy = (X_train, X_test, y_train, y_test)
np.save('./image_files.npy', xy)