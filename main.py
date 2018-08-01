from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from os import listdir
from os.path import isfile, join
import os
import time
import argparse


#Default configs
case_sensitive = False
music_dir = "C:\\music"
formats = ('.mp3')
html_template = "template.html"
cols =  ('filename','title', 'artist', 'album','genre', 'length', 'bitrate')

class Song(object):
    def __init__(self, path,filename):
        if not os.path.exists(path):
            print(sys.stderr, "%s does not exist" % path)
        self.filename = path
        try:
            s = MP3(path,ID3=EasyID3)
        except:
            self.title = "" 
            self.artist = ""
            self.album = "" 
            self.length = 0
            self.genre = ""
            self.bitrate = ""
            return
            
        if(len(s['title']) >0):
           self.title = s['title'][0]
        if(len(s['artist']) >0):
            self.artist = s['artist'][0]
        if(len(s['album']) >0):
            self.album = s['album'][0]
        if(len(s['length']) >0):
            self.length = s['length'][0]
        if(len(s['genre']) >0):
            self.genre = s['genre'][0]
        else:
            self.genre = "" 
        self.bitrate =s.info.bitrate


##
##
##Handle argurments
##
##
def loadArgs():
    parser = argparse.ArgumentParser(description='Set music dir to process')
    parser.add_argument('--case-sensitive')
    parser.add_argument('music_dir')
    args = parser.parse_args()
    if args.case-sensitive is not None:
        case_sensitive = True
    if args.music_dir is not None:
        music_dir = args.launch_directory
##
##
## Misc
##
##
def toMinutes(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d" % (m, s)
##
##
## Digest data
##
##
def listFiles(): 
    result = []
    for root, dirs, files in os.walk(music_dir):
        for file in files:
            if file.endswith(formats):
                #print(root + "\\" + file)
                song = Song(root + "\\" + file,file)
                if(song == False): next
                #print(file)
                result.append(song)
    return result
def similarity(s1,s2):
    
def processData(songs):
    dups= []
    for s in songs:
        d = []
        count =0
        for x in songs:
            if(s.title == x.title):
                count +=1
                if(count >1):
                    d.append(s)
                          
        if(len(d) > 0):
            dups.append(d)
    return dups
def generateHtmlReport(songList):
    html_text = open(html_template, 'r').read()
    header = "<tr>"
    body =""
    #add table header
    for c in cols:
        header += "<th scope=\"col\">{0}</th>".format(c)
    header +="</tr>"
    switch_color = False
    for songs in songList:
        for d in songs:
            if(switch_color):
                body +="<tr bgcolor=\"#fff\">"
            else:
                body +="<tr bgcolor=\"#f8f8f8\">"
            body += "<td>{0}</td>".format(d.filename)
            body += "<td>{0}</td>".format(d.title)
            body += "<td>{0}</td>".format(d.artist)
            body += "<td>{0}</td>".format(d.album)
            body += "<td>{0}</td>".format(d.genre)
            body += "<td>{0}</td>".format(toMinutes(int(d.length)))
            body += "<td>{0}kbps</td>".format(int(int(d.bitrate) /1000))
            body += "</tr>"
        switch_color =not switch_color
    html_text = html_text.format(header,body)
    with open("report.html", "w", encoding='utf-8') as html_file:
        html_file.write(html_text)
##
##
## c
##
##
if __name__ == "__main__":
    #loadArgs()
    start_time = time.time()  
    all_songs = listFiles()
    
    generateHtmlReport(processData(all_songs))
   # print(temp)
    print("Process time: %s seconds " % (time.time() - start_time))
 
    
