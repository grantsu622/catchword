import urllib2
import urllib
import re
import codecs
import sys

'''
argv[1]:source file
argv[2]:destination file
'''
#f = open('b.txt', 'r')
f = open(sys.argv[1], 'r')
#fw = open('c.txt', 'w')
#fw = codecs.open('c.txt', 'w', 'utf-8')
fw = codecs.open(sys.argv[2], 'w', 'utf-8')

'''
Parse word
'''

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
        for i in self.IDlist:  
            print i.decode('utf-8') 
            #fw.write(i.deconde('utf-8'))
            i1 = unicode(i, 'utf-8')
            fw.write(i1)
            fw.write('\n')
            #return i.decode('utf-8')
            

while True :
    i = f.readline()
    if i=='': break
    print i
    print len(i)
    
    fw.write(i)
    
    url = 'https://tw.dictionary.yahoo.com/dictionary?p=' + i
    content = urllib2.urlopen(url).read()
    
    '''
    download MP3 file
    '''
    urls = re.findall('http[s]?://s.yimg.com/tn/dict/dreye/live/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+.mp3', content)
    try:
        print urls[0]
    except IndexError:
        continue
    urllib.urlretrieve(urls[0], i[0:len(i)-1] + ".mp3")
    
    explanation = GetIdList()
    explanation.feed(content)
    #fistexplanation = explanation.printID()
    explanation.printID()
    fw.write('\n')
    #print fistexplanation
    
f.close()
fw.close()