import cv2
import os
import pandas as pd
DATASET_PATH='D:\\dataset\\PHOENIX-2014-T-release-v3\\PHOENIX-2014-T'

def read_image():
    return img


def read_file(PATH):
    #spilt  |
    file=pd.read_csv(PATH,sep='|',header=0)
    # 对数据进行排序
    file=file.sort_values(by='name')
    file=file.reset_index(drop=True)
    return file

#根据excel去找文件，如果找到则进行操作，否则跳过

if __name__=='__main__':
    annotations=os.path.join(DATASET_PATH,'annotations','manual')
    file=os.path.join(annotations,'PHOENIX-2014-T.train.corpus.csv')
    train=read_file(file)
    dataset={}
    # 似乎存在无用数据
    del train['start']
    del train['end']
    # 这里视频和名称相同，使用key索引即可
    del train['video']
    for i in range(0,len(train)):
        dataset[train['name'][i]]={train.columns[j]:train[train.columns[j]][i] for j in range(1,len(train.columns))}
    print(dataset['01April_2010_Thursday_heute-6696'])