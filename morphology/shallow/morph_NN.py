# morph_NN.py
# Bennett Garza
# 3 November 2018
# An artificial neural network implemented to classify early and late galaxies

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.table import Table
from math import log10
from math import pi
import os
import glob
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import roc_curve, precision_recall_curve, auc
from sklearn.model_selection import train_test_split

def NN_test(feature_names, hidden_layers):
    # Get FITS data
    cat = "/home/ben/Documents/git/DeepLearn/morphology/Nair_Abraham_cat.fit"
    data = fits.getdata(cat,1)
    # Print FITS data
    #t = Table(data)
    #print(t.colnames)


    # Define features and classes
    nf = len(feature_names)
    features = []
    for i in range(nf):
        features.append(data[feature_names[i]])

    # Time type
    ttype = data["TType"]
    # Default class of each to -1 until defined
    c=ttype*0-1
    # Define class of each
    # Late galaxies
    c[np.where((ttype > 0) & (ttype <= 10))] = 1
    # Early galaxies
    c[np.where((ttype >= -5) & (ttype <= 0))] = 0
    # Other galaxies with ttype not between -5 and 10 will be filtered out

    # Filter out bad values, or filter in good values
    # Good values are:
    # c not -1 (c >= 0)
    p = np.where((c >= 0))

    # Class vector
    class_vector = c[p]

    # Feature vector
    
    feature_vector = np.zeros((class_vector.shape[0], nf))

    for i in range(nf):
        try:
            feature_vector[:, i] = features[i][p]
        except:
            print("Feature contains non-numerical data, training ended")
            # Removes feature from consideration by returning an AUC of -1
            return -1


    # Divide training set and test set
    X_train, X_test, y_train, y_test = train_test_split(feature_vector, class_vector, test_size=0.33, random_state=69)
    # print("Sizes training / test")
    # print(len(X_train), " / ", len(X_test))


    # Plot feature histograms and feature space
    """
    print("Early galaxies are red; late galaxies are blue")

    # n_r histogram
    plt.xlabel("$n_r$", fontsize=20)
    plt.ylabel("N", fontsize=20)
    plt.xlim(0, 6)
    plt.ylim(0, 1500)
    # Early galaxies are red
    plt.hist(feature_vector[class_vector==0, 1], histtype='step', color='red', linewidth=3)
    # Late galaxies are blue
    plt.hist(feature_vector[class_vector==1, 1], histtype='step', color='blue', linewidth=3)
    plt.show()

    # g-r histogram
    plt.xlabel("$g-r$", fontsize=20)
    plt.ylabel("N", fontsize=20)
    plt.xlim(0,1.5)
    plt.ylim(0, 4000)
    # Early galaxies are red
    plt.hist(feature_vector[class_vector==0, 0], histtype='step', color='red', linewidth=3)
    # Late galaxies are blue
    plt.hist(feature_vector[class_vector==1, 0], histtype='step', color='blue', linewidth=3)
    plt.show()

    #n_r -- g-r feature space
    plt.xlabel("$n_r$", fontsize=20)
    plt.ylabel("$g-r$", fontsize=20)
    plt.xlim(0, 6)
    plt.ylim(0, 1.5)
    # Early galaxies are red
    plt.scatter(feature_vector[class_vector==0, 1], feature_vector[class_vector==0, 0], color='red', s=1)
    # Late galaxies are blue
    plt.scatter(feature_vector[class_vector==1, 1], feature_vector[class_vector==1, 0], color='blue', s=1)
    plt.show()
    """

    # Train
    nn = MLPClassifier(hidden_layers, random_state=96)
    nn.fit(X_train, y_train)
    print("ANN Classifier Trained\nTraining set size: ", len(X_train), "\nNum features: ", nf)
    # print(nn)


    # Test
    y_pred = nn.predict_proba(X_test)
    fpr, tpr, thresholds = roc_curve(y_test, y_pred[:, 1])

    # Plotting ROC
    plt.xlabel("FPR", fontsize=20)
    plt.ylabel("TPR", fontsize=20)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.plot(fpr, tpr, linewidth=3, color='black')
    plt.show()

    # Calculate AUC
    AUC = auc(fpr, tpr)
    print("AUC:", AUC)
    return AUC


if __name__=="__main__":
    NN_test(['n_r', 'g-r'], (100, 100))
