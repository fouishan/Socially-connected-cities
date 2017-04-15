
# coding: utf-8

# In[1]:

#https://stackoverflow.com/questions/18130499/how-to-scrape-instagram-with-beautifulsoup
#for maco sx, download chrome driver - https://sites.google.com/a/chromium.org/chromedriver/downloads


# In[22]:

import re
import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import csv


# In[23]:

def readCSV (file):
    df = pd.read_csv(file)
    return df


# In[24]:



#URL = 'https://www.instagram.com/explore/tags/chapelhill/?hl=en' #hoboken location

def instaURL (URL):
    driver = webdriver.Chrome('/Users/fouis/Downloads/chromedriver_win32/chromedriver')  # Optional argument, if not specified will search path.
    driver.get(URL);
    time.sleep(1) # Let the user actually see something!
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Click on "Load more..." label
    load_more = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/a')
    load_more.click()
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source)
    time.sleep(5) # Let the user actually see something!
    driver.quit()
    
    #isolate the owner IDs from the pictures
    stringTest=""
    for x in soup:
        stringTest = stringTest + str(x)
        #print x
    pic_pattern='''(?<="owner").*?(?="owner")'''
    pic = re.findall(pic_pattern, stringTest)
    output = pic
    #print output
    return output


# In[25]:

def formatHashtag(hashtag):
    
    outputTag=""
    hashtagDict = []
    #print hashtag
    listRange = range(len(hashtag))
    for i in listRange:
        iterator = i
        for x in hashtag[(i+1):]:
            outputTag+=hashtag[i]+ "," + (x) + "\n"
    #print outputTag
    return outputTag


# In[26]:

def parse(Source, City):
    hashtagout=""
    df = pd.DataFrame()
    CityFileName = str('InstaOutputMain_'+City+'.csv')
    CityFileListName = str('InstaOutputlist_'+City+'.csv')
    ofile  = open(CityFileName, "w")
    ofile.write("date" + "," + "pictureURL" +","+ "numLikes" +","+ "City" + "," + "hashtagout" + "\n")
    #ofile_list  = open(CityFileListName, "wb") create
    ofile_list  = open(CityFileListName, "a+") #append
    ofile_list.write("tag1" + "," + "tag2"+ "\n")
    for test in Source:  
        ownerID_pattern='''(?<=: {"id": ").*?(?="},)'''
        ownerID = re.search(ownerID_pattern, test)
        ownerID = ownerID.group(0)
        #print ownerID

        video_pattern='''(?<="is_video": ).*?(?=,)'''
        video = re.search(video_pattern, test)
        if video: video = video.group(0)
        else: video="N/A"

        pictureURL_pattern='''(?<="display_src": ").*?(?="},)'''
        pictureURL = re.search(pictureURL_pattern, test)
        if pictureURL: pictureURL = pictureURL.group(0)
        else: pictureURL="N/A"

        date_pattern='''(?<="date": ).*?(?=,)'''
        date = re.search(date_pattern, test)
        date = date.group(0)
        date = datetime.datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S')

        commentsCount_pattern='''(?<="comments": {"count": ).*?(?=},)'''
        commentsCount = re.search(commentsCount_pattern, test)
        numComments = commentsCount.group(0)

        numLikes="N/A"
        likesCount_pattern='''(?<="likes": {"count": ).*?(?=},)'''
        likesCount = re.search(likesCount_pattern, test)
        numLikes = likesCount.group(0)

        caption_pattern='''(?<="caption": ").*?(?=, "likes":)'''
        caption = re.search(caption_pattern, test)
        hashtagtext="N/A"
        if caption:
            hashtagtext = caption.group(0)

        hashtag = "N/A"
        hashtag_pattern='''(?<=#).*?(?=\W)'''
        hashtag = re.findall(hashtag_pattern, hashtagtext)

        
        #print hashtag
        df = df.append({ 'ownerID': ownerID,
                           'isVideo': video,
                           'pictureURL': pictureURL,
                           'date': date,
                           'numComments': numComments,
                           'numLikes': numLikes,
                           'caption': hashtagtext,
                        'hashtag': hashtag
            }, ignore_index=True)
        #additional data cleanup
        cols = df.columns.tolist()
        cols = ['caption',
         'date',
         'isVideo',
         'numComments',
         'numLikes', 'pictureURL', 'ownerID','hashtag']
        df=df[cols]

        #print hashtag
        
        
        formatHashtag(hashtag)
        ofile_list.write(formatHashtag(hashtag))

        hashtagout=""
        for x in hashtag:
            hashtagout += x + "\t"
            
        
        ofile.write(date + "\t" + pictureURL +"\t"+ numLikes +"\t"+ City + "\t" + hashtagout + "\n")

    return "Check InstaOutput.txt file for output"
    


# In[27]:

def getCities(df):
    for index, row in df.iterrows():
        URL= row['Link']
        City = row['City']
        output=instaURL(URL)
        parse(output,City)


# In[28]:

file = '/Users/fouis/Downloads/Socially-connected-cities-master/Socially-connected-cities-master/Data/Cities List.csv'
df = readCSV(file)
#df['Link'][1]
getCities(df)


# In[52]:

#output=instaURL(URL)


# In[53]:

#parse(output)


# In[ ]:



