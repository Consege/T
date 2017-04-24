import pandas as pd
from sklearn import preprocessing
import numpy as np
import lightgbm as lgb
from  sklearn.linear_model import LogisticRegression
from  sklearn import metrics
import math
import scipy.sparse as sp
from pyfm import pylibfm
import matplotlib.pyplot as plt
df_data_train = pd.read_csv(r'D:\实验结果\train10.txt',header = None ,sep=',',encoding='gbk')
X_train = df_data_train.drop(len(df_data_train.keys())-1,axis = 1)
y_train = df_data_train[len(df_data_train.keys())-1]
df_data_test = pd.read_csv(r'D:\实验结果\test10.txt',header = None,sep=',',encoding='gbk')
X_test = df_data_test.drop(len(df_data_test.keys())-1,axis = 1)
y_test = df_data_test[len(df_data_test.keys())-1]
min_max_scaler = preprocessing.MinMaxScaler()
X_train_normalized = min_max_scaler.fit_transform(np.mat(X_train))
X_test_normalized = min_max_scaler.transform(np.mat(X_test))
y_test_list = list(y_test)
print(X_train.shape)
print(X_test.shape)
print(X_train_normalized.shape)
print(X_test_normalized.shape)
# gbdt + lr result
lgb_train = lgb.Dataset(X_train,y_train)
lgb_eval = lgb.Dataset(X_test,y_test,reference=lgb_train)

#specify your configuration as a dict
params = {
    'task' : 'train',
    'application' : 'binary',
    'boosting_type' : 'gbdt',
    'learning_rate' : 0.001,
    'num_leaves' : 32,
    'feature_fraction': 0.9 ,
    'bagging_fraction':  0.8 ,
    'bagging_freq' : 5 ,
    'verbose': 0 ,
    'metric' : 'binary_logloss'
}

num_leaf = 32
print("gradient boosting machine start...")
print('Start training...')
gbm = lgb.train(params,lgb_train,num_boost_round=100,valid_sets= lgb_train)

print('Start predicting...')
y_pred = gbm.predict(X_train,pred_leaf = True)
print('Writing transformed training data')
transformed_training_matrix  = np.zeros([len(y_pred),len(y_pred[0])*num_leaf ] , dtype = np.int64)
yy_train = list(y_train)
yy_test = list(y_test)

for i in range (0,len(y_pred)):
    temp = np.arange(len(y_pred[0])) * num_leaf -1 + np.array(y_pred[i])
    transformed_training_matrix[i][temp] += 1
y_pred = gbm.predict(X_test,pred_leaf=True)
print('Writing transformed testing data')
transformed_testing_matrix  = np.zeros([len(y_pred),len(y_pred[0])*num_leaf ] , dtype = np.int64)
for i in range (0,len(y_pred)):
    temp = np.arange(len(y_pred[0])) * num_leaf -1 + np.array(y_pred[i])
    transformed_testing_matrix[i][temp] += 1

lm = LogisticRegression(penalty='l2', C=0.1)
lm.fit(transformed_training_matrix, y_train)
gbm_predicted = lm.predict(transformed_testing_matrix)
# scores = lm.decision_function(transformed_testing_matrix)
gbm_y_pred_est = lm.predict_proba(transformed_testing_matrix)[:, 1]
fp = 0
fn = 0
tp = 0
tn = 0
array_len = len(gbm_predicted)
print(array_len)
for i in range(array_len):
    if gbm_predicted[i] != y_test_list[i]:
        if gbm_predicted[i] == 1 and y_test_list[i] == 0:
            fp += 1
        else:
            fn += 1
    else:
        if gbm_predicted[i] == 1:
            tp += 1
        else:
            tn += 1
print(tp, fp, tn, fn)
#MCC = (tp * tn - fp * fn) / math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
#print(MCC)
print(metrics.classification_report(y_test_list, gbm_predicted))
print("log loss %f" % metrics.log_loss(y_test, gbm_y_pred_est))
fpr, tpr, thresholds = metrics.roc_curve(y_test, gbm_y_pred_est)
print('AUC %f' % metrics.auc(fpr, tpr))

print("gradient boosting machine end...")

print("FM start...")
train_X_sparse =  sp.csr_matrix(np.asarray(X_train_normalized),dtype="double")
test_X_sparse = sp.csr_matrix(np.asarray(X_test_normalized),dtype="double")
train_yy = np.asarray(y_train)
test_yy = np.asarray(y_test)
fm = pylibfm.FM(num_factors=15,num_iter=20,verbose=True,task="classification",initial_learning_rate=0.001,learning_rate_schedule="optimal")
fm.fit(train_X_sparse,train_yy)
fm_predict_est = fm.predict(test_X_sparse)
cnt = 0
tp = 0
fp = 0
tn = 0
fn = 0
fm_predict = []
for x in fm_predict_est:
    if(x>=0.5):
        fm_predict.append(1)
    else:
        fm_predict.append(0)
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
MCC = (tp*tn-fp*fn)/math.sqrt( (tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
print(MCC)
print("Validation log loss: %.4f" % metrics.log_loss(test_yy, fm_predict_est))
print(metrics.classification_report(test_yy,fm_predict))
fpr, tpr, thresholds = metrics.roc_curve(test_yy, fm_predict_est)
print('AUC %f' % metrics.auc(fpr, tpr))
print("FM end...")
print("Logistic Regression start...")
#Logistic regression

lg = LogisticRegression(penalty='l2',C=0.01)
lg.fit(X_train_normalized,y_train)
lg_predicted  = lg.predict(X_test_normalized)
lg_y_pred_est = lg.predict_proba(X_test_normalized)[:,1]
fp = 0
fn = 0
tp = 0
tn = 0
array_len = len(lg_predicted)
print(array_len)
for i in range(array_len):
    if lg_predicted[i] != y_test_list[i]:
        if lg_predicted[i] == 1 and y_test_list[i] == 0:
            fp +=1
        else:
            fn += 1
    else:
        if lg_predicted[i] == 1:
            tp += 1
        else:
            tn += 1
print(tp,fp,tn,fn)

print (metrics.classification_report(y_test_list,lg_predicted))
print ("log loss %f"%metrics.log_loss(y_test,lg_y_pred_est))
fpr ,tpr ,thresholds = metrics.roc_curve(y_test,lg_y_pred_est)
print('AUC %f'%metrics.auc(fpr,tpr))

print("Logistic Regression end...")

predict = []

fp = 0
fn = 0
tp = 0
tn = 0
for i in range(array_len):
    voteGet = 0
    if gbm_predicted[i]==1:
        voteGet+=1
    if fm_predict[i] ==1 :
        voteGet+=1
    if lg_predicted[i] == 1:
        voteGet+=1
    if voteGet>1:
        predict.append(1)
    else:
        predict.append(0)

    if predict[i] != y_test_list[i]:
        if predict[i] == 1 and y_test_list[i] == 0:
            fp +=1
        else:
            fn += 1
    else:
        if predict[i] == 1:
            tp += 1
        else:
            tn += 1
print(tp,fp,tn,fn)
print (metrics.classification_report(y_test_list,predict))


gbdt_fpr,gbdt_tpr,gbdt_threshold = metrics.roc_curve(y_test,gbm_y_pred_est)
fm_fpr,fm_tpr,fm_threshold = metrics.roc_curve(y_test,fm_predict_est)
lr_fpr,lr_tpr,lr_threshold= metrics.roc_curve(y_test,lg_y_pred_est)

plt.plot([0,1],[0,1],'--',color=(0.5,0.5,0.5))
plt.plot(gbdt_fpr,gbdt_tpr,color = '#990033',label ="GBDT+LR")
plt.plot(fm_fpr,fm_tpr,color='#339933',label="FM")
plt.plot(lr_fpr,lr_tpr,color="#000099",label="LR")
plt.xlim([-0.05,1.05])
plt.ylim([-0.05,1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receive operation characteristic curve")
plt.legend(loc="lower right")
plt.show()