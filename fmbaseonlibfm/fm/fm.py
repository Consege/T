from pyfm import pylibfm
import  numpy as np
import scipy.sparse as sp
from sklearn import preprocessing
from sklearn import metrics
import matplotlib.pyplot as plt
def loadDataSet(file):
    dataMat = []
    y = []
    with open(file,encoding = 'utf-8') as fr:
        for line in fr:
            features = line.strip().split(',')
            tmp = []
            len_feature = len(features)
            cnt = 0
            for x in features:
                if cnt != len_feature - 1:
                    tmp.append(float(x))
                else:
                    y.append(float(x))
                cnt += 1
            dataMat.append(tmp)
    return  dataMat,y

if __name__ == "__main__":
    train_X ,train_y = loadDataSet(r'D:\实验结果\train10.txt')
    test_X, test_y = loadDataSet(r'D:\实验结果\test10.txt')
    min_max_scaler = preprocessing.MinMaxScaler()
    train_X_normalized = min_max_scaler.fit_transform(np.mat(train_X))
    test_X_normalized = min_max_scaler.transform(np.mat(test_X))
    train_X_sparse =  sp.csr_matrix(np.asarray(train_X_normalized),dtype="double")
    test_X_sparse = sp.csr_matrix(np.asarray(test_X_normalized),dtype="double")
    train_yy = np.asarray(train_y)
    test_yy = np.asarray(test_y)
    fm = pylibfm.FM(num_factors=15,num_iter=20,verbose=True,task="classification",initial_learning_rate=0.001,learning_rate_schedule="optimal")
    fm.fit(train_X_sparse,train_yy)
    predict = fm.predict(test_X_sparse)
    cnt = 0
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    predict_list = []
    for x in predict:
        if(x>=0.5):
            predict_list.append(1)
        else:
            predict_list.append(0)
        if x >= 0.5 and test_yy[cnt] == 1:
            tp += 1
        if x >= 0.5 and test_yy[cnt] == 0:
            fp += 1
        if x < 0.5 and test_yy[cnt] == 1:
            fn += 1
        if x < 0.5 and test_yy[cnt] == 0:
            tn += 1
        cnt += 1
    print(tp, fp, tn, fn)
    logloss = 0
    cnt = 0
    with open('predict.txt','w') as fw:
        for x in predict:
            fw.write(str(x)+"\n")
    import math
    MCC = (tp*tn-fp*fn)/math.sqrt( (tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
    print(MCC)
    print("Validation log loss: %.4f" % metrics.log_loss(test_yy, predict))
    print(metrics.classification_report(test_yy,predict_list))
    fpr, tpr, thresholds = metrics.roc_curve(test_yy, predict)
    print('AUC %f' % metrics.auc(fpr, tpr))
    #对角线
    plt.plot([0,1],[0,1],'--',color=(0.5,0.5,0.5),label = "Luck")
    plt.plot(fpr,tpr,color=(0.9,0.8,0.5))
    plt.xlim([-0.05,1.05])
    plt.ylim([-0.05,1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Receive operation characteristic curve")
    plt.legend(loc='lower right')
    plt.show()