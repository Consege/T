def readFile(file):
    with open('valid_watch_data.txt','w',encoding='utf-8') as fw:
        with open(file,encoding='gbk',errors='ignore') as fr:
            for line in fr:
                user_watch = line.split()
                #简单处理 ：观看时长超过5分钟认为是有效的观看记录
                watch_time_str=user_watch[-1]
                try:
                    watch_time = int(watch_time_str)
                    if(watch_time>=300000):
                        fw.write(line)
                except:
                    pass
if __name__ == '__main__':
    readFile(r'F:\video_click_data2\video_watch_data.txt')