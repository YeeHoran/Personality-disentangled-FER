#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 19:08:05 2023
4 persons, 20 frames for each of them. P/N=1/3, increase the value of P/N to promote the F1 result.
by up the number of frames for each one, and down the number of persons.
totally about 3k pairs, with about 900 of the pairs are from a same person.

@author: yi
"""
'''
The program is to test the models' performance for face varification so as to find the best model to be used for face representation in the following tasks.
first step, read out facepair file into a list,
second step, call the verify API function that using the specified model to verify whether the two face images are from one single identity/person. Yes:True, No: False.
Third step, see the root dir of the two face image files to check whether they are the same. Yes: Really from one same person, No: Really not from on same person.
Fourth step, add or substract the TN, TP, FN, FP values by the results from the above two steps.(TN: Detect 0, Real 0) (TP: Detect 1, Real 1) (FN: Detect 0, Real 1) (FP: Detect 1, Real 0)
Fifth step, compute recall, precision, and F1. Recall=tp/(tp+fn), Precision=tp/(tp+fp), 
models: face recognition framework wrapping state-of-the-art models: VGG-Face, Google FaceNet, OpenFace, Facebook DeepFace, DeepID, ArcFace, Dlib and SFace.
'''
import tensorflow
#a=tensorflow.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None)
from deepface import DeepFace
import cv2
import os
import os.path
import datetime
import csv
#from pycm import *

#interface paras.
modelName='OpenFace'
#interface paras.

datasetFolder="4identity20frames"
#interface paras.

#initialization
y_real=list()   #y_real contain the actual values about whether the face pair images are from the same person/identity
y_pred=list()   #y_pred contain the computed(verify API function) values on whether the face pair images are of same person.
TP = 0
FP = 0
TN = 0
FN = 0



with open('facePairs4*20', 'r') as file:  #open facePairs txt file and read out the data to a list
    # Read the contents of the file
    contents = file.read()
    # Split the contents of the file into a list
    facePairList = contents.split()

    os.chdir(r"./"+datasetFolder)   #change current working dir to the dataset folder.
    #aa=os.path.abspath(os.path.curdir)   #see whether change dir successfully.

ii=0
beginTime=datetime.datetime.now()
for facePair in facePairList:
    faceImages=facePair.split(',')
    img1_path=faceImages[0]
    img2_path=faceImages[1]
    
    #1. extract the parents' name of the two face images, and check whether they are the same one, all pairs' results are saved to a list.
    img1String=img1_path.split('/')
    img1Parent=img1String[0]
    img2String=img2_path.split('/')
    img2Parent=img2String[0]
    realVerify=(img1Parent==img2Parent)  #test whether the two face images are from56 a same identity.
    
    y_real.append(realVerify)
    #2. use DeepFace API function 'verify' to use models to compute whether the two face image are from a same person.
    cwd=os.path.curdir
    img1_path=f"{cwd}/{img1_path}"
    img2_path=f"{cwd}/{img2_path}"
    faceVerify = DeepFace.verify(img1_path, img2_path, model_name=modelName)   #when the distance>threshold,then the result is false, i.e., not the same person/identity, all pairs' results are saved to a list.
    y_pred.append(faceVerify.get("verified"))
    ii=ii+1
    print(ii)

endTime=datetime.datetime.now()

for i in range(len(y_pred)): 
    if y_real[i]==y_pred[i]==1:
       TP=TP+1
    if y_pred[i]==1 and y_real[i]!=y_pred[i]:
       FP += 1
    if y_real[i]==y_pred[i]==0:
       TN += 1
    if y_pred[i]==0 and y_real[i]!=y_pred[i]:
       FN += 1
    
#call perf_measure function to compute TN, TP, FN, FP values
#perf_measure(y_real, y_pred)
recall=TP/(TP+FN)
precision=TP/(TP+FP)
F1=2*recall*precision/(recall+precision)
Accuracy=(TP+TN)/(TP+FP+TN+FN)
#TP, FP, FN, TN=confusion_matrix(y_real, y_pred)
timeUsed=endTime-beginTime

#save results to a file named 'faceVerifyResult'.

faceVerifyRes=list()
faceVerifyRes.append("TP: "+str(TP)+", TN: "+str(TN)+", FP: "+str(FP)+", FN: "+str(FN)+"\n")
faceVerifyRes.append("recall: "+str(recall)+", precision: "+str(precision)+", F1: "+str(F1)+", Accuracy: "+str(Accuracy))
faceVerifyRes.append("Time Used:{}".format(timeUsed))

#delete the commas in the list 
newFaceVerifyRes=[str.replace(",","") for str in faceVerifyRes]
print(newFaceVerifyRes)
listToStr = ' '.join([str(elem) for elem in newFaceVerifyRes])
 
print(listToStr)
with open('faceVerifyResult', 'w') as f:
    f.write(listToStr)