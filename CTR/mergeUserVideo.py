with open(r'F:\video_click_data2\video_watch_data.txt') as fr:
    user_video_dict = dict()
    for line in fr:
        user_video = line.split()
        if(len(user_video) == 5 and user_video[2]!='NULL' and user_video[3]!='NULL' and user_video[4]!='NULL'):
            str_key = user_video[2]+','+user_video[3] ;
            if user_video_dict.get(str_key) is None:
                user_video_dict[str_key] = int(user_video[4])

            else:
                user_video_dict[str_key] = user_video_dict.get(str_key) + float(user_video[4])

    with open('merged_user_video_watch_data.txt','w',encoding='utf-8') as fw:
        for key in user_video_dict:
            uid , vid = key.split(',')
            value=  user_video_dict.get(key)
            fw.write(uid+"\t"+vid+"\t"+ str(value)+"\n")

