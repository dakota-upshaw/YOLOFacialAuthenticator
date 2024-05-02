from ultralytics import YOLO


model = YOLO('C:/Users/Master/Desktop/378FacialRecog/runs/detect/CHECKPOINT2/weights/best.pt')

def main():
    model.train(data='C:/Users/Master/Desktop/378FacialRecog/Dakota_Upshaw_FacialRecog/DatasetFINAL/SplitData/data.yaml', epochs=300)  #change to a higher number of epochs for more accuracy, 300?

if __name__ == '__main__':
    main()

#changes to data.yaml file on local PC
#1. need absolute path of data.yaml (C:/....)
#2. remove the .. from train/images etc etc in yaml file (unless you setup environmental variables but we cant do that on linux LOLOL)

#copy the best weights, use in yoloTest 