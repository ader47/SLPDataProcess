import sys
import cv2
import os
import pandas as pd
from sys import platform
import argparse
import time
import numpy as np
try:
    # Import Openpose (Windows/Ubuntu/OSX)
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    #dir_path = 'D:\\Graduate\\Code\\Sign Language Production\\openpose\\build\\examples\\tutorial_api_python'
    dir_path = '/home/share/liufeng/openpose/build/examples/tutorial_api_python'
    print(dir_path)
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../build/python/openpose/Debug');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../build/x64/Debug;' +  dir_path + '/../../bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('/home/share/liufeng/openpose/build/python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e
except Exception as e:
    #在这里打开文件，读取，可否多线程？
    print(e)
    sys.exit(-1)


#DATASET_PATH='D:\\dataset\\PHOENIX-2014-T-release-v3\\PHOENIX-2014-T'
#IMAGE_PATH='D:\\dataset\\PHOENIX-2014-T-release-v3\\PHOENIX-2014-T\\features\\fullFrame-210x260px'
DATASET_PATH='/home/share/liufeng/dataset/PHOENIX-2014-T-release-v3/PHOENIX-2014-T'
IMAGE_PATH='/home/share/liufeng/dataset/PHOENIX-2014-T-release-v3/PHOENIX-2014-T/features/fullFrame-210x260px'
METHOD='train'
def read_file(PATH):
    #spilt  |
    file=pd.read_csv(PATH,sep='|',header=0)
    # 对数据进行排序
    file=file.sort_values(by='name')
    file=file.reset_index(drop=True)
    # 似乎存在无用数据
    del file['start']
    del file['end']
    # 这里视频和名称相同，使用key索引即可
    del file['video']
    return file

def Process(args):
    # Flags
    params = dict()
    #params["model_folder"] = "D:/Graduate/Code/Sign Language Production/openpose/models"
    params["hand"] = True
    params["model_folder"] = "/home/share/liufeng/openpose/models"
    # 多gpu
    # params["num_gpu"] = int(vars(args[0])["num_gpu"])
    # numberGPUs = int(params["num_gpu"])
    # print('GPUs:',numberGPUs)
    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item
    print(params)
    try:
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()
        return opWrapper

    except ImportError as e:
        print('improt failed')


if __name__=='__main__':

    start = time.time()
    annotations=os.path.join(DATASET_PATH,'annotations','manual')
    file=os.path.join(annotations,'PHOENIX-2014-T.train.corpus.csv')
    train=read_file(file)
    dataset={}

    for i in range(0,len(train)):
        dataset[train['name'][i]]={train.columns[j]:train[train.columns[j]][i] for j in range(1,len(train.columns))}

    #print(dataset['01April_2010_Thursday_heute-6696'])
    #开始
    parser = argparse.ArgumentParser()
    args = parser.parse_known_args()

    # Flags
    params = dict()
    #params["model_folder"] = "D:/Graduate/Code/Sign Language Production/openpose/models"
    params["hand"] = True
    params["face"]=True
    params["model_folder"] = "/home/share/liufeng/openpose/models"
    # 多gpu
    # params["num_gpu"] = int(vars(args[0])["num_gpu"])
    # numberGPUs = int(params["num_gpu"])
    # print('GPUs:',numberGPUs)
    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()
    # open file
    #filetxt=open('./data/filename.file','w+',encoding='utf-8')
    #gloss_file=open('./data/train.gloss','w+',encoding='utf-8')
    #todo
    # 这里好像没有句号
    #text_file=open('./data/train.text','w+',encoding='utf-8')
    # skels_file=open('./data/train.skels','w+',encoding='utf-8')
    couter=0
    for name,values in dataset.items():
        couter+=1
        print(couter/len(dataset)*100,'%')
        if not os.path.exists("/home/share/liufeng/openpose_json/"):
            os.mkdir("/home/share/liufeng/openpose_json/")
        if not os.path.exists("/home/share/liufeng/openpose_json/"+METHOD):
            os.mkdir("/home/share/liufeng/openpose_json/"+METHOD)
        params["write_json"] = "/home/share/liufeng/openpose_json/" + METHOD +'/'+ name
        opWrapper.configure(params)
        opWrapper.start()
        # 在循环开始之前写入 文件名  gloss text
        if os.path.exists(os.path.join(IMAGE_PATH, METHOD, name)):
            print(name)
            # 写入信息
            #filetxt.write(os.path.join(IMAGE_PATH, METHOD, name)+'\n')
            #gloss_file.write(values['orth']+'\n')
            #text_file.write(values['translation']+' .\n')
            imagePaths = op.get_images_on_directory(os.path.join(IMAGE_PATH, METHOD, name));
            for imagePath in imagePaths:
                datum = op.Datum()
                try:
                    imageToProcess = cv2.imread(imagePath)
                    datum.cvInputData = imageToProcess
                    opWrapper.emplaceAndPop(op.VectorDatum([datum]))
                except TypeError as e:
                    continue
            #     posePoints=datum.poseKeypoints.flatten()
            #     for x in posePoints:
            #         skels_file.write(str(x)+' ')
            #     lefthand=datum.handKeypoints[0].flatten()
            #     for x in lefthand:
            #         skels_file.write(str(x)+' ')
            #     righthand = datum.handKeypoints[1].flatten()
            #     for x in righthand:
            #         skels_file.write(str(x) + ' ')
            # skels_file.write('\n')
        else:
            continue

    # close file
    # skels_file.close()
    # filetxt.close()
    # gloss_file.close()
    # text_file.close()

    end=time.time()
    times=end-start
    time=open('./data/time.txt','w+',encoding='utf-8')
    time.write(str(times))
    time.close()




