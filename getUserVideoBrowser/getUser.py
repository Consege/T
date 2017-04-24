def deal_user_interest(interest):
    interestes = interest.split('#')
    user_interest_list=[]
    for x in interestes:
        real_interest = x.split('|')
        if real_interest[0] is not None and len(real_interest)==2:
            user_interest_list.append(real_interest[0])
    return user_interest_list

def deal_district(district):
    district_list=[]
    districts = district.split('#')
    for x in districts:
        real_district=  x.split('%')
        if real_district[0] is not None:
            district_list.append(real_district[0])
    return  district_list

def deal_video_type(video_type):
    video_type_list = []
    video_types = video_type.split('#')
    for x in video_types:
        real_video_type = x.split('%')
        #[0]为视频大类，[1]为视频子类
        if real_video_type is not None:
            subtype = real_video_type[0].split('@')
            if len(subtype)>1:
                video_type_list.append(subtype[1])
    return  video_type_list

def deal_director(director):
    director_list = []
    directors = director.split('#')
    for x in directors:
        real_director = x.split('%')
        if real_director[0] is not None:
            director_list.append(real_director[0])
    return  director_list

def deal_actor(actor):
    actors = actor.split('#')
    actor_list = []
    for x in actors:
        real_actor = x.split('%')
        if real_actor[0] is not None:
            actor_list.append(real_actor[0])
    return  actor_list

# def writeSet(file,data_set):
#     with open(file,'w',encoding='utf-8') as fw:
#         for x in data_set:
#             fw.write(str(x)+'\n')

def writeDict(file,_dict):
    #提取前100的特征
    _list =sorted(_dict.items(),key=lambda x:x[1],reverse = True)
    with open(file,'w',encoding='utf-8') as fw:
        count = 0
        for x ,value in _list:
            count=count+1
            if(count==101):
                break
            if(x == 'null'):
                continue
            fw.write(str(x)+'\n')
def readFile(file):
    browser_set=set()
    browser_dict=dict()
    #用户大类兴趣标签集合
    user_interest_set = set()
    user_interest_dict = dict()
    #视频地区标签集合
    district_set = set()
    district_dict = dict()
    #视频类型集合
    video_type_set = set()
    video_type_dict = dict()
    #导演集合
    director_set = set()
    director_dict = dict()
    #演员集合
    actor_set = set()
    actor_dict = dict()

    #从原始文件中提取特征，用dict保存每个特征出现的次数
    with open(file,encoding='gbk',errors='ignore') as fr:
        for line in fr:
            user_profile = line.split()
            user_len = len(user_profile)
            if user_len == 16:
                browser = user_profile[2].split('\\')[-1].lower()
                if(browser_dict.get(browser) is None):
                    browser_dict[browser] = 1
                else:
                    browser_dict[browser] = browser_dict.get(browser) + 1
                # if(browser!= 'NULL' and browser_dict.get(browser)>100):
                #     browser_set.add(browser)

                if(user_profile[7]!='NULL'):
                    user_interest_list = deal_user_interest(user_profile[7])
                    for x in user_interest_list:
                        if(user_interest_dict.get(x) is None):
                            user_interest_dict[x] = 1
                        else:
                            user_interest_dict[x]=user_interest_dict.get(x)+1
                        # if(x != 'NULL' and user_interest_dict.get(x)>100):
                        #      user_interest_set.add(x)

                if(user_profile[8]!='NULL'):
                    district_list = deal_district(user_profile[8])
                    for x in district_list:
                        if(district_dict.get(x) is  None):
                            district_dict[x] = 1
                        else:
                            district_dict[x] = district_dict.get(x) + 1
                        # if(x != 'NULL' and district_dict[x]>100):
                        #     district_set.add(x)

                if(user_profile[9]!='NULL'):
                    video_type_list = deal_video_type(user_profile[9])
                    for x in video_type_list:
                        if video_type_dict.get(x) is None:
                            video_type_dict[x] =  1
                        else:
                            video_type_dict[x] = video_type_dict.get(x) + 1
                        # if(x != 'NULL' and video_type_dict.get(x) > 100):
                        #     video_type_set.add(x)

                if(user_profile[10]!='NULL'):
                    director_list = deal_director(user_profile[10])
                    for x in director_list:
                        if director_dict.get(x) is None:
                            director_dict[x] = 1
                        else:
                            director_dict[x] = director_dict.get(x) + 1
                        # if(x != 'NULL' and director_dict.get(x)>100):
                        #     director_set.add(x)

                if(user_profile[11] !='NULL'):
                    actor_list = deal_actor(user_profile[11])
                    for x in actor_list:
                        if actor_dict.get(x) is None:
                            actor_dict[x] = 1
                        else:
                            actor_dict[x] = actor_dict.get(x) + 1
                        # if(x != 'NULL' and actor_dict[x] > 100):
                        #     actor_set.add(x)
    # writeSet(r'F:\tencent\getUserVideoBrowser\browser.txt',browser_set)
    # writeSet(r'F:\tencent\getUserVideoBrowser\user_interest.txt', user_interest_set)
    # writeSet(r'F:\tencent\getUserVideoBrowser\districts.txt', district_set)
    # writeSet(r'F:\tencent\getUserVideoBrowser\video_type.txt', video_type_set)
    # writeSet(r'F:\tencent\getUserVideoBrowser\director.txt', director_set)
    # writeSet(r'F:\tencent\getUserVideoBrowser\actor.txt', actor_set)

    #提取出前100的兴趣\地区\等 写入文件中
    writeDict(r'F:\tencent\getUserVideoBrowser\browser.txt',browser_dict)
    writeDict(r'F:\tencent\getUserVideoBrowser\user_interest.txt', user_interest_dict)
    writeDict(r'F:\tencent\getUserVideoBrowser\districts.txt', district_dict)
    writeDict(r'F:\tencent\getUserVideoBrowser\video_type.txt', video_type_dict)
    writeDict(r'F:\tencent\getUserVideoBrowser\director.txt', director_dict)
    writeDict(r'F:\tencent\getUserVideoBrowser\actor.txt', actor_dict)
if __name__=="__main__":
    readFile(r'F:\video_click_data2\user_profile.txt')