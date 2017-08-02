#-*- coding: cp950 -*-�@
#-*- coding: utf-8 -*-

import urllib2

import urllib
import re
import codecs
import sys
import os


"""
argv[1]:source file
argv[2]:destination file
"""
#�إߨӷ���Ƨ�
foldname = sys.argv[2][0:len(sys.argv[2])-4]
if not os.path.exists(foldname):
    os.makedirs(foldname)

#f = open('b.txt', 'r')
f = open(sys.argv[1], 'r')
#fw = open('c.txt', 'w')
#fw = codecs.open('c.txt', 'w', 'utf-8')
fw = codecs.open(foldname + "/00_" + sys.argv[2], 'w', 'utf-8')
flose = codecs.open(foldname + "/" + '00_lose.txt', 'w', 'utf-8')

#fdebug = codecs.open(foldname + "/" + '00_debug.txt', 'w', 'utf-8')

#Parse word ���ѳ�r
from sgmllib import SGMLParser  
class GetIdList(SGMLParser):  
    def reset(self):  
        self.IDlist = []  
        self.flag = False  
        self.getdata = False  
        SGMLParser.reset(self)  
          
    def start_li(self, attrs):  
        for k,v in attrs: 
            if k == 'class' and v == 'ov-a fstlst':
                self.flag = True
                #print(attrs)
                return  
  
    def end_li(self):
        self.flag = False  
              
    def start_h4(self, attrs):  
        if self.flag == False:  
            return
        self.getdata = True

    def end_h4(self):
        if self.getdata:  
            self.getdata = False  
  
    def handle_data(self, text):
        if self.getdata:  
            self.IDlist.append(text)  
    def printID(self):  
        i3=0
        for i in self.IDlist:  
        #if self.IDlist:
            #print i.decode('utf-8') 
            #fw.write(i.deconde('utf-8'))
            i1 = unicode(i, 'utf-8')
            fw.write(i1[3:])
            
            i3=i3 + 1
            #print i3
            #i2 = i1.split()
            #print self.IDlist
            #print i1[3:] #�C�L����
            #print i2[3:] #�C�L����
            fw.write('\n')
            #return i.decode('utf-8')
            if i3 == 1:
                return
            

#Parse word ���ѰʦW��
from sgmllib import SGMLParser  
class GetSpeechList(SGMLParser):  
    def reset(self):  
        self.IDlist = []  
        self.flag = False  
        self.getdata = False  
        SGMLParser.reset(self)  
          
    def start_div(self, attrs):  
        for k,v in attrs: 
            if k == 'class' and v == 'compTitle mb-10':
                self.flag = True
                #print(attrs)
                return  
  
    def end_div(self):
        self.flag = False  

    def start_h3(self, attrs):  
        if self.flag == False:  
            return
        self.getdata = True

    def end_h3(self):
        if self.getdata:  
            self.getdata = False  
    def handle_data(self, text):
        if self.getdata:  
            self.IDlist.append(text)  
    def printID(self):  
        i3=0
        for i in self.IDlist:  
        #if self.IDlist:
            #print i.decode('utf-8') 
            #fw.write(i.deconde('utf-8'))
            i3=i3 + 1
            if i3 == 1: 
                continue
            i1 = unicode(i, 'utf-8')
            i2 = i1.split('.')
            #print i2[0]
            fw.write(i2[0])
            
            #print i3
            #i2 = i1.split()
            #print self.IDlist
            #print i1 #�C�L����
            #print i2[3:] #�C�L����
            fw.write(',')
            #return i.decode('utf-8')
            if i3 == 2:
                return
            
while True :
    i = f.readline()
    if i=='': break
    print i[0:len(i)-1]
    #print len(i)
    
    
    url = 'https://tw.dictionary.yahoo.com/dictionary?p=' + i
    content = urllib2.urlopen(url).read()
    
    '''
    download MP3 file
    '''
    urls = re.findall('http[s]?://s.yimg.com/tn/dict/dreye/live/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+.mp3', content)
    try:
        #print urls[0]
        len(urls[0])
    except IndexError:
        flose.write(i)
        continue
    
    
    #print content
    #fdebug.write(content)
    
    urllib.urlretrieve(urls[0], foldname + "/" + i[0:len(i)-1] + ".mp3")
    
    fw.write(i[0:len(i)-1] + " ")  #�g�J�^���r
    ######
    explanation = GetSpeechList()
    explanation.feed(content)
    explanation.printID()   #�g�J����
    
    ######
    explanation = GetIdList()
    explanation.feed(content)
    #fistexplanation = explanation.printID()
    explanation.printID() #�g�J����
    #fw.write('\n')
    #print fistexplanation


f.close()
fw.close()
flose.close()

#fdebug.close()
