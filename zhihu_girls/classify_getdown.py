#coding=utf-8
'''
Created on 2016��11��18��

@author: yy
'''
import urllib.request, urllib.parse
import http.cookiejar
import re
import os
import socket


def openurl(opener,request):                  #opener.open异常
    try:
        response=opener.open(request)
    except Exception as e :
        print(type(e),e)
        openurl(request)
    return response

def get_col_num():
    file=open('collection.txt','r')
    collection=file.readlines()
    col_num=len(collection)
    return col_num

def get_dir_list():                                  #得到user dir信息
    file_list=os.listdir('.')
    dir_list=[]
    for i in file_list:
        if os.path.isdir(i):
            dir_list.append(i)
    return dir_list

def get_rename(dir_list):                       #得到重名文件夹字典
    rename={}
    for i in dir_list:
        if i[-4:] == '0828':
            t=i[:-4]
            rename[t]=i
    return(rename)

def get_uqa_str(i):
    my_path=os.path.join("collection","%d_col_qalist.txt"%i)
    file=open(my_path,'rb')
    uqa_str=file.readlines()
    return uqa_str

def new_dir(dirname):
    os.makedirs(dirname)
    my_path=os.path.join(dirname,"qa.txt")
    file=open(my_path,'wb')
    file.close
    print('%s 向您奔来!                                          \r'%dirname,end='' )
    

def get_cookie():
    LOGIN_URL = 'https://www.zhihu.com/login/phone_num'
    phone_num=input('输入手机号:')
    password=input('输入登陆密码:')
    values = {'phone_num': phone_num, 'password': password,'remember_me':'ture'}
    postdata = urllib.parse.urlencode(values).encode()
    user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    cookie_filename = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    request = urllib.request.Request(LOGIN_URL, postdata, headers)
    response = openurl(opener,request)
    page = response.read().decode()
    cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中

def get_url(url):
    user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    cookie_filename = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
    cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    request = urllib.request.Request(url,headers=headers)
    page = openurl(opener,request)
    html=page.read().decode()
    return html

def get_img(q,a):              #打开问题答案页面
    url3='https://www.zhihu.com'
    url4=url3+'/question/%s/answer/%s'%(q,a)
    html=get_url(url4)
    reg='data-original=\"([^_<]+?_r.jpg)\"'                         #此处可以改进,发现jpeg，png格式图片
    imgre=re.compile(reg)
    imglist=re.findall(imgre,html)
    return imglist

def get_all_img(imglist,all_imglist):                      #去重复,并生成图片文件列表,因内存使用过大没有使用
    for i in imglist:
        if not i in all_imglist:
            all_imglist.append(i)
    return all_imglist

def getdown_img(re_imglist,t,user,down_file):                    #下载图片文件到本地,并记录下载文件名
    i=1
    n=len(re_imglist)    
    for imgurl in re_imglist:
        print('           /%3d                                \r'%n,end='')
        s=os.path.join(user,"%s-%s.jpg"%(t,i))
        print("        %3d\r"%i,end='')
        fun(imgurl,s)
        down_file.append(s)
        i+=1
    print ('%s:%s Done                \r'%(user,t),end='')
    return down_file

def schedule(a,b,c):                            #下载进度
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print ('%6.2f%%\r' % per,end='')

def fun(imgurl,s):                                                  #循环出错下载
    try:
        socket.setdefaulttimeout(30)
        urllib.request.urlretrieve(imgurl, s,schedule)
    except Exception as e:
        print(type(e),e)
        fun(imgurl,s)

def show_update(all_down_file):                         #生成html更新文件
    file=open('update.html','w')
    html_1='''<html>
    <head>
    </head>
    <body>
    
    '''
    file.write(html_1)
    for i in all_down_file:
        s="<img src='%s' height='80%%' >"%i
        file.write(s)
        file.write('<p>%s</p>'%i)
    html_2='''
    </body>
    </html>
    '''
    file.write(html_2)
    file.close
    print('update.html 已生成！')
    
        
    
 


judge=input('是否拥有cookie(y or n):')            #主程序开始
if judge=='n':
    get_cookie()
judge=input('请将collection.txt放入文件夹!')
judge=input('请确认col_qalist.txt都已经全部生成!')
col_num=get_col_num()
print('收藏夹数目为:%d'%col_num)
all_down_file=[]
for i in range(1,col_num+1):                      #建立dir建立txt dirname=username  txt包含qa
    uqa_str=get_uqa_str(i)
    for j in uqa_str:
        s=':'
        s_b=s.encode()
        uqa=j.split(s_b)
        user_b=uqa[0]
        user=user_b.decode()
        qa=uqa[1]
        dir_list=get_dir_list()
        rename=get_rename(dir_list)
        if user not in dir_list:
            try:
                new_dir(user)
            except Exception as e :
                print(type(e),e)
                if user not in rename.keys():
                    user=user+'0828'                   #文件夹命名大小写不敏感，防重复
                    new_dir(user)
                else:
                    user=user+'0828'
        file_path=os.path.join(user,"qa.txt")
        file=open(file_path,'rb')
        qa_list=file.readlines()
        if qa not in qa_list:
            file.close
            qa_num=len(qa_list)+1
            s=' '
            s_b=s.encode()
            qa_s=qa.split(s_b)
            q=qa_s[0].decode()
            a=qa_s[1].decode()
            a=a[:-2]
            imglist=get_img(q, a)
            re_imglist=[]
            for t in imglist:
                if not t in re_imglist:
                    re_imglist.append(t)
            down_file=[]
            down_file=getdown_img(re_imglist,qa_num,user,down_file)
            file_path=os.path.join(user,"qa.txt")
            file=open(file_path,'ab')
            file.write(qa)
            file.close
        else:
            file.close
    print('第%d个收藏夹已完成                       '%i)    
show_update(all_down_file)
print('all done')
            




