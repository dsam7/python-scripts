import numpy as np
import os
from PIL import Image
from sklearn.decomposition import RandomizedPCA
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import pylab as pl

#size for all images to be resized to
IMG_SIZE = (607,606)

print "Running ..."

def img_to_array(filename):
    #converts image to numpy array
    img = Image.open(filename)
    img = img.resize(IMG_SIZE)
    img = list(img.getdata())
    img = map(list, img)
    img = np.array(img)
    return img


def flatten(img):
    #takes a (m, n) numpy array and flattens it into an array of shape (1, m * n)
    s = img.shape[0] * img.shape[1]
    img_wide = img.reshape(1, s)
    return img_wide[0]

#specify directory here and differentiate files through labels 
#labels - used to create the plot and the "correct answers" to judge the predictions on
img_dir = "ElecImagesTest/"
images = [img_dir + f for f in os.listdir(img_dir)]
labels = ["Elec" if "Elec" in f.split('/')[-1] else "Pi0" for f in images]

data = []
#with a lot of data, this takes a long time
for image in images:
    img = img_to_array(image)
    img = flatten(img)
    data.append(img)

data = np.array(data)

is_train = np.random.uniform(0, 1, len(data)) <= .9 #number determines what fraction of the files to use from the dir (can't do 1 or higher)
y = np.where(np.array(labels)=="Elec", 1, 0)

train_x, train_y = data[is_train], y[is_train]
test_x, test_y = data[is_train==False], y[is_train==False]

pca = RandomizedPCA(n_components=3)
train_x = pca.fit_transform(train_x)
test_x = pca.transform(test_x)
X = pca.fit_transform(data)

print "A window has opened up with the graph"
print "Exit out of it to see the prediction accuracy"

#creates plot of all Elec and Pi0 array values
df = pd.DataFrame({"x": X[:, 0], "y": X[:, 1], "label":np.where(y==1, "Elec", "Pi0")})
colors = ["red", "yellow"]
for label, color in zip(df['label'].unique(), colors):
    mask = df['label']==label
    pl.scatter(df[mask]['x'], df[mask]['y'], c=color, label=label)
pl.legend()
pl.show()

#creates the model
knn = KNeighborsClassifier()
knn.fit(train_x, train_y)

#accuracy test
z = knn.predict(X)
accuracy = knn.score(train_x, train_y)
print "Prediction Accuracy: " + str(accuracy)

preds = knn.predict(train_x)
preds = np.where(preds==1, "Elec", "Pi0")

#prints the incorrect predictions
counter = 0
for counter in range(len(train_y)):
    if train_y[counter] == 0 and preds[counter] == 'Pi0':
        pass
    elif train_y[counter] == 1 and preds[counter] == 'Elec':
        pass
    else:
        print 'Incorrect: ' + images[counter]
