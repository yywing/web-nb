#coding=utf-8
'''
Created on 2016��11��18��
中国
@author: yy
'''

import urllib.request, urllib.parse
import http.cookiejar
import re

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
    reg2='data-author-name="([^"]+)" data-entry-url="/question/([0-9]+)/answer/([0-9]+)"'   #知乎网址格式/question/题目号/answer/答案号
    qa=re.compile(reg2)
    qalist=re.findall(qa,html)
    return qalist

def get_re_qa(qalist,re_qalist):     #去重复,并最终生成收藏问题列表
    for i in qalist:
        if not i in re_qalist:
            re_qalist.append(i)
    return re_qalist

def write_re_qalist(col_num,re_qalist):
    file=open('%d_col_qalist.txt'%col_num,'wb')
    for i in range(0,len(re_qalist)):
        wri_lin=re_qalist[i][0]+':'+re_qalist[i][1]+' '+re_qalist[i][2]+'\r\n'
        file.write(wri_lin.encode())
    file.close
    


judge=input('是否拥有cookie(y or n):')            #主程序开始
if judge=='n':
    get_cookie()
judge=input('请将collection.txt放入文件夹!')
file=open('collection.txt','r')
urllist=file.readlines()
file.close
col_num=1
for url in urllist:
    url=url[:-1]                                #去掉换行符
    html=get_url(url)
    pagenumber=get_page(html)
    qalist=get_qa(html)
    re_qalist=[]
    re_qalist=get_re_qa(qalist,re_qalist)
    for i in range(2,pagenumber+1):
        url2=url+'?page=%d'%i
        html=get_url(url2)
        qalist=get_qa(html)
        re_qalist=get_re_qa(qalist,re_qalist)
        print(len(re_qalist))
    write_re_qalist(col_num,re_qalist)
    print('%d collection qalist write'%col_num)
    col_num+=1
    #完成一个收藏夹的qa收集









    
    
