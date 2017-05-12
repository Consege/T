def Generator_File(file_in1,file_in2):
    try:
        all_user_file=open(r'F:\video_click_data2\user_profile.txt',encoding='gbk',errors='ignore')
        all_video_file=open(r'F:\video_click_data2\video_info.txt',encoding='gbk',errors='ignore')
        user_file=open(file_in1,encoding='utf-8',errors='ignore')
        video_file=open(file_in2,encoding='utf-8',errors='ignore')
        selected_user=open(r'D:\实验结果\推荐\大于20\大于20_user.txt','w',encoding='utf8')
        selected_video=open(r'D:\实验结果\推荐\大于20\videos_none.txt','w',encoding='utf8')
        user_set=set()
        video_set=set()
        for line in user_file:
            user_set.add(line[0:len(line)-1])
        for line in video_file:
            #print(line)
            video_set.add(line[0:len(line)-1])
        for line in all_user_file:
            uid, active_days, browser, cpu, memory, other_browser, other_safe, interest, v_district, v_type, director, actor, mobile, gender, age, education = line.split(
                '\t')
            for user in user_set:
                #print(user,uid)
                if user==uid:
                    selected_user.write(line)
                    break
        for line in all_video_file:
            vid,vname,vtype,vsubtype,director,actor,time,district=line.split('\t')
            for video in video_set:
                if video==vid:
                   # print(video,vid)
                    selected_video.write(line)
                    break

    finally:
        all_user_file.close()
        all_video_file.close()
        user_file.close()
        video_file.close()
        selected_user.close()
        selected_video.close()



if __name__=='__main__':
    Generator_File(r'F:\tencent\findtop1000\main\top_500_users.txt',r'F:\tencent\findtop1000\main\vid3.txt')