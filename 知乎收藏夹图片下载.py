#coding=utf-8
'''
Created on 2016��11��18��

@author: yy
'''
import urllib.request
import re

def get_url(url):
    page =urllib.request.urlopen(url)
    html=page.read()
    html=html.decode('UTF-8')
    page.close()
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
    reg='src=\"([^\"]+?_b.jpg)\"'                         #此处可以改进,而且正则表达式可能有点问题,会漏抓,还有其他形式的图片如png
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




    
    
    
    
    
    
    
    

