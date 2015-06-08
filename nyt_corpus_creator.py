from bs4 import BeautifulSoup
from nytimesarticle import articleAPI
import csv
import sys
import os
import requests

def parse_articles(articles):
    '''
    This function takes in a response to the NYT api and parses
    the articles into a list of dictionaries
    '''
    news = []
    for i in articles['response']['docs']:
        dic = {}
        dic['id'] = i['_id']
        if i['abstract'] is not None:
            dic['abstract'] = i['abstract'].encode("utf8")
        dic['headline'] = i['headline']['main'].encode("utf8")
        dic['desk'] = i['news_desk']
        dic['date'] = i['pub_date'][0:10] # cutting time of day.
        dic['section'] = i['section_name']
        if i['snippet'] is not None:
            dic['snippet'] = i['snippet'].encode("utf8")
        dic['source'] = i['source']
        dic['type'] = i['type_of_material']
        dic['url'] = i['web_url']
        dic['word_count'] = i['word_count']
        # locations
        locations = []
        for x in range(0,len(i['keywords'])):
            if 'glocations' in i['keywords'][x]['name']:
                locations.append(i['keywords'][x]['value'])
        dic['locations'] = locations
        # subject
        subjects = []
        for x in range(0,len(i['keywords'])):
            if 'subject' in i['keywords'][x]['name']:
                subjects.append(i['keywords'][x]['value'])
        dic['subjects'] = subjects   
        news.append(dic)
    return(news) 

def mkdir_nyt(path):
    path = "/Users/camcairns/Dropbox/Datasets/nyt_sections/" + section + "/"
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

if __name__ == "__main__":
    api = articleAPI('599c5ebb1e180f4cd6eb426217a06518:6:72209945')
    nytd_section = ['Arts']#,'Business','Obituaries','Sports','World']
    
    for section in nytd_section:
        save_dirpath = "/Users/camcairns/Dropbox/Datasets/nyt_sections/" + section + "/"
        mkdir_nyt(save_dirpath)
        num_pages = 1 #max = 101
        for i in range (0,num_pages):
            print "scraping %s section, page %d/%d" % (section, i+1, num_pages)
            articles = api.search(sort='newest', fq = {'source':['The New York Times'], 'document_type':['article'], 'section_name':[section]}, page=i)
            news = parse_articles(articles)
            
            body_text = []
            for j in range(10):
                r  = requests.get(news[j]['url'])
                data = r.text
                soup = BeautifulSoup(data)
                g_text = soup.find_all("p", {"class":["story-body-text story-content","story-body-text"]})
                g_text.extend(soup.find_all(["p", {"itemprop":"articleBody"}]))
                body_tmp = []
                for item in g_text:
                    body_tmp.append(item.text)

                save_filepath = save_dirpath + section + '_' + str(i*10+j).zfill(4) + '.csv'
                f = open(save_filepath, 'w')
                try:
                    writer = csv.writer(f)
                    writer.writerow( ('url', 'title', 'body') )
                    for k in range(10):
                        writer.writerow( (news[j]['url'], news[j]['headline'], body_text[j]) )
                finally:
                    f.close()



