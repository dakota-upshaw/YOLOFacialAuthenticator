import os
import random
import shutil
from itertools import islice


outputFolderPath = "Dataset/SplitData"
inputFolderPath = "Dataset/all"
splitRatio = {"train" :0.7, "val" :0.2, "test" :0.1}
classes = ["fake", "real"]

# create folder, if already exists then delete and create
try:
    shutil.rmtree(outputFolderPath)
    print("Removed Directory")
except OSError as e:
    os.mkdir(outputFolderPath)

# ------------- Directories to create --------- #
os.makedirs(f"{outputFolderPath}/train/images", exist_ok = True) #use instead of mkdir bc mkdir only makes if parent dir is available
os.makedirs(f"{outputFolderPath}/train/labels", exist_ok = True)
os.makedirs(f"{outputFolderPath}/val/images", exist_ok = True)
os.makedirs(f"{outputFolderPath}/val/labels", exist_ok = True)
os.makedirs(f"{outputFolderPath}/test/images", exist_ok = True)
os.makedirs(f"{outputFolderPath}/test/labels", exist_ok = True)

# --------------- Get Names  --------------
listNames = os.listdir(inputFolderPath)

uniqueNames = [] # for only returning the 20 images
for name in listNames:
    uniqueNames.append(name.split('.')[0])
uniqueNames = list(set(uniqueNames)) # remove duplicates

# ---------------- Shuffle ----------
random.shuffle(uniqueNames)

# ------------ Find number of imgs for each folder
lenData = len(uniqueNames)
lenTrain = int(lenData * splitRatio['train'])
lenVal = int(lenData * splitRatio['val'])
lenTest = int(lenData * splitRatio['test'])

# ------------ Put remaining images in training ---------
if lenData != lenTrain + lenTest + lenVal:
    remaining = lenData-(lenTrain + lenTest + lenVal)
    lenTrain += remaining
print(f'Total Images: {lenData} \nSplit: {lenTrain} {lenVal} {lenTest}')

# -----------  Split the list ----------------
# plit uniqueNames into 3 different lists
lengthToSplit = [lenTrain, lenVal, lenTest]
Input = iter(uniqueNames)
Output = [list(islice(Input, ele)) for ele in lengthToSplit]
print(f'Total Images: {lenData} \nSplit: {len(Output[0])} {len(Output[1])} {len(Output[2])}')

#-----------Copy the Files ------------
sequence = ['train', 'val', 'test'] #allow to change filename w value
for i, out in enumerate(Output):
    for filename in out:
        shutil.copy(f'{inputFolderPath}/{filename}.jpg', f'{outputFolderPath}/{sequence[i]}/images/{filename}.jpg')
        shutil.copy(f'{inputFolderPath}/{filename}.txt', f'{outputFolderPath}/{sequence[i]}/labels/{filename}.txt')

print("Splitting Complete")

#----------- Creating Data.yaml file
dataYaml = f'path: \n\
train: train/images\n\
val: val/images\n\
test: test/images\n\
\n\
nc : {len(classes)}\n\
names: {classes}'

f = open(f"{outputFolderPath}/data.yaml", 'a') #f for file. a is the flag for append. if file isn't present then create it. If present then add the data to it
f.write(dataYaml)
f.close()

print("Data.yaml file created")