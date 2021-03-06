import numpy as np
from sklearn.cluster import KMeans
import random
def get_user_dict(file,user_dict):
    with open(file,encoding = 'gbk',errors='ignore') as fr:
        count = 0
        for line in fr:
            user_profile= line.split('\t')
            if(len(user_profile)==16):
                uid = user_profile[0]
                if(user_dict.get(uid) is None):
                    user_dict[uid] = line
                count += 1
    return  user_dict

def get_user_line(file):
    user_line_dict = dict()
    with open(file,encoding = 'utf-8',errors='ignore') as fr:
        count = 0
        for line in fr:
            user_profile= line.split('\t')
            user_line_dict[user_profile[0]] = count
            count+=1
    return  user_line_dict

def get_video_dict(file,video_dict):
    with open(file,encoding='utf-8',errors = 'ignore') as fr:
        count = 0
        for line in fr:
            video_info = line.split('\t')
            if(len(video_info) == 8):
                vid = video_info[0]
                if(video_dict.get(vid) is None):
                    video_dict[vid] = line
            count += 1
    return  video_dict

def get_video_line(file):
    video_line_dict = dict()
    with open(file,encoding='utf-8',errors = 'ignore') as fr:
        count = 0
        for line in fr:
            video_info = line.split('\t')
            video_line_dict[video_info[0]] = count
            count += 1
    return video_line_dict

def get_videotype(video):
    video_list = video.split('|')
    return  video_list
def get_video_director(director):
    return  director.split('|')
def get_video_actor(actor):
    return  actor.split('|')
def cmp(s):
    return s[1]

def read_some_file(file):
    _list = []
    with open(file,encoding='utf-8') as fr:
        for line in fr:
            _list.append(line[0:-1])
    return  _list
def get_user_browser(broswer):
    return  broswer.split('\\')[-1].lower()
def get_user_interest(interest):
    interest_dict=dict()
    interestes = interest.split('#')
    for x in interestes:
        interest_detail = x.split('|')
        if(len(interest_detail) == 2):
            interest_dict[interest_detail[0]] = interest_detail[1]
    return  interest_dict
def get_user_district(district):
    district_dict  = dict()
    districts = district.split('#')
    for x in districts:
        district_detail = x.split('%')
        if(len(district_detail) == 2):
            district_dict[district_detail[0]] = district_detail[1]
    return  district_dict
def get_user_videotype(video_type):
    video_type_dict = dict()
    video_sub_type_dict = dict()
    video_types = video_type.split('#')
    for x in video_types:
        video_type_detail = x.split('%')
        type_and_subtype = video_type_detail[0].split('@')
        if len(video_type_detail) ==2:
            if len(type_and_subtype)  == 2:
                try:
                    video_type_dict[int(type_and_subtype[0])] = video_type_detail[1]
                    video_sub_type_dict[type_and_subtype[1]] = video_type_detail[1]
                except:
                    pass
            else:
                video_sub_type_dict[type_and_subtype[0]] = video_type_detail[1]
    return video_type_dict , video_sub_type_dict
def get_user_director(director):
    director_dict = dict()
    directors = director.split('#')
    for x in directors:
        director_detail  = x.split('%')
        if len(director_detail) == 2:
            director_dict[director_detail[0]] = director_detail[1]
    return  director_dict

def get_user_actor(actor):
    actor_dict = dict()
    actors = actor.split('#')
    for x in actors:
        actor_detail  = x.split('%')
        if len(actor_detail) == 2:
            actor_dict[actor_detail[0]] = actor_detail[1]
    return  actor_dict
def getUserFeature(uid,user_dict,interest_list,browser_list,video_type_list,district_list,director_list,actor_lis):
    user_profile = user_dict.get(uid)
    user_actor = []
    user_director = []
    user_district = []
    user_video_type = []
    user_video_sub_type = []
    age = 2016
    if user_profile is not None:
        user_profile_detail = user_profile.split('\t')
        if (len(user_profile_detail) == 16 ):
            feature = []
            # 活跃天数
            if user_profile_detail[1] == 'NULL':
                feature.append(0)
            else:
                try:
                    tmp = int(user_profile_detail[1])
                    feature.append(tmp)
                except:
                    feature.append(0)
            # 默认浏览器
            user_broswer = get_user_browser(user_profile_detail[2])

            for x in browser_list:
                if user_broswer == x:
                    feature.append(1)
                else:
                    feature.append(0)
            # cpu核数
            if user_profile_detail[3] == 'NULL':
                feature.append(0)
            else:
                try:
                    tmp = int(user_profile_detail[3])
                    feature.append(tmp)
                except:
                    feature.append(0)
            # 内存
            if user_profile_detail[4] == 'NULL':
                feature.append(0)
            else:
                try:
                    tmp = int(user_profile_detail[4])
                    feature.append(tmp)
                except:
                    feature.append(0)
            # 共存浏览器
            if user_profile_detail[5] == 'NULL':
                feature.append(0)
            else:
                try:
                    tmp = int(user_profile_detail[5])
                    feature.append(tmp)
                except:
                    feature.append(0)
            # 共存安全软件
            if user_profile_detail[6] == 'NULL':
                feature.append(0)
            else:
                try:
                    tmp = int(user_profile_detail[6])
                    feature.append(tmp)
                except:
                     feature.append(0)
            # 大类兴趣标签
            interest_dict = get_user_interest(user_profile_detail[7])
            if interest_dict is None:
                for x in interest_list:
                    feature.append(0)
            else:
                for x in interest_list:
                    if x in interest_dict.keys():
                        try:
                            tmp = int(interest_dict[x])
                            feature.append(tmp)
                        except:
                            feature.append(0)
                    else:
                        feature.append(0)
            # 视频地区标签
            district_dict = get_user_district(user_profile_detail[8])
            if district_dict is None:
                for x in district_list:
                    feature.append(0)
            else:
                for x in district_list:
                    if x in district_dict.keys():
                        try:
                            tmp = int(district_dict[x])
                            user_district.append(x)
                            feature.append(tmp)
                        except:
                            feature.append(0)
                    else:
                        feature.append(0)
            # 视频类型标签(包括视频大类和子类)
            video_type_dict, video_sub_type_dict = get_user_videotype(user_profile_detail[9])
            for i in range(14):
                if video_type_dict is None:
                    feature.append(0)
                else:
                    if (video_type_dict.get(i) is None):
                        feature.append(0)
                    else:
                        try:
                            user_video_type.append(i)
                            tmp = int(video_type_dict.get(i))
                            feature.append(tmp)
                        except:
                            feature.append(0)
            for x in video_type_list:
                if video_sub_type_dict is None:
                    user_video_sub_type.append(0)
                    feature.append(0)
                else:
                    if video_sub_type_dict.get(x) is None:
                        user_video_sub_type.append(0)
                        feature.append(0)
                    else:
                        try:
                            tmp = int(video_sub_type_dict.get(x))
                            user_video_sub_type.append(1.0*tmp/100)
                            feature.append(tmp)
                        except:
                            user_video_sub_type.append(0)
                            feature.append(0)
            # 导演
            director_dict = get_user_director(user_profile_detail[10])
            if director_dict is None:
                for x in director_list:
                    user_director.append(0)
                    feature.append(0)
            else:
                for x in director_list:
                    if x in director_dict.keys():
                        try:
                            tmp = int(director_dict[x])
                            user_director.append(1.0*tmp/100)
                            feature.append(tmp)
                        except:
                            user_director.append(0)
                            feature.append(0)
                    else:
                        user_director.append(0)
                        feature.append(0)
            # 演员
            actor_dict = get_user_actor(user_profile_detail[11])
            if actor_dict is None:
                for x in actor_list:
                    user_actor.append(0)
                    feature.append(0)
            else:
                for x in actor_list:
                    if x in actor_dict.keys():
                        try:
                            tmp = int(actor_dict[x])
                            user_actor.append(1.0*tmp/100)
                            feature.append(tmp)
                        except:
                            user_actor.append(0)
                            feature.append(0)
                    else:
                        user_actor.append(0)
                        feature.append(0)
            # 性别，年龄，学历
            if (user_profile_detail[13] == 'NULL'):
                feature.append(0)
            else:
                try:
                    tmp = int(user_profile_detail[13])
                    feature.append(tmp)
                except:
                    feature.append(0)

            if (user_profile_detail[14] == 'NULL'):
                feature.append(0)
            else:
                try:
                    tmp = int(user_profile_detail[14])
                    age=2016-tmp
                    feature.append(tmp)
                except:
                    feature.append(0)
            if (user_profile_detail[15] == 'NULL'):
                feature.append(0)
            else:
                try:
                    tmp = int(user_profile_detail[15][0:-1])
                    feature.append(tmp)
                except:
                    feature.append(0)
        return  feature,user_actor,user_director,user_district,user_video_type,user_video_sub_type,age

if __name__=='__main__':

    ####加载user_matrix 和 video_matrix
    user_matrix= []
    with open(r'D:\tencentvideos\交叉特征\user_matrix.txt',encoding='utf-8') as fr:
        for line in fr:
            temp_matrix = []
            vec = line.split(',')
            for x in vec:
                temp_matrix.append(float(x))
            user_matrix.append(temp_matrix)

    video_matrix = []
    with open(r'D:\tencentvideos\交叉特征\video_matrix.txt',encoding='utf-8') as fr:
        for line in fr:
            temp_matrix = []
            vec = line.split(',')
            for x in vec:
                temp_matrix.append(float(x))
            video_matrix.append(temp_matrix)
    ############################################
    # 获取挑选出来的兴趣\导演\演员等
    interest_list = read_some_file(r'F:\tencent\user_interest.txt')
    browser_list = read_some_file(r'F:\tencent\browser.txt')
    video_type_list = read_some_file(r'F:\tencent\video_type.txt')
    district_list = read_some_file(r'F:\tencent\districts.txt')
    director_list = read_some_file(r'F:\tencent\director.txt')
    actor_list = read_some_file(r'F:\tencent\actor.txt')
    ############################################
    video_type_list = []
    director_list = []
    actor_list = []
    district_list = []
    with open(r'F:\tencent\video_type.txt',encoding='utf-8') as fr:
        for line in fr:
            video_type_list.append(line[0:-1])
    with open(r'F:\tencent\director.txt',encoding = 'utf-8') as fr:
        for line in fr:
            director_list.append(line[0:-1])
    with open(r'F:\tencent\actor.txt',encoding='utf-8') as fr:
        for line in fr:
            actor_list.append(line[0:-1])
    with open(r'F:\tencent\districts.txt',encoding='utf-8') as fr:
        for line in fr:
            district_list.append(line[0:-1])
    #############################################
    #key为视频id，存储每个视频的特征
    video_feature_dict=dict()
    #对视频进行聚类
    with open(r'F:\video_click_data2\video_info.txt',encoding='gbk') as fr:
        k_means_list = []
        k_means_list_vid = []
        for line in fr:
            video_info = line.split('\t')
            if len(video_info) == 8:
                video_feature = []
                # 视频大类类型
                if (video_info[2] == 'NULL'):
                    video_feature.append(0)
                else:
                    if str(video_info[2]).isdigit():
                        video_feature.append(video_info[2])
                    else:
                        video_feature.append(0)
                # 视频子类型
                v_video_type_list = get_videotype(video_info[3])
                for x in video_type_list:
                    if x in v_video_type_list:
                        video_feature.append(1)
                    else:
                        video_feature.append(0)
                # 导演
                v_director_list = get_video_director(video_info[4])
                for x in director_list:
                    if x in v_director_list:
                        video_feature.append(1)
                    else:
                        video_feature.append(0)
                # 演员
                v_actor_list = get_video_actor(video_info[5])
                for x in actor_list:
                    if x in v_actor_list:
                        video_feature.append(1)
                    else:
                        video_feature.append(0)
                # 上映年份
                if (video_info[6] == 'NULL'):
                    video_feature.append(0)
                else:
                    if str(video_info[6]).isdigit():
                        video_feature.append(video_info[6])
                    else:
                        video_feature.append(0)
                # 地区
                for x in district_list:
                    if x == video_info[7][0:-1]:
                        video_feature.append(1)
                    else:
                        video_feature.append(0)
                k_means_list.append(video_feature)
                if video_feature_dict.get(video_info[0]) is None:
                    video_feature_dict[video_info[0]] = []
                video_feature_dict[video_info[0]].extend(video_feature)
                video_feature.append(video_info[0])
                k_means_list_vid.append(video_feature)
        X = np.array(k_means_list)

        k = 30
        kmeans = KMeans(n_clusters=k).fit(X)
        count = 0
        for line in kmeans.labels_:
            k_means_list_vid[count].append(line)
            count = count + 1
        #cate[i]表示聚类编号为i的所有视频集合
        cate=[[]for i in range(k)]
        for i in range(k):
            for line in k_means_list_vid:
                if line[-1] == i:
                    cate[i].append(line[-2])

        # 打印出聚类查看结果
        # with open('clusterResult.txt', 'w', encoding='utf-8') as fw:
        #     for i in range(k):
        #         with open(r'F:\video_click_data2\video_info.txt') as fr:
        #             for x in fr:
        #                 video_info= x.split()
        #                 vid = video_info[0]
        #                 if vid in cate[i]:
        #                     fw.write(str(i)+' '+x)

        #计算每个用户观看聚类i的次数
        #user_video_dict存储每个用户观看的视频编号的集合
        user_video_dict = dict()
        with open(r'F:\tencent\valid_watch_data.txt',encoding='utf-8') as fr:
            for line in fr:
                user_watch_video = line.split()
                if len(user_watch_video) == 5:
                    uid = user_watch_video[2]
                    vid = user_watch_video[3]
                    if user_video_dict.get(uid) is None:
                        tmp = set()
                        tmp.add(vid)
                        user_video_dict[uid] = tmp
                    else:
                        user_video_dict[uid].add(vid)
        # 记录user和video属于第几行
        user_line_dict = dict()
        video_line_dict = dict()
        video_dict = dict()
        # key 为 uid ,value 为 对应的用户信息
        user_dict = dict()
        user_dict= get_user_dict(r'F:\video_click_data2\user_profile.txt', user_dict)
        user_line_dict = get_user_line(r'F:\selected_user5.txt')
        video_dict = get_video_dict(r'F:\video_click_data2\video_info.txt',video_dict)
        video_line_dict = get_video_line(r'F:\selected_videos5.txt')
        process_bar = 0
        with open(r'D:\tencentvideos\交叉特征\test5_0.txt','w',encoding='utf-8') as fw:
            with open(r'F:\video_click_data2\user_profile.txt',encoding='gbk',errors='ignore') as fr:
                for line in fr:
                    #print(process_bar)
                    process_bar = process_bar + 1
                    if process_bar % 1000 == 0:
                        print(process_bar * 1.0 / 1472174)
                    user_info = line.split('\t')
                    if len(user_info) == 16:
                        uid =  user_info[0]
                        #获取用户看过的视频id
                        user_video = user_video_dict.get(uid)
                        # 人工交叉特征
                        #######################
                        user_actor = []
                        user_director = []
                        user_district = []
                        user_video_type = []
                        user_video_sub_type = []
                        age = 2016
                        ######################
                        # user_feature 存储用户的特征
                        user_feature,user_actor,user_director,user_district,user_video_type,user_video_sub_type,age= getUserFeature(uid,user_dict,interest_list,browser_list,video_type_list,district_list,director_list,actor_list)
                        ###########################

                        #user_watch_video_times[i]存储用户观看聚类i的次数
                        user_watch_video_times = [0 for i in range(k)]
                        if user_video is not None:
                            for x in user_video:
                                for i in range(k):
                                    if x in cate[i]:
                                        user_watch_video_times[i] = user_watch_video_times[i] + 1
                                        break

                        #根据用户观看每个聚类中视频次数/该聚类中视频总数排序
                        class_user_watch_video_times = []
                        for i in range(k):
                            class_user_watch_video_times.append([i,user_watch_video_times[i]/len(cate[i])])
                        class_user_watch_video_times =sorted(class_user_watch_video_times,key = cmp)
                        user_not_seen_videos_count =  0
                        for not_seen_videos in class_user_watch_video_times:
                            kmeans_class = not_seen_videos[0]
                            for video_number in cate[kmeans_class]:
                                #####人工交叉特征(视频)##########
                                video_actor = []
                                video_director = []
                                video_sub_type = []
                                video_year = 2016
                                ################################
                                #print(video_number)
                                #如果该视频确实未被用户点击，则生成一条未点击的记录，由于未点击的记录太多，这里对于每个用户只取9条
                               # print(video_number,len(user_video))
                                if (user_video is None or video_number not in user_video) and video_number in video_dict.keys():

                                    ###获取视频信息############
                                    video_info_line = video_dict.get(video_number)
                                    video_info = video_info_line.split('\t')
                                    if len(video_info) == 8:
                                        # 视频大类类型
                                        video_type = 9999
                                        if (video_info[2] != 'NULL'):
                                            if str(video_info[2]).isdigit():
                                                video_type = int(video_info[2])
                                        # 视频子类型
                                        v_video_type_list = get_videotype(video_info[3])
                                        for x in video_type_list:
                                            if x in v_video_type_list:
                                                video_sub_type.append(1)
                                            else:
                                                video_sub_type.append(0)
                                        # 导演
                                        v_director_list = get_video_director(video_info[4])
                                        for x in director_list:
                                            if x in v_director_list:
                                                video_director.append(1)
                                            else:
                                                video_director.append(0)
                                        # 演员
                                        v_actor_list = get_video_actor(video_info[5])
                                        #print(len(actor_list),len(user_actor),len(video_actor))
                                        for x in actor_list:
                                            if x in v_actor_list:
                                                video_actor.append(1)
                                            else:
                                                video_actor.append(0)
                                        # 上映年份
                                        if (video_info[6] != 'NULL'):
                                            if str(video_info[6]).isdigit():
                                                video_year=int(video_info[6])
                                        # 地区
                                        video_district = video_info[7][0:-1]

                                    ###########################

                                    user_video_feature = video_feature_dict.get(video_number)
                                    #print(user_video_feature)
                                    if user_video_feature is None:
                                        continue
                                    user_not_seen_videos_count = user_not_seen_videos_count + 1
                                    #将该条记录写入文件
                                    feature = []
                                    feature.extend(user_feature)
                                    # 检验特征抽取是否正确
                                    # if len(feature)!= 492:
                                    #     print(feature)
                                    for x in user_video_feature:
                                        feature.append(x)

                                    ###人工交叉特征
                                    #用户年龄和视频上映年份
                                    feature.append(video_year-age)
                                    #用户演员标签和视频演员标签
                                    actor_euler = np.linalg.norm(np.array(user_actor) - np.array(video_actor))
                                    actor_manhattan = sum(abs(np.array(user_actor)-np.array(video_actor)))
                                    actor_chebyshew = abs(np.array(user_actor) - np.array(video_actor)).max()

                                    if np.linalg.norm(np.array(user_actor)) < 1e-8 or np.linalg.norm(np.array(video_actor)) < 1e-8:
                                        actor_cosDis = 0
                                    else:
                                        actor_cosDis = np.dot(np.array(user_actor),np.array(video_actor))/(np.linalg.norm(np.array(user_actor))*np.linalg.norm(np.array(video_actor)))

                                    feature.append(actor_euler)
                                    feature.append(actor_manhattan)
                                    feature.append(actor_chebyshew)
                                    feature.append(actor_cosDis)

                                    ### 用户导演标签和视频导演标签
                                    director_euler  = np.linalg.norm(np.array(user_director) - np.array(video_director))
                                    director_manhattan = sum(abs(np.array(user_director)-np.array(video_director)))
                                    director_chebyshew = abs(np.array(user_director)-np.array(video_director)).max()
                                    if np.linalg.norm(np.array(user_director)) < 1e-8 or np.linalg.norm(np.array(video_director)) < 1e-8:
                                        dirctor_cosDis = 0
                                    else:
                                        director_cosDis=np.dot(np.array(user_director),np.array(video_director))/(np.linalg.norm(np.array(user_director))*np.linalg.norm(np.array(video_director)))
                                    feature.append(director_euler)
                                    feature.append(director_manhattan)
                                    feature.append(director_chebyshew)
                                    feature.append(dirctor_cosDis)

                                    ###用户视频地区标签和视频地区标签
                                    if video_district in user_district:
                                        feature.append(1)
                                    else:
                                        feature.append(0)

                                    ###用户感兴趣的视频大类代号和视频大类代号
                                    if video_type in user_video_type:
                                        feature.append(1)
                                    else:
                                        feature.append(0)

                                    ###用户感兴趣的视频子类型和视频子类型标签
                                    sub_type_euler = np.linalg.norm(np.array(user_video_sub_type)-np.array(video_sub_type))
                                    sub_type_manhattan = sum(abs(np.array(user_video_sub_type)-np.array(video_sub_type)))
                                    sub_type_chewbyshew = abs(np.array(user_video_sub_type) - np.array(video_sub_type)).max()
                                    feature.append(sub_type_euler)
                                    feature.append(sub_type_manhattan)
                                    feature.append(sub_type_chewbyshew)

                                    ###矩阵分解交叉特征

                                    user_line = user_line_dict.get(uid)
                                    video_line =  video_line_dict.get(video_info[0])
                                    if video_line is None or user_line is None:
                                        user_video_euler = 0
                                        user_video_manhattan = 0
                                        user_video_chewbyshew = 0
                                        user_video_cosDis = 0
                                    else:
                                        user_vector = np.array(user_matrix)[user_line]
                                        video_vector = np.array(video_matrix)[:,video_line]
                                        user_video_euler = np.linalg.norm(user_vector - video_vector)
                                        user_video_manhattan = sum(abs(user_vector - video_vector))
                                        user_video_chewbyshew = abs(user_vector-video_vector).max()
                                        if np.linalg.norm(user_vector) < 1e-8 or np.linalg.norm(video_vector) < 1e-8:
                                            user_video_cosDis = 0
                                        else:
                                            user_video_cosDis=np.dot(user_vector,video_vector)/(np.linalg.norm(user_vector)*np.linalg.norm(video_vector))


                                    feature.append(user_video_euler)
                                    feature.append(user_video_manhattan)
                                    feature.append(user_video_chewbyshew)
                                    feature.append(user_video_cosDis)



                                    ######################

                                    #标签
                                    feature.append(0)
                                    feature_len = len(feature)
                                    #检验特征抽取是否正确
                                    # if(feature_len != 870):
                                    #     print(feature_len,feature)
                                    cnt = 0
                                    random_number= random.uniform(0,10)
                                    if random_number<0.1:
                                        for x in feature:
                                            fw.write(str(x))
                                            cnt = cnt + 1
                                            if cnt != feature_len:
                                                fw.write(',')

                                        fw.write('\n')
                                       # print(user_not_seen_videos_count)
                                    if user_not_seen_videos_count > 9:
                                            break
                            if user_not_seen_videos_count > 9:
                                break
