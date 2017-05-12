# 随机抽取1000个用户用作测试 , 并提取用户特征
import random

class User(object):
    def get_user_browser(self,broswer):
        return broswer.split('\\')[-1].lower()

    def get_user_interest(self,interest):
        interest_dict = dict()
        interestes = interest.split('#')
        for x in interestes:
            interest_detail = x.split('|')
            if (len(interest_detail) == 2):
                interest_dict[interest_detail[0]] = interest_detail[1]

        return  interest_dict

    def get_user_district(self,district):
        district_dict = dict()
        districts = district.split('#')
        for x in districts:
            district_detail = x.split('%')
            if (len(district_detail) == 2):
                district_dict[district_detail[0]] = district_detail[1]
        return  district_dict
    def get_user_videotype(self,video_type):
        video_type_dict = dict()
        video_sub_type_dict = dict()
        video_types = video_type.split('#')
        for x in video_types:
            video_type_detail = x.split('%')
            type_and_subtype = video_type_detail[0].split('@')
            if len(video_type_detail) == 2:
                if len(type_and_subtype) == 2:
                    try:
                        video_type_dict[int(type_and_subtype[0])] = video_type_detail[1]
                        video_sub_type_dict[type_and_subtype[1]] = video_type_detail[1]
                    except:
                        pass
                else:
                    video_sub_type_dict[type_and_subtype[0]] = video_type_detail[1]
        return video_type_dict, video_sub_type_dict

    def get_user_director(self,director):
        director_dict = dict()
        directors = director.split('#')
        for x in directors:
            director_detail = x.split('%')
            if len(director_detail) == 2:
                director_dict[director_detail[0]] = director_detail[1]
        return director_dict

    def get_user_actor(self,actor):
        actor_dict = dict()
        actors = actor.split('#')
        for x in actors:
            actor_detail = x.split('%')
            if len(actor_detail) == 2:
                actor_dict[actor_detail[0]] = actor_detail[1]
        return actor_dict

    def get_videotype(self,video):
        video_list = video.split('|')
        return video_list

    def get_video_director(self,director):
        return director.split('|')

    def get_video_actor(self,actor):
        return actor.split('|')


    def read_some_file(self,file):
        _list = []
        with open(file, encoding='utf-8') as fr:
            for line in fr:
                _list.append(line[0:-1])
        return _list

    def RandomSampling(self,user_data,k):
        try:
            slice = random.sample(user_data,k)
            return slice
        except:
            print('sample larger than population')

    def getUserMat(self,user_list):
        user_mat = []
        # 获取挑选出来的兴趣\导演\演员等
        interest_list = self.read_some_file(r'F:\tencent\user_interest.txt')
        browser_list = self.read_some_file(r'F:\tencent\browser.txt')
        video_type_list = self.read_some_file(r'F:\tencent\video_type.txt')
        district_list = self.read_some_file(r'F:\tencent\districts.txt')
        director_list = self.read_some_file(r'F:\tencent\director.txt')
        actor_list = self.read_some_file(r'F:\tencent\actor.txt')
        for line in user_list:
            user_profile = line.split('\t')
            if (len(user_profile) == 16):
                feature = []
                #活跃天数
                if user_profile[1] == 'NULL':
                    feature.append(0)
                else:
                    try:
                        tmp=int(user_profile[1])
                        feature.append(tmp)
                    except:
                        feature.append(0)
                #默认浏览器
                user_broswer = self.get_user_browser(user_profile[2])
                for x in browser_list:
                    if user_broswer == x:
                        feature.append(1)
                    else:
                        feature.append(0)
                #cpu核数
                if user_profile[3] == 'NULL':
                    feature.append(0)
                else:
                    try:
                        tmp=int(user_profile[3])
                        feature.append(tmp)
                    except:
                        feature.append(0)
                #内存
                if user_profile[4] =='NULL':
                    feature.append(0)
                else:
                    try:
                        tmp=int(user_profile[4])
                        feature.append(tmp)
                    except:
                        feature.append(0)
                #共存浏览器
                if user_profile[5] == 'NULL':
                    feature.append(0)
                else:
                    try:
                        tmp =int(user_profile[5])
                        feature.append(tmp)
                    except:
                        feature.append(0)
                #共存安全软件
                if user_profile[6] == 'NULL':
                    feature.append(0)
                else:
                    try:
                        tmp = int(user_profile[6])
                        feature.append(tmp)
                    except:
                        feature.append(0)
                # 大类兴趣标签
                interest_dict = self.get_user_interest(user_profile[7])
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
                district_dict = self.get_user_district(user_profile[8])
                if district_dict is None:
                    for x in district_list:
                        feature.append(0)
                else:
                    for x in district_list:
                        if x in district_dict.keys():
                            try:
                                tmp = int(district_dict[x])
                                feature.append(tmp)
                            except:
                                feature.append(0)
                        else:
                            feature.append(0)
                # 视频类型标签(包括视频大类和子类)
                video_type_dict, video_sub_type_dict = self.get_user_videotype(user_profile[9])
                for i in range(14):
                    if video_type_dict is None:
                        feature.append(0)
                    else:
                        if (video_type_dict.get(i) is None):
                            feature.append(0)
                        else:
                            try:
                                tmp = int(video_type_dict.get(i))
                                feature.append(tmp)
                            except:
                                feature.append(0)
                for x in video_type_list:
                    if video_sub_type_dict is None:
                        feature.append(0)
                    else:
                        if video_sub_type_dict.get(x) is None:
                            feature.append(0)
                        else:
                            try:
                                tmp = int(video_sub_type_dict.get(x))
                                feature.append(tmp)
                            except:
                                feature.append(0)
                # 导演
                director_dict = self.get_user_director(user_profile[10])
                if director_dict is None:
                    for x in director_list:
                        feature.append(0)
                else:
                    for x in director_list:
                        if x in director_dict.keys():
                            try:
                                tmp = int(director_dict[x])
                                feature.append(tmp)
                            except:
                                feature.append(0)
                        else:
                            feature.append(0)
                # 演员
                actor_dict = self.get_user_actor(user_profile[11])
                if actor_dict is None:
                    for x in actor_list:
                        feature.append(0)
                else:
                    for x in actor_list:
                        if x in actor_dict.keys():
                            try:
                                tmp = int(actor_dict[x])
                                feature.append(tmp)
                            except:
                                feature.append(0)
                        else:
                            feature.append(0)
                # 性别，年龄，学历
                if (user_profile[13] == 'NULL'):
                    feature.append(0)
                else:
                    try:
                        tmp = int(user_profile[13])
                        feature.append(tmp)
                    except:
                        feature.append(0)

                if (user_profile[14] == 'NULL'):
                    feature.append(0)
                else:
                    try:
                        tmp = int(user_profile[14])
                        feature.append(tmp)
                    except:
                        feature.append(0)
                if (user_profile[15] == 'NULL'):
                    feature.append(0)
                else:
                    try:
                        tmp = int(user_profile[15])
                        feature.append(tmp)
                    except:
                        feature.append(0)
                feature.append(user_profile[0])
                user_mat.append(feature)
            #print(len(user_mat[0]))
        # for x in user_mat:
        #     print(x)
        return  user_mat

    def getUsers(self,k):
        with open(r'F:\selected_user4.txt',encoding='utf-8',errors='ignore') as user_profile:
            user_data = []
            for line in user_profile.readlines():
                user_data.append(line)
            user_list = self.RandomSampling(user_data,k)
            #user_list = user_data
            return  self.getUserMat(user_list)



