with open(r'D:\tencentvideos\交叉特征\电视剧推荐\videos2.txt','w',encoding='utf-8') as fw:
    with open(r'F:\selected_videos5.txt',encoding='utf-8') as fr:
        for line in fr:
            data_detail = line.split('\t')
            if(data_detail[2] == '2'):
                fw.write(line)