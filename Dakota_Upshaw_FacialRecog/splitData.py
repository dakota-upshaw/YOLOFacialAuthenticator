import os
import random
import shutil
from itertools import islice

outputDir = 'Dataset/SplitData'
inputDir = "Dataset/all"
ratio = {"train":0.7, "val":0.2, "test":0.1}
classes = ["fake", "real"]

try:
    shutil.rmtree(outputDir)
    print("Directory Removed")
except OSError as e:
    os.mkdir(outputDir)
    
os.makedirs(f"{outputDir}/train/images",exist_ok=True)
os.makedirs(f"{outputDir}/train/labels",exist_ok=True)
os.makedirs(f"{outputDir}/validate/images",exist_ok=True)
os.makedirs(f"{outputDir}/validate/labels",exist_ok=True)
os.makedirs(f"{outputDir}/test/images",exist_ok=True)
os.makedirs(f"{outputDir}/test/labels",exist_ok=True)

###-----get names
listNames = os.listdir(inputDir)
#print(len(listNames))
#print(listNames)
uniqueNames = []
for name in listNames:
    uniqueNames.append(name.split('.')[0]) # get the first half of 1984092886095480.jpg
uniqueNames = list(set(uniqueNames))
#print(len(uniqueNames))
#print(uniqueNames)
    
###------shuffle dirs
random.shuffle(uniqueNames)

###------find images for each folder
lenData = len(uniqueNames)
#print(f'Total Data: {lenData}')
lenTrain = lenData * ratio['train']
lenVal = lenData * ratio['val']
lenTest = lenData * ratio['test']
#print(f'Total Data: {lenData}\n Split: {lenTrain} , {lenVal} , {lenTest}')

##-----accounting for remaining imgs and put them in training
if lenData != (lenTrain + lenVal + lenTrain):
    mod = lenData - (lenTrain + lenVal + lenTrain)
    lenTrain += mod
#print(f'Total Data: {lenData}\n Split: {lenTrain} , {lenVal} , {lenTest}')


###-------split list
lSplit = [lenTrain, lenVal, lenTest]
Input = iter(uniqueNames)
Out = [list(islice(Input,ele))for ele in lSplit]
#print(len(Out))
#print(f'Total Data: {lenData}\n Split: {len(Out[0])} , {len(Out[1])} , {len(Out[2])}')

###--------copy files
splitDir = ratio = ["train", "val", "test"]
for i,o in enumerate(Out):
    for filename in o:      
        shutil.copy(f'{inputDir}/{filename}.jpg', f'{outputDir}/{splitDir[i]}/images/{filename}.jpg') #for jpg
        shutil.copy(f'{inputDir}/{filename}.txt', f'{outputDir}/{splitDir[i]}/labels/{filename}.txt') #for jpg

print("Split complete \n")
        
yamlData = f'path: ../Data\n\
train: ../train/images\n\
val: ../val/images\n\
test: ../test/images\n\
\n\
nc: {len(classes)}\n\
names: {classes}' # need to put the absolute path of the split data folders here later
f = open(f"{outputDir}/data.yaml", 'a')
f.write(yamlData)
f.close

print("Data.yaml initialized \n")
#GOAL: about 7000 imgs, 3500 real 3500 fake