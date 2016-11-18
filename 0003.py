#coding=utf-8
'''

第 0004 题：任一个英文的纯文本文件，统计其中的单词出现的个数。
@author: yy
'''
import re
filename=input('please enter filename:')
file=open(filename,'r')
str1=file.read()
file.close()
str1=str1.lower()
reobj=re.compile("\b?([a-zA-Z]+)\b?")
words=reobj.findall(str1)
word_dict={}
for word in words:
    if word in word_dict :
        word_dict[word]+=1
    else:
        word_dict[word]=1
file1=open('tongji.txt','w')
for(word,number) in word_dict.items():
    s=str(number)
    file1.write(word+':'+s+'\n')
file1.close
print('finish')       
