#抽取视频特征

class Video(object):
    def get_videotype(self,video):
        video_list = video.split('|')
        return video_list

    def read_some_file(self,file):
        _list = []
        with open(file, encoding='utf-8') as fr:
            for line in fr:
                _list.append(line[0:-1])
        return _list

    def get_video_director(self,director):
        return director.split('|')

    def get_video_actor(self,actor):
        return actor.split('|')
    def getVideo(self):
        video_type_list = self.read_some_file(r'F:\tencent\video_type.txt')
        director_list = self.read_some_file(r'F:\tencent\director.txt')
        actor_list = self.read_some_file(r'F:\tencent\actor.txt')
        district_list = self.read_some_file(r'F:\tencent\districts.txt')
        video_actor_dict = dict()
        video_director_dict = dict()
        video_sub_type_dict = dict()
        video_type_dict = dict()
        video_district_dict = dict()
        video_year_dict = dict()
        with open(r'D:\实验结果\推荐\大于30\电视剧.txt', encoding='utf-8', errors='ignore') as video_info:
            video_mat = []

            for line in video_info.readlines():
                ############################
                video_actor = []
                video_director = []
                video_sub_type = []
                video_year = 2016
                ############################

                video_info=line.split('\t')
                if(len(video_info) == 8):
                    feature = []

                    # 视频大类类型
                    video_type = 9999
                    if (video_info[2] == 'NULL'):
                        feature.append(0)
                    else:
                        try:
                            tmp = int(video_info[2])
                            video_type=tmp
                            feature.append(tmp)
                        except:
                            feature.append(0)
                    # 视频子类型
                    v_video_type_list = self.get_videotype(video_info[3])
                    for x in video_type_list:
                        if x in v_video_type_list:
                            video_sub_type.append(1)
                            feature.append(1)
                        else:
                            video_sub_type.append(0)
                            feature.append(0)
                    # 导演
                    v_director_list = self.get_video_director(video_info[4])
                    for x in director_list:
                        if x in v_director_list:
                            video_director.append(1)
                            feature.append(1)
                        else:
                            video_director.append(0)
                            feature.append(0)
                    # 演员
                    v_actor_list = self.get_video_actor(video_info[5])
                    for x in actor_list:
                        if x in v_actor_list:
                            video_actor.append(1)
                            feature.append(1)
                        else:
                            video_actor.append(0)
                            feature.append(0)
                    # 上映年份
                    if (video_info[6] == 'NULL'):
                        feature.append(0)
                    else:
                        try:
                            tmp = int(video_info[6])
                            video_year=tmp
                            feature.append(tmp)
                        except:
                            feature.append(0)
                    # 地区
                    video_district = video_info[7][0:-1]
                    print(video_info[7][0:-1])
                    for x in district_list:
                        if x == video_info[7][0:-1]:
                            feature.append(1)
                        else:
                            feature.append(0)
                    feature.append(video_info[0])
                    video_mat.append(feature)
                    video_actor_dict[video_info[0]] = video_actor
                    video_director_dict[video_info[0]] = video_director
                    video_type_dict[video_info[0]] = video_type
                    video_sub_type_dict[video_info[0]] = video_sub_type
                    video_district_dict[video_info[0]] = video_district
                    video_year_dict[video_info[0]] = video_year
                   # print(len(video_mat[0]))
        # for x in video_mat:
        #     print(x)
        return video_mat,video_actor_dict,video_director_dict,video_type_dict,video_sub_type_dict,video_district_dict,video_year_dict