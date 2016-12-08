#coding=utf-8
'''
Created on 2016��11��18��

@author: yy
'''
import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import re

def get_cookie():                                                           #新增cookie抓取,因为有些答案不登陆无法访问
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
    response = opener.open(request)
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
    page = opener.open(request)
    html=page.read().decode()
    return html

def get_page(html):
    reg='\"\?page=([0-9]+)\"'    #知乎收藏夹页面属性
    page=re.compile(reg)
    pagelist=re.findall(page,html)
    pagenumber=int(pagelist[-2])
    return pagenumber


def get_qa(html):
    reg2=r'href="/question/([0-9]+)/answer/([0-9]+)"'     #知乎网址格式/question/题目号/answer/答案号
    qa=re.compile(reg2)
    qalist=re.findall(qa,html)
    return qalist


def get_all_qa(qalist,all_qalist):     #去重复,并最终生成收藏问题列表
    for i in qalist:
        if not i in all_qalist:
            all_qalist.append(i)
    return all_qalist


def get_img(one_qa):              #打开问题答案页面
    url3='https://www.zhihu.com'
    url4=url3+'/question/%s/answer/%s'%(one_qa[0],one_qa[1])
    html=get_url(url4)
    reg='data-original=\"([^_]+?_r.jpg)\"'                         #知乎网站代码更新了,原来的正则修改了
    imgre=re.compile(reg)
    imglist=re.findall(imgre,html)
    return imglist


def get_all_img(imglist,all_imglist):                      #去重复,并生成图片文件列表,因内存使用过大没有使用
    for i in imglist:
        if not i in all_imglist:
            all_imglist.append(i)
    return all_imglist


def getdown_img(re_imglist,t):                    #下载图片文件到本地
    i=1
    for imgurl in re_imglist:
        urllib.request.urlretrieve(imgurl, '%s-%s.jpg'%(t,i))
        i+=1
    print ('%s Done'%t)

    
judge=input('是否拥有cookie(y or n):')
if judge=='n':
    get_cookie()
url=input('请输入url:(友情提示一会还要输入一次题号)')                                    #主程序开始
html=get_url(url)
pagenumber=get_page(html)
qalist=get_qa(html)
all_qalist=[]
all_qalist=get_all_qa(qalist,all_qalist)
for i in range(2,pagenumber+1):
    url2=url+'?page=%d'%i
    html=get_url(url2)
    qalist=get_qa(html)
    all_qalist=get_all_qa(qalist,all_qalist)
    print(len(all_qalist))
print('qalist done')
ts=input('请输入开始爬取的问题号从1开始:')                #网速不好总卡住,加入循环控制,可以断点重下
t=int(ts)
jianyi=t-1
for i in range(jianyi,len(all_qalist)):
    one_qa=all_qalist[i] 
    imglist=get_img(one_qa)
    re_imglist=[]
    for i in imglist:
        if not i in re_imglist:
            re_imglist.append(i)
    getdown_img(re_imglist,t)
    t+=1
print('all done')
input("Prease <enter>")                             #本意是想让程序运行完界面保留住,不过没测试过
    
    
    
    
    
    
    
    

