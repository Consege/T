from sklearn import preprocessing
import numpy as np
import scipy.sparse as sp
from pyfm import pylibfm
import queue
#主函数
from SimulationRecommand import user,videos,makedata_mat
class Node:
    def __init__(self,vid,result):
        self.vid = vid
        self.result = result

    def __lt__(self,other):
        return self.result<other.result
class SimulationRecommand(object):
    def __init__(self):
        self.User = user.User()
        self.Video = videos.Video()
        self.DataMat = makedata_mat.DataMat()

    def loadDataSet(self,file):
        dataMat = []
        y = []
        with open(file, encoding='utf-8') as fr:
            for line in fr:
                features = line.strip().split(',')
                tmp = []
                len_feature = len(features)
                cnt = 0
                for x in features:
                    if cnt != len_feature - 1:
                        tmp.append(int(x))
                    else:
                        y.append(int(x))
                    cnt += 1
                dataMat.append(tmp)
        return dataMat, y
    def getUserVideo(self,file):
        user_video_dict = dict()
        with open(file,encoding='gbk') as fr:
            for line in fr:
                user_video = line.split()
                if len(user_video) == 5:
                    uid = user_video[2]
                    vid = user_video[3]
                    if user_video_dict.get(uid) is None:
                        user_video_dict[uid] = [vid]
                    else:
                        #print(uid,vid)
                        user_video_dict[uid].append(vid)
            return  user_video_dict
    def isClick(self,uid,vid,user_video_dict):
        if user_video_dict.get(uid) is None:
            return  0
        if vid not in user_video_dict.get(uid):
            return 0
        return  1


    def main(self):
        k=900
        user_mat = self.User.getUsers(k)
        video_mat = self.Video.getVideo()
        min_max_scaler = preprocessing.MinMaxScaler()
        train_X, train_y = self.loadDataSet(r'D:\实验结果\train10.txt')
        train_X_normalized = min_max_scaler.fit_transform(np.mat(train_X))

        train_X_sparse = sp.csr_matrix(np.asarray(train_X_normalized), dtype="double")
        train_yy = np.asarray(train_y)
        fm = pylibfm.FM(num_factors=15,num_iter=20,verbose=True,task="classification",initial_learning_rate=0.0005,learning_rate_schedule="optimal")
        fm.fit(train_X_sparse,train_yy)
        print('Training end...')
        user_count = 0
        fm_true = 0
        #记录用户看了那些视频
        user_video_dict = self.getUserVideo(r'F:\video_click_data2\video_watch_data.txt')
        count = 0
        all_command = 0
        valid_command = 0
        for user in user_mat:
            count += 1
            print(count)
            if(count%10==0):
                print(1.0*count/1000)
            video_cnt = 0
            data_Mat =  []
            #记录video的id，以便后续验证是否真正点击
            video_id = [0 for x in range(80000)]
            import random
            #sub_video_mat = random.sample(video_mat,2000)
            for video in video_mat:
                user_video_feature=[]
                user_video_feature.extend(user[0:-1])
                user_video_feature.extend(video[0:-1])
                video_id[video_cnt] = video[-1]
                video_cnt+=1
               # print(user_video_feature)
                data_Mat.append(user_video_feature)
                #print(len(data_Mat),len(data_Mat[0]),len(train_X),len(train_X[0]))
            test_X_normalized = min_max_scaler.transform(np.mat(data_Mat))
            test_X_sparse=sp.csr_matrix(np.asarray(test_X_normalized),dtype="double")
            #print(test_X_sparse)
            fm_predict_est = fm.predict(test_X_sparse)
            #找到fm_predict_est 的最大值，把该最大值对应的video推荐给user
            video_cnt = 0
            max_value = 0
            vid = video_id[video_cnt]
            top_ten = queue.PriorityQueue()
            top_ten.queue.clear()
            for x in fm_predict_est:
                #print(x)
                # if x==1:
                #     all_command+=1
                #     if(self.isClick(user[-1],video_id[video_cnt],user_video_dict)):
                #         valid_command+=1
                # video_cnt+=1
                if top_ten.qsize()>=1:
                    temp = top_ten.get()
                    if(temp.result <= x):
                        top_ten.put(Node(video_id[video_cnt],x))
                    else:
                        top_ten.put(temp)
                else:
                    top_ten.put(Node(video_id[video_cnt],x))
                video_cnt+=1
            print("==========================")
            while not top_ten.empty():
                tmp = top_ten.get()
                print(tmp.result)
                if(tmp.result>0.5):
                    all_command+=1
                    if self.isClick(user[-1],tmp.vid,user_video_dict):
                        valid_command+=1
                        break
            print(all_command,valid_command,user[-1])
            # for x in fm_predict_est:
            #     if x > max_value and x<0.9:
            #         max_value =x
            #         vid = video_id[video_cnt]
            #     video_cnt += 1
            # print("And")
            # print(max_value)
            # print(user[-1],vid)
            # if max_value>0.5:
            #     user_count += 1
            #     fm_click = self.isClick(user[-1],vid,user_video_dict)
            #     if fm_click == 1:
            #         fm_true += 1
            #         print("yes"+str(user[-1])+" "+str(vid))
        #print("precision is %.5f"%(1.0*fm_true/user_count))
        print(1.0*valid_command/all_command)

if __name__=='__main__':
    simRec=SimulationRecommand()
    simRec.main()