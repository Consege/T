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
                        tmp.append(float(x))
                    else:
                        y.append(float(x))
                    cnt += 1
                dataMat.append(tmp)
        return dataMat, y
    def getUserVideo(self,file):
        user_video_dict = dict()
        with open(file,encoding='gbk') as fr:
            for line in fr:
                user_video = line.split()
                if len(user_video) == 3:
                    uid = user_video[0]
                    vid = user_video[1]
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

    def get_user_line(self,file):
        user_line_dict = dict()
        with open(file, encoding='utf-8', errors='ignore') as fr:
            count = 0
            for line in fr:
                user_profile = line.split('\t')
                user_line_dict[user_profile[0]] = count
                count += 1
        return user_line_dict

    def get_video_line(self, file):
        video_line_dict = dict()
        with open(file, encoding='utf-8', errors='ignore') as fr:
            count = 0
            for line in fr:
                video_info = line.split('\t')
                video_line_dict[video_info[0]] = count
                count += 1
        return video_line_dict

    def main(self):
        user_matrix = []
        with open(r'D:\实验结果\推荐\大于30\电视剧\user_matrix.txt', encoding='utf-8') as fr:
            for line in fr:
                temp_matrix = []
                vec = line.split(',')
                for x in vec:
                    temp_matrix.append(float(x))
                user_matrix.append(temp_matrix)
        # 视频矩阵
        video_matrix = []
        with open(r'D:\实验结果\推荐\大于30\电视剧\video_matrix.txt', encoding='utf-8') as fr:
            for line in fr:
                temp_matrix = []
                vec = line.split(',')
                if len(vec) < 10:
                    continue
                for x in vec:
                    temp_matrix.append(float(x))
                video_matrix.append(temp_matrix)
        # 记录user和video属于第几行
        user_line_dict = self.get_user_line(r'D:\实验结果\推荐\大于30\大于30_users.txt')
        video_line_dict = self.get_video_line(r'D:\实验结果\推荐\大于30\电视剧.txt')
        k=399
        user_mat,user_actor_dict,user_director_dict,user_district_dict,user_video_type_dict,user_video_sub_type_dict,user_age_dict = self.User.getUsers(k)
        video_mat,video_actor_dict,video_director_dict,video_type_dict,video_sub_type_dict,video_district_dict,video_year_dict = self.Video.getVideo()
        print(len(user_mat),len(video_mat))
        min_max_scaler = preprocessing.MinMaxScaler()
        train_X, train_y = self.loadDataSet(r'D:\tencentvideos\交叉特征\电视剧\train1.txt')
        train_X_normalized = min_max_scaler.fit_transform(np.mat(train_X))

        train_X_sparse = sp.csr_matrix(np.asarray(train_X_normalized), dtype="double")
        train_yy = np.asarray(train_y)
        fm = pylibfm.FM(num_factors=15,num_iter=20,verbose=True,task="classification",initial_learning_rate=0.0002,learning_rate_schedule="optimal")
        fm.fit(train_X_sparse,train_yy)
        print('Training end...')
        user_count = 0
        fm_true = 0
        #记录用户看了那些视频
        user_video_dict = self.getUserVideo(r'D:\tencentvideos\merged_user_video_watch_data2.txt')
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
            #####人工交叉特征
            user_actor = user_actor_dict.get(user[-1])
            user_director = user_director_dict.get(user[-1])
            user_video_type = user_video_type_dict.get(user[-1])
            user_video_sub_type = user_video_sub_type_dict.get(user[-1])
            user_district = user_district_dict.get(user[-1])
            #age = user_age_dict.get(user[-1])

            #######################
            for video in video_mat:

                #################
                video_actor = video_actor_dict.get(video[-1])
                video_director = video_director_dict.get(video[-1])
                video_type = video_type_dict.get(video[-1])
               # video_sub_type = video_sub_type_dict.get(video[-1])
                #video_district = video_district_dict.get(video[-1])
                #video_year = video_year_dict.get(video[-1])
                ################
                user_video_feature=[]
                user_video_feature.extend(user[0:-1])
                user_video_feature.extend(video[0:-1])

                #######人工交叉特征
                # 用户年龄和视频上映年份
                #user_video_feature.append(video_year - age)

                # 用户演员标签和视频演员标签
                #actor_euler = np.linalg.norm(np.array(user_actor) - np.array(video_actor))
                actor_manhattan = sum(abs(np.array(user_actor)-np.array(video_actor)))
                actor_chebyshew = abs(np.array(user_actor)-np.array(video_actor)).max()

                if np.linalg.norm(np.array(user_actor)) < 1e-8 or np.linalg.norm(np.array(video_actor)) < 1e-8:
                    actor_cosDis = 0
                else:
                    actor_cosDis = np.dot(np.array(user_actor), np.array(video_actor)) / (np.linalg.norm(np.array(user_actor)) * np.linalg.norm(np.array(video_actor)))
                #user_video_feature.append(actor_euler)
               # user_video_feature.append(actor_manhattan)
               # user_video_feature.append(actor_chebyshew)
                user_video_feature.append(actor_cosDis)
                # #用户导演标签和视频导演标签
               # director_euler = np.linalg.norm(np.array(user_director) - np.array(video_director))
                director_manhattan = sum(abs(np.array(user_director)-np.array(video_director)))
                director_chebyshew = abs(np.array(user_director) - np.array(video_director)).max()
                if np.linalg.norm(np.array(user_director)) < 1e-8 or np.linalg.norm(np.array(video_director)) < 1e-8:
                    director_cosDis = 0
                else:
                    director_cosDis = np.dot(np.array(user_director), np.array(video_director)) / (np.linalg.norm(np.array(user_director)) * np.linalg.norm(np.array(video_director)))
               # user_video_feature.append(director_euler)
                #user_video_feature.append(director_manhattan)
               # user_video_feature.append(director_chebyshew)
                user_video_feature.append(director_cosDis)
                # 用户视频地区标签视频地区标签
                # if video_district in user_district:
                #     user_video_feature.append(1)
                # else:
                #     user_video_feature.append(0)
                # 用户感兴趣的视频大类代号和视频大类标签
                if video_type in user_video_type:
                    user_video_feature.append(1)
                else:
                    user_video_feature.append(0)
                # 用户感兴趣的视频子类型标签和视频子类型标签
               # sub_type_euler = np.linalg.norm(np.array(user_video_sub_type) - np.array(video_sub_type))
                #sub_type_manhattan = sum(abs(np.array(user_video_sub_type) -  np.array(video_sub_type)))
               # sub_type_chewbyshew = abs(np.array(user_video_sub_type) - np.array(video_sub_type)).max()
                #user_video_feature.append(sub_type_euler)
                #user_video_feature.append(sub_type_manhattan)
                #user_video_feature.append(sub_type_chewbyshew)

                # 矩阵分解交叉特征
                user_line = user_line_dict.get(user[-1])
                video_line = video_line_dict.get(video[-1])
                # print(user_line,video_line)
                if video_line is None or user_line is None:
                    user_video_euler = 0
                    user_video_manhattan=0
                    user_video_chewbyshew=0
                    user_video_cosDis = 0
                else:
                    # print(video_matrix[1])
                    # print(video_line,len(video_matrix[0]),len(video_matrix))
                    user_vector = np.array(user_matrix)[user_line]
                    video_vector = np.array(video_matrix)[:, video_line]
                    #user_video_euler = np.linalg.norm(user_vector - video_vector)
                    user_video_manhattan = sum(abs(user_vector-video_vector))
                    user_video_chewbyshew = abs(user_vector-video_vector).max()

                    if np.linalg.norm(user_vector) < 1e-8 or np.linalg.norm(video_vector) < 1e-8:
                        user_video_cosDis = 0
                    else:
                        user_video_cosDis = np.dot(user_vector, video_vector) / (
                        np.linalg.norm(user_vector) * np.linalg.norm(video_vector))

               # user_video_feature.append(user_video_euler)
                #user_video_feature.append(user_video_manhattan)
                #user_video_feature.append(user_video_chewbyshew)
                user_video_feature.append(user_video_cosDis)




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
                print(tmp.result,tmp.vid)
                if(tmp.result>0):
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