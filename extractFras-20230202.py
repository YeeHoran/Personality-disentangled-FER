#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 12:44:30 2023

@author: yi
"""
'''
The program is to extract multiple face frames for each identity, since the train dataset is a three-level tree structure, the iterative is structured by 3-level loops in which top 'train' folder is level-3, its lower levels of train-1 to train-6 are level-2, and finally all the folders under these train-1 to train-6 are level-1 folders.
The interface paras such as the nubmer of extracted frames for each video are set firstly, then the for loop start to run across the tree structure to visit each video to extract image frames. The extracted image frames for each video are saved into a folder with the same name and path as the video itself.
The keypoint to keep in mind is that it has to set working dir iteratively by cmd 'os.chdir(r"./"+dsDirLevel3)' since it visit the 3-level tree iteratively.
The train folder has totally 6000 interview videos from youtube. Nearly one video corresponds to one single person/identity, but with very few exceptions that more than one videos(e.g. 2 videos) correspond to one single identity. In that condition, only the first visited video from the multiples is used to extract multiple frames for the person/identity. The method to judge whether multiple videos refer to one person is that their main file names are the same just with different post-fix numbers to discriminate them.
'''
import cv2
import os
import os.path

def extractFrames(filepath, toreadNum):
    video=cv2.VideoCapture(filepath)
    #see how many frames are in the video
    totalFrames= int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(totalFrames)

    #compute how many intervals to read out a frame
    readInterval=int(totalFrames/toreadNum)
    print(readInterval)

    try:
        #firstly, extract the file name of the mp4 video, and make it as the name of the folder to contain specified frames.
        name = filename.split('.')
        filepath = name[0].split('/')
        fileDirPath=f"{'.'}/{filepath[-1]}"      #must add 'f' to generate path.aa is current
                
        if not os.path.exists(fileDirPath):  #if exist mp4 files coming from the same identity, their main file names are same, and highlight the filename difference by tail numbers. but since they are from the same person/identity, no more dir should be created.
            os.makedirs(fileDirPath)
        #if not create, pop up error
    except OSError:
        print('Error: Creating directory of'+fileDirPath)
    
    #frame
    currentFrame=0
    readoutNum=0

    while(readoutNum<toreadNum): #when the number of readout frames is less than the toreadNum that is specified by 'toreadNum',
                             #continue to read
        video.set(1, currentFrame)    #set the specified frame no. to be read out
        #extract image frames from video
        ret, frame=video.read()       #read out the frame pointed by the above cmd
    
        if ret:
            #if video still exist, continue to create images
            name=fileDirPath+'/frame'+str(currentFrame)+'.jpg'
            print('Creating...'+name)
            #output extracted images to jpg files
            cv2.imwrite(name, frame)
            #extract frames in every readInterval, to guanrantee extract specified number of frames.
            currentFrame+=readInterval
            readoutNum+=1  # the number of readout frames is added by 1.
        else:
            break

    #release all space and windows when complete
    video.release()
    cv2.destroyAllWindows()



#interface parameters,
#set the highest level Dir, say 'train'
dsDirLevel3='train-mini version for code test'
pathDirLevel3='./'+dsDirLevel3;    
#set the number of frames to be extracted for the video
toreadNum=8
#change current working directory, 
flag_success=os.chdir(r"./"+dsDirLevel3)  #change to 3st level Dir, i.e. 'train'. must add 'r' before the path str.
aa=os.path.curdir   #obtain current working dir, such as './train'
#change current working directory, although aa is still ./, and in fact it should be ./ since cwd will always be ./. it actually has changed to the directory specified by os.dir
#interface parameters.

dirsLevel2=os.listdir(aa)   #list current dir's folders
print(dirsLevel2)
# iterate through all the mp4 files under the 3 level folders
for dirLevel2 in dirsLevel2:       #change to level2 directory, such as './train/train1', './train/train2', etc.
    #change to Level2's directory
    flag_success=os.chdir(r"./"+dirLevel2)
    bb=os.path.curdir   #obtain current working directory
    dirsLevel1=os.listdir(bb)
    print(bb)
    for dirLevel1 in dirsLevel1:
        flag_success=os.chdir(r"./"+dirLevel1)   #change to level1 directory, such as './train/train1/train80_01', './train/train1/train80_02', etc.
        cc=os.path.curdir                        #get current path
        fileList=os.listdir(cc)
        for filename in fileList:  
            # Check whether file is in mp4 format or not
            if filename.endswith(".mp4"):
                #从指定路径读取视频
                file_path = f"{cc}/{filename}"      #must add 'f' to generate path.aa is current
                #call the 'extractFrames' function, extract specified number of frames for all the mp4 files in a folder,
                extractFrames(file_path, toreadNum)    #path is used to generate correct path in called function
        #while all the files in level1 are traversed, return to 1 level higher directory, i.e. level2 folder, such as 'train-2', and go to for for next level1 folder process.
        flag_success=os.chdir(os.path.pardir )    #obtain 1 level higher dir and changle dir to it, i.e.  Level2 dir, such as 'train-2', 'train-1', etc.   
    #while all the level1 folders of one level2 folder have been traversed, it will return to 1 higher dir and change dir to it, i.e., Level3 dir, such as 'train'       
    flag_success=os.chdir(os.path.pardir)
    
        
