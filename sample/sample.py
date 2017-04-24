import random

def loadDataSet(fileName):
    dataMat = []
    with open(fileName,encoding='utf-8') as fr:
        for line in fr:
            dataMat.append(line)
    return  dataMat

def RandomSampling(dataMat,number):
    try:
        slice = random.sample(dataMat,number)
        return slice
    except:
        print('Sample larger than population')

if __name__ == '__main__':
    dataMat = loadDataSet(r'D:\tencentvideos\交叉特征\test5_1.txt')
    ss = RandomSampling(dataMat,100)
    with open(r'D:\tencentvideos\交叉特征\test101.txt','w',encoding = 'utf-8') as fw:
        for s in ss:
            fw.write(s)