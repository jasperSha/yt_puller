#!/usr/bin/env python
from __future__ import unicode_literals
import pandas as pd
import youtube_dl
import webvtt
import re

def pull_url():
    '''
    Downloads youtube URL in .wav format.
    Provides option to download captions as well. 
    '''
    youtube_url = input("Enter youtube url\n")
    filename = input("Enter the name of the file: ")
    subs = input("Would you like to download the captions as well? (y/n)\n")

    ydl_opts = { 'format': 'bestaudio/best',
                 'postprocessors': [{
                     'key': 'FFmpegExtractAudio',
                     'preferredcodec': 'wav',
                     'preferredquality': '192',
                     }],
                 }
    ydl_opts['outtmpl'] = unicode(filename)
    if (subs == 'y' or subs == 'Y'):
        ydl_opts['writesubtitles'] = True

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def read_vtt():
    '''
    Parses caption file generated from youtube-dl download.
    Writes to a csv with the header: ['start_time', 'end_time', 'words']
    Words are each caption segment, and have been stripped of non alphanumeric characters
    '''
    vtt = input("Enter the caption filename (vtt format) please:\n")
    start, end, text = [], [], []
    emptystring = ''
    for caption in webvtt.read(vtt):
        start.append(caption.start)
        end.append(caption.end)
        parsed_words = [re.sub(r'\W+', '', word.lower()) for word in caption.text.split()]
        while emptystring in parsed_words: parsed_words.remove(emptystring)
        text.append(parsed_words)
    
    data = list(zip(start, end, text))
    cols = ['start_time', 'end_time', 'words']
    
    caption_log = pd.DataFrame(data = data, columns=cols)
    
    filename = input("Enter name of parsed file: ")
    directory = input("Enter folder name: ")
    caption_log.to_csv('%s/%s.csv'%(directory, filename), index=False)

def parse_log():
    '''
    Opens caption csv file
    '''
    folder = input("Enter relative folder directory: ")
    log = input("Enter file.csv: ")
    log = '%s/'%folder + log
    df = pd.read_csv(log)
    print(df.head())

if __name__ == '__main__':
    user = input("\n(D)ownload Youtube Video?\n(R)ead caption file?\n(P)arse (open) caption log? \n")

    options = { 'd' : pull_url,
                'r' : read_vtt,
                'p' : parse_log
                }

    options[user.lower()]()
        
    

