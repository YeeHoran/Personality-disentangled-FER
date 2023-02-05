#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 20:33:46 2023

@author: yi
"""
import cv2
import os
import os.path

import itertools as it
import csv

import shutil


def copyFramesFolder(framesFolderPath, verifyNum):
    if not (framesFolderPath in listFramesFolderNames):  #if the identity doe not exist in the list, then 1.insert its name into the list.
        listFramesFolderNames.append(framesFolderPath)   
        #framesFolderPath=f"{cc}/{framesFolder}" 
        #dd=os.path.abspath(os.path.curdir)        
        hierarchyPath=f"{'../../..'}/{'trainHierarchyDir'}"
        if not os.path.exists(hierarchyPath):
            trainHierarchyDir=os.makedirs(hierarchyPath)    #create a dir to save train's 3-level dirs to 1-level hierarchy dirs
        #test=os.path.abspath(path)
        framesFolderPath=framesFolderPath[2:]
        targetPath=f"{hierarchyPath}/{framesFolderPath}"    
        if not os.path.exists(targetPath):
            sourceFramesFolder=os.path.abspath(framesFolderPath) 
            testTarget=os.path.abspath(targetPath)
            shutil.copytree(framesFolderPath, targetPath)   #2.copy the identity's framesFolder and its extracted frame files to the hierarchy dir.                              
            #here exist problem,FileNotFoundError: [Errno 2] No such file or directory: '1eOvtoZCie8'
            
            os.chdir(r"./"+targetPath)
            #currentPath=os.path.curdir
            framesListCurrent = os.listdir()
            numFlag=0
            for frameName in framesListCurrent:   #3. save each frameName to listFramesNames.
                if numFlag<verifyNum:
                    #sourceFramePath=f"{framesFolderPath}/{frameName}"
                    #targetFramePath=f"{targetPath}/{frameName}"
                    #shutil.copyfile(sourceFramePath, targetFramePath)
                    framePathName=f"{framesFolderPath}/{frameName}"   #the saved framePathName is composed of framesFolderPath and frameName.
                    listFramesNames.append(framePathName)        #add an element to the end of the list 
                    numFlag+=1  
            return sourceFramesFolder  #return to the coming framesFolder path, for conveniently perform next iteration.
    else:
        print("repeat")        
        return framesFolderPath
            
    
    

#interface parameters,
#set the highest level Dir, say 'train'
dsDirLevel3='train-mini version for code test'
pathDirLevel3='./'+dsDirLevel3;    
#set the number of frames to be used for generating face verification pairs.
verifyNum=2
#change current working directory, 
flag_success=os.chdir(r"./"+dsDirLevel3)  #change to 3st level Dir, i.e. 'train'. must add 'r' before the path str.
aa=os.path.curdir   #obtain current working dir, such as './train'
listFramesFolderNames=list() #contain identity video's extracted frames' folder names(same as identity video names), used for further deleting repeated frameFolderNames(belong to the same identity/person which under different 2-order 'train' dirs).
                             #the extractFras program only delete repeated videos of the same person under 'train''s lowest order(1-order) dirs.
listFramesNames=list()       #contain frame names, used for generating frame pairs to verify the face images.
#change current working directory, although aa is still ./, and in fact it should be ./ since cwd will always be ./. it actually has changed to the directory specified by os.dir
#interface parameters.

#first, visit across the 4-level extracted facial images(each identity has the number of "toreadNum" image frames for computing), and add their name(video name+frame name) to the list containing all the frame names.
#second, enforce it.combinations() function on the list, and save all the resulted frame pairs to a csv file.
#first step, like ants moving, to move the tree structured framesFolders into a new hierarchy folder, and generate frameFileList for generating face verification pairs in the next step.
dirsLevel2=os.listdir(aa)   #list current dir's folders
#print(dirsLevel2)
# iterate through all the mp4 files under the 3 level folders
for dirLevel2 in dirsLevel2:       #change to level2 directory, such as './train/train1', './train/train2', etc.
    #change to Level2's directory
    if os.path.isdir(dirLevel2):       
        flag_success=os.chdir(r"./"+dirLevel2)
        #bb=os.path.abspath(os.path.curdir)   #obtain current working directory(absolute path)
        bb=os.path.curdir
        dirsLevel1=os.listdir(bb)
        #print(bb)       
        for dirLevel1 in dirsLevel1:
            flag_success=os.chdir(r"./"+dirLevel1)   #change to level1 directory, such as './train/train1/train80_01', './train/train1/train80_02', etc.
            #firstLevelAbsPath=os.path.abspath(os.path.curdir)  #reserve 1-level path for next step use, since the path changes across loop operation frequently. This could guarantee the memorization of the abs path in this step that'll be used at next step.   
            firstLevelRelatPath=os.path.curdir   #get the relative path of the current dir, for this step use.
            #cc=os.path.abspath(firstLevelRelatPath)
            framesFolderList=os.listdir(firstLevelRelatPath)
            for framesFolder in framesFolderList:  
                #cc=os.path.abspath(os.path.curdir)
                framesFolderPath=f"{firstLevelRelatPath}/{framesFolder}" 
                #call the 'geneFacePair' function, 
                framesFolderPath=copyFramesFolder(framesFolderPath, verifyNum)    #path is used to generate correct path in called function                               
                flag_success=os.chdir(framesFolderPath)    #change to the dir before calling the copyFramesFolder, to go on next iteration. This operation is to the following problem that in the calling function, the current working directory has changed.
                cwd=os.path.curdir
                flag_success=os.chdir(os.path.pardir)
                firstLevelRelatPath=os.path.curdir
            #while all the files in level1 are traversed, return to 1 level higher directory, i.e. level2 folder, such as 'train-2', and go to for for next level1 folder process.
            flag_success=os.chdir(os.path.pardir )    #obtain 1 level higher dir and changle dir to it, i.e.  Level2 dir, such as 'train-2', 'train-1', etc.                   
        #while all the level1 folders of one level2 folder have been traversed, it will return to 1 higher dir and change dir to it, i.e., Level3 dir, such as 'train'       
        flag_success=os.chdir(os.path.pardir)
#second step, generate face pairs list, and save the list to a csv file for face verification.
listFacePairs = it.combinations(listFramesNames, 2)  # size of combination is set to 2, since verify function works on two face images.
flag_success=os.chdir(os.path.pardir)

#second step, enforce it.combinations() function on the list, and save all the resulted frame pairs to a csv file.
with open('facePairs.csv', 'w+') as f:
    write = csv.writer(f)  # using csv.writer method from CSV package     
    #write.writerow(fields)
    write.writerows(listFacePairs)

    
        

        