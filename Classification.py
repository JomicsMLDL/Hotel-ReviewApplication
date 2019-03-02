# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 13:00:34 2018

@author: dell
"""

from sklearn.naive_bayes import MultinomialNB
import numpy as np
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from pandas import read_csv
from sklearn.model_selection import train_test_split

"Read Data from CSV file using Pandas"
dataframe = read_csv('Singapore_review.csv', usecols=[ 1, 2,3], engine='python', skipfooter=3) 
dataset = np.array(dataframe.values)

"In first column in csv file is Review,next Ratings,next Sentiment"
reveiew_data=list(dataset[:,0])
rev_score=(dataset[:,1:3]).astype('float32')

"Feature Extraction"
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(reveiew_data)

trainX=vectors.toarray()   #review features
trainY=rev_score[:,1]  #sentiment

# classify using SVM
from sklearn.svm import SVC

XX_train, XX_val, yy_train, yy_val = train_test_split(trainX, trainY, test_size=0.33, random_state=42)

for c in [0.01,0.05,0.1,0.15,0.2,0.5,1]:
    svm = SVC(C=c,kernel='linear')
    svm.fit(XX_train,yy_train)
    print ("Accuracy for C in SVM = %s: %s" % (c, metrics.accuracy_score(yy_val, svm.predict(XX_val))))



## classsify Using Naive Bayes
for c in [0.01,0.05,0.1,0.15,0.2,0.5,1]:    
    clf = MultinomialNB(alpha=c)
    clf.fit(XX_train,yy_train)
    pred = clf.predict(XX_val)

    print('Accuracy for C in NaiveBayes= %f' % metrics.accuracy_score(yy_val, pred))
