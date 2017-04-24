import random
import numpy as np
from datetime import  *
def get_user_dict(file,user_dict):
    with open(file,encoding = 'utf-8',errors='ignore') as fr:
        count = 0
        for line in fr:
            user_profile= line.split('\t')
            if(len(user_profile)==16):
                uid = user_profile[0]
                if(user_dict.get(uid) is None):
                    user_dict[uid] = line
            count+=1
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
    return interest_dict
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
def get_videotype(video):
    video_list = video.split('|')
    return  video_list
def get_video_director(director):
    return  director.split('|')
def get_video_actor(actor):
    return  actor.split('|')
def readFile(file):
    #记录user和video属于第几行
    user_line_dict = dict()
    #key 为 uid ,value 为 对应的用户信息
    user_dict=dict()
    #key 为 vid ,value为对应的视频信息

    video_dict=dict()
    user_line_dict = get_user_line(r'F:\selected_user5.txt')
    user_dict=get_user_dict(r'F:\video_click_data2\user_profile.txt',user_dict)
    video_dict=get_video_dict(r'F:\video_click_data2\video_info.txt',video_dict)
    video_line_dict = get_video_line(r'F:\selected_videos5.txt')


    #获取挑选出来的兴趣\导演\演员等
    interest_list=read_some_file(r'F:\tencent\user_interest.txt')
    browser_list = read_some_file(r'F:\tencent\browser.txt')
    video_type_list = read_some_file(r'F:\tencent\video_type.txt')
    district_list = read_some_file(r'F:\tencent\districts.txt')
    director_list = read_some_file(r'F:\tencent\director.txt')
    actor_list = read_some_file(r'F:\tencent\actor.txt')

    # 用户矩阵
    user_matrix = []
    with open(r'D:\tencentvideos\交叉特征\user_matrix.txt', encoding='utf-8') as fr:
        for line in fr:
            temp_matrix = []
            vec = line.split(',')
            for x in vec:
                temp_matrix.append(float(x))
            user_matrix.append(temp_matrix)
    #视频矩阵
    video_matrix = []
    with open(r'D:\tencentvideos\交叉特征\video_matrix.txt',encoding='utf-8') as fr:
        for line in fr:
            temp_matrix = []
            vec = line.split(',')
            if len(vec)<10:
                continue
            for x in vec:
                temp_matrix.append(float(x))
            video_matrix.append(temp_matrix)
    with open(file , encoding='gbk') as fr:
        with open(r'D:\tencentvideos\交叉特征\test5_1.txt','w',encoding='utf-8') as fw:
            count_line = 0
            for line in fr:
                count_line = count_line + 1
                if count_line%10000 ==0:
                    print(count_line*1.0/19389877)
                user_watch_data = line.split()
                if(len(user_watch_data) == 5):
                    user_profile = user_dict.get(user_watch_data[2])
                    video_info = video_dict.get(user_watch_data[3])
                    if user_profile is not None and video_info is not None:
                        user_profile_detail = user_profile.split('\t')
                        video_info_detail = video_info.split('\t')
                        if user_dict.get(user_profile_detail[0]) is None or video_dict.get(video_info_detail[0]) is None:
                            continue
                        if(len(user_profile_detail) ==16 and len(video_info_detail) == 8):
                            ############################
                            user_actor = []
                            video_actor = []
                            user_director = []
                            video_director = []
                            user_district = []
                            user_video_type = []
                            user_video_sub_type = []
                            video_sub_type = []
                            age = 2016  #这里的age是用户出生年份
                            video_year = 2016
                            ############################
                            feature = []
                            #活跃天数
                            if user_profile_detail[1] == 'NULL':
                                feature.append(0)
                            else:
                                try:
                                    tmp=int(user_profile_detail[1])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            #默认浏览器
                            user_broswer = get_user_browser(user_profile_detail[2])
                            for x in browser_list:
                                if user_broswer == x:
                                    feature.append(1)
                                else:
                                    feature.append(0)
                            #cpu核数
                            if user_profile_detail[3] == 'NULL':
                                feature.append(0)
                            else:
                                try:
                                    tmp=int(user_profile_detail[3])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            #内存
                            if user_profile_detail[4] =='NULL':
                                feature.append(0)
                            else:
                                try:
                                    tmp=int(user_profile_detail[4])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            #共存浏览器
                            if user_profile_detail[5] == 'NULL':
                                feature.append(0)
                            else:
                                try:
                                    tmp =int(user_profile_detail[5])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            #共存安全软件
                            if user_profile_detail[6] == 'NULL':
                                feature.append(0)
                            else:
                                try:
                                    tmp = int(user_profile_detail[6])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            #大类兴趣标签
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
                            #视频地区标签
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
                            #视频类型标签(包括视频大类和子类)
                            video_type_dict ,video_sub_type_dict= get_user_videotype(user_profile_detail[9])
                            for i in range(14):
                                if video_type_dict is None:
                                    feature.append(0)
                                else:
                                    if(video_type_dict.get(i) is None):
                                        feature.append(0)
                                    else:
                                        try:
                                            tmp = int(video_type_dict.get(i))
                                            if(tmp!=0):
                                                user_video_type.append(i)
                                            feature.append(tmp)
                                        except:
                                            feature.append(0)

                            for x in  video_type_list:
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
                                            user_video_sub_type.append(tmp)
                                            feature.append(tmp)
                                        except:
                                            user_video_sub_type.append(0)
                                            feature.append(0)
                            #导演
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
                                            feature.append(0)
                                            user_director.append(0)
                                    else:
                                        feature.append(0)
                                        user_director.append(0)
                            #演员
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
                            #性别，年龄，学历
                            if(user_profile_detail[13]=='NULL'):
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

                                    age = datetime.today().year-tmp

                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            if (user_profile_detail[15][0:-1] == 'NULL'):
                                feature.append(0)
                            else:
                                try:
                                    tmp = int(user_profile_detail[15][0:-1])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            #视频大类类型
                            video_type  = 9999
                            if(video_info_detail[2] == 'NULL'):
                                feature.append(0)
                            else:
                                try:
                                    tmp = int(video_info_detail[2])
                                    video_type = tmp
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            #视频子类型
                            v_video_type_list=get_videotype(video_info_detail[3])
                            for x in video_type_list:
                                if x in v_video_type_list:
                                    video_sub_type.append(1)
                                    feature.append(1)
                                else:
                                    video_sub_type.append(0)
                                    feature.append(0)
                            #导演
                           # print(video_info_detail[4])
                            v_director_list = get_video_director(video_info_detail[4])
                            for x in director_list:
                                if x in v_director_list:
                                    feature.append(1)
                                    video_director.append(1)
                                else:
                                    video_director.append(0)
                                    feature.append(0)
                            #演员
                            v_actor_list = get_video_actor(video_info_detail[5])
                            for x in actor_list:
                                if x in v_actor_list:
                                    video_actor.append(1)
                                    feature.append(1)
                                else:
                                    video_actor.append(0)
                                    feature.append(0)
                            #上映年份
                            if(video_info_detail[6] == 'NULL'):
                                video_year = 0
                                feature.append(0)
                            else:
                                try:
                                    tmp = int(video_info_detail[6])

                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            #地区
                            video_district = video_info_detail[7][0:-1]
                            for x in district_list:
                                if x == video_info_detail[7][0:-1]:
                                    feature.append(1)
                                else:
                                    feature.append(0)

                            #######人工交叉特征
                            #用户年龄和视频上映年份
                            feature.append(video_year-age)

                            #用户演员标签和视频演员标签
                            actor_euler = np.linalg.norm(np.array(user_actor) - np.array(video_actor))
                            actor_manhattan = sum(abs(np.array(user_actor)-np.array(video_actor)))
                            actor_chebyshew = abs(np.array(user_actor)-np.array(video_actor)).max()

                            if np.linalg.norm(np.array(user_actor)) <1e-8 or np.linalg.norm(np.array(video_actor)) < 1e-8:
                                actor_cosDis = 0
                            else:
                                actor_cosDis = np.dot(np.array(user_actor),np.array(video_actor))/(np.linalg.norm(np.array(user_actor))*np.linalg.norm(np.array(video_actor)))
                            feature.append(actor_euler)
                            feature.append(actor_manhattan)
                            feature.append(actor_chebyshew)
                            feature.append(actor_cosDis)
                            # #用户导演标签和视频导演标签
                            director_euler = np.linalg.norm(np.array(user_director) - np.array(video_director))
                            director_manhattan = sum(abs(np.array(user_director)-np.array(video_director)))
                            director_chebyshew = abs(np.array(user_director) - np.array(video_director)).max()
                            if np.linalg.norm(np.array(user_director)) <1e-8 or np.linalg.norm(np.array(video_director)) < 1e-8:
                                director_cosDis = 0
                            else:
                                director_cosDis = np.dot(np.array(user_director),np.array(video_director))/(np.linalg.norm(np.array(user_director))*np.linalg.norm(np.array(video_director)))
                            feature.append(director_euler)
                            feature.append(director_manhattan)
                            feature.append(director_chebyshew)
                            feature.append(director_cosDis)
                            #用户视频地区标签视频地区标签
                            if video_district in user_district:
                                feature.append(1)
                            else:
                                feature.append(0)
                            #用户感兴趣的视频大类代号和视频大类标签
                            if video_type in user_video_type:
                                feature.append(1)
                            else:
                                feature.append(0)
                            #用户感兴趣的视频子类型标签和视频子类型标签
                            sub_type_euler = np.linalg.norm(np.array(user_video_sub_type) - np.array(video_sub_type))
                            sub_type_manhattan = sum(abs(np.array(user_video_sub_type) -  np.array(video_sub_type)))
                            sub_type_chewbyshew = abs(np.array(user_video_sub_type) - np.array(video_sub_type)).max()
                            feature.append(sub_type_euler)
                            feature.append(sub_type_manhattan)
                            feature.append(sub_type_chewbyshew)

                            #矩阵分解交叉特征
                            user_line = user_line_dict.get(user_profile_detail[0])
                            video_line = video_line_dict.get(video_info_detail[0])
                           # print(user_line,video_line)
                            if video_line is None or user_line is None:
                                user_video_euler=0
                                user_video_manhattan=0
                                user_video_chewbyshew=0
                                user_video_cosDis = 0
                            else:
                                #print(video_matrix[1])
                                #print(video_line,len(video_matrix[0]),len(video_matrix))
                                user_vector = np.array(user_matrix)[user_line]
                                video_vector = np.array(video_matrix)[:,video_line]
                                user_video_euler = np.linalg.norm(user_vector - video_vector)
                                user_video_manhattan = sum(abs(user_vector-video_vector))
                                user_video_chewbyshew = abs(user_vector-video_vector).max()

                                if np.linalg.norm(user_vector) < 1e-8 or np.linalg.norm(video_vector) < 1e-8:
                                    user_video_cosDis = 0
                                else:
                                    user_video_cosDis = np.dot(user_vector, video_vector) / (np.linalg.norm(user_vector) * np.linalg.norm(video_vector))


                            feature.append(user_video_euler)
                            feature.append(user_video_manhattan)
                            feature.append(user_video_chewbyshew)
                            feature.append(user_video_cosDis)

                            #标签
                            feature.append(1)
                            count = 0
                            feature_len = len(feature)
                            random_number = random.uniform(0,10)
                            if random_number <0.05:
                                for x in feature:
                                    count = count+1
                                    fw.write(str(x))
                                    if count!=feature_len:
                                        fw.write(',')
                                fw.write('\n')





if __name__=='__main__':
    readFile(r'F:\tencent\valid_watch_data.txt')