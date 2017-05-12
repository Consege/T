import numpy as np
from sklearn.decomposition import NMF
if __name__ == "__main__":
    #加载selected_users
    selected_users = []
    with open(r'D:\实验结果\推荐\大于20\大于20_user.txt',encoding='utf-8') as fr:
        for line in fr:
            user_profile= line.split('\t')
            selected_users.append(user_profile[0])
    #加载selected_videos
    selected_videos = []
    user_video_matrix=[]
    with open(r'D:\tencentvideos\交叉特征\电影推荐\videos.txt',encoding = 'utf-8') as fr:
        for line in fr:
            video_info = line.split('\t')
            selected_videos.append(video_info[0])

    user_video_watched_duration_dict = dict()
    with open(r'F:\merged_user_video_watch_data.txt') as fr:
        for line in fr:
            user_watched=line.split('\t')
            if user_video_watched_duration_dict.get(user_watched[0]+user_watched[1]) is None:
                user_video_watched_duration_dict[user_watched[0]+user_watched[1]] = float(user_watched[2])
            else:
                user_video_watched_duration_dict[user_watched[0]+user_watched[1]] = user_video_watched_duration_dict.get(user_watched[0]+user_watched[1])+float(user_watched[2])

    #产生用户-视频矩阵，元素为 用户观看视频时长
    for user in selected_users:
        matrix_line = []
        for video in selected_videos:
            if user_video_watched_duration_dict.get(user+video) is None:
                matrix_line.append(0)
            else:
                matrix_line.append(user_video_watched_duration_dict.get(user+video))
        user_video_matrix.append(matrix_line)

    ##############
    with open('origin_matrix.txt','w',encoding='utf-8') as fw:
        for line in user_video_matrix:
            for x in line:
                fw.write(str(x)+',')
            fw.write('\n')
    #############
    #矩阵分解
    K = 60
    nmf = NMF(n_components=K,init='nndsvd',tol=0.0000000099,max_iter=10000,shuffle = True,verbose=True)
    nP= nmf.fit_transform(np.array(user_video_matrix))
    nQ = nmf.components_

    print(nmf.reconstruction_err_)
    mul_matrix = nmf.inverse_transform(nP)

    ##############
    with open('post_matrix.txt', 'w', encoding='utf-8') as fw:
        for line in mul_matrix:
            for x in line:
                fw.write(str(x) + ',')
            fw.write('\n')
    #############

    ###########
    with open(r'D:\实验结果\推荐\大于20\user_matrix.txt','w',encoding='utf-8') as fw:
        for line in nP:
            count = 0
            for x in line:
                fw.write(str(x))
                if count != len(line) -1:
                    fw.write(',')
                count+=1
            fw.write('\n')
    ###########
    print(np.array(nP).shape)
    ###########
    with open(r'D:\实验结果\推荐\大于20\video_matrix.txt', 'w', encoding='utf-8') as fw:
        for line in nQ:
            count = 0
            for x in line:
                fw.write(str(x))
                if count != len(line) - 1:
                    fw.write(',')
                count += 1
            fw.write('\n')
    ###########
    print(np.array(nQ).shape)








