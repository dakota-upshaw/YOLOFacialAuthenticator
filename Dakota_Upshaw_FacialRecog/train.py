from ultralytics import YOLO

model = YOLO('yolov8n.pt')

def main():
    model.train(data='Dataset/SplitData/data.yaml', epochs=3) #change to a higher number of epochs for more accuracy, 300?

if __name__ == '__main__':
    main()

#changes to data.yaml file on local PC
#1. need absolute path of data.yaml (C:/....)
#2. remove the .. from train/images etc etc in yaml file (unless you setup environmental variables but we cant do that on linux LOLOL)

#copy the best weights, in yoloTest 