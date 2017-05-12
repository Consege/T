user_list = list()
user_video = list()
with open(r'D:\tencentvideos\交叉特征\train3_1.txt',encoding='utf-8') as fr:
    for line in fr:
        user_profile = line.split(',')
        if(user_profile[0] not in user_list):
            user_list.append(user_profile[0])
            user_video.append(line)

with open(r'D:\tencentvideos\交叉特征\train4_1.txt','w',encoding='utf-8') as fw:
    for line in user_video:
        fw.write(line)
