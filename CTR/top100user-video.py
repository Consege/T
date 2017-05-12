#筛选出前1000的用户和视频
def GeneratorFile(file_in):
    ufw=open('top_500_users.txt','w',encoding='utf8')
    vfw=open('top_500_videos.txt','w',encoding='utf8')
    try:
        video_watch_data=open(file_in,encoding = 'gbk',errors='ignore')
        user_info = open(r'F:\video_click_data2\user_profile.txt',encoding='gbk',errors='ignore')
        video_info= open(r'F:\video_click_data2\video_info.txt',encoding = 'gbk',errors='ignore')

        count=1
        number_of_uid={}
        number_of_vid={}
        for line in video_watch_data:
            try:
                uid,vid,long=line.split()
                #print(hour,minute,uid,vid,long)
                if number_of_uid.get(uid) is None:
                    number_of_uid[uid] =1
                else:
                    number_of_uid[uid] = number_of_uid.get(uid)+1
                if number_of_vid.get(vid) is None:
                    number_of_vid[vid]=1
                else:
                    number_of_vid[vid] = number_of_vid.get(vid)+1
            except:
                print('split error 1')

        uid_list=sorted(number_of_uid.items(),key=lambda x:x[1],reverse = True)
        vid_list=sorted(number_of_vid.items(),key=lambda x:x[1],reverse = True)
        selected_uid_list=[]
        selected_vid_list=[]
        count=0
        for index ,value in uid_list:
            if count >= 500:
                break
            count = count + 1
            selected_uid_list.append(index)
        count = 0
        for index,value in vid_list:
            if count >= 500:
                break
            count = count + 1
            selected_vid_list.append(index)
        print(len(selected_uid_list))
        vid_set = set()


        for index in selected_uid_list:
            ufw.write(index+'\n')
            count = 0
            print(count)
            with open(r'D:\tencentvideos\merged_user_video_watch_data.txt',encoding='utf-8') as fr:
                for line in fr:
                    user_video = line.split()
                    #print(index,user_video[0])
                    if len(user_video)==3:
                        if count == 0:
                            print("dsfasdf",index,user_video)

                        count = 1
                        #print(index,user_video[0])
                        if index == user_video[0]:
                            #print(index,user_video)
                            vid_set.add(user_video[1])
        with open(r"vid5.txt", 'w', encoding='utf-8') as fw:
            for index in vid_set:
                fw.write(index+'\n')

        for index in selected_vid_list:
            vfw.write(index+'\n')
        #print(number_of_vid.get('5827269'))
    finally:
        ufw.close()
        vfw.close()


if __name__ == '__main__':
    GeneratorFile(r'D:\tencentvideos\merged_user_video_watch_data.txt')

