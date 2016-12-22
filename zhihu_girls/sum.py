#coding=utf-8


import os

def get_dir_list():                                 #简单的统计一下爬取的文件
    file_list=os.listdir('.')
    dir_list=[]
    for i in file_list:
        if os.path.isdir(i):
            dir_list.append(i)
    return dir_list

def get_qa_num(dir):
    file=open('%s\\qa.txt'%dir,'rb')
    qa_list=file.readlines()
    qa_num=len(qa_list)
    return(qa_num)

def get_col_num():
    file=open('collection.txt','r')
    collection=file.readlines()
    collection.remove('\n')
    col_num=len(collection)
    return col_num

def get_uqa_str(i):
    file=open('%d_col_qalist.txt'%i,'rb')
    uqa_str=file.readlines()
    return uqa_str


col_sum=0
col_num=get_col_num()
for i in range(1,col_num+1):                      
    uqa_str=get_uqa_str(i)
    col_sum=len(uqa_str)+col_sum
qa_sum=0
dir_list=get_dir_list()
user_qanum={}
for dir in dir_list:
    qa_num=get_qa_num(dir)
    user_qanum[dir]=qa_num
    qa_sum=qa_sum+qa_num
user_qa_num= sorted(user_qanum.items(), key=lambda d:d[1], reverse = True)
file=open('sum.txt','wb')
s='收藏夹答案数：'+str(col_sum)+'\r\n'
file.write(s.encode())
s='下载答案数：'+str(qa_sum)+'\r\n'
file.write(s.encode())
for i in user_qa_num:
    s=i[0]+':'
    file.write(s.encode())
    s=str(i[1])
    file.write(s.encode())
    t='\r\n'
    file.write(t.encode())
file.close
print('Done!')
       
    
        
    
    
    
    
    
    
    
