from bs4 import BeautifulSoup
from nytimesarticle import articleAPI
import csv
import sys
import os
import errno
import requests
reload(sys)
sys.setdefaultencoding('utf8')


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
        dic['date'] = i['pub_date'][0:10]  # cutting time of day.
        dic['section'] = i['section_name']
        if i['snippet'] is not None:
            dic['snippet'] = i['snippet'].encode("utf8")
        dic['source'] = i['source']
        dic['type'] = i['type_of_material']
        dic['url'] = i['web_url']
        dic['word_count'] = i['word_count']
        # locations
        locations = []
        for x in range(0, len(i['keywords'])):
            if 'glocations' in i['keywords'][x]['name']:
                locations.append(i['keywords'][x]['value'])
        dic['locations'] = locations
        # subject
        subjects = []
        for x in range(0, len(i['keywords'])):
            if 'subject' in i['keywords'][x]['name']:
                subjects.append(i['keywords'][x]['value'])
        dic['subjects'] = subjects
        news.append(dic)
    return(news)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def create_save_dir(file_type, section):
    root_dirpath = os.environ["data_dir"] + "nyt_corpus/"
    save_dirpath = "/".join(root_dirpath, file_type, section)
    mkdir_p(save_dirpath)
    return save_dirpath


if __name__ == "__main__":
    api = articleAPI(os.environ["nyt_api_key"])  # load export nyt api key as environmental variable alias=nyt_api_key

    nytd_section = ['Arts', 'Business', 'Obituaries', 'Sports', 'World']
    for section in nytd_section:
        num_pages = 101  # nyt max paginate limit = 101
        for i in range(0, num_pages):
            print "scraping %s section, page {0}/{1}".format(section, i+1, num_pages)
            articles = api.search(sort='newest', fq={'source': ['The New York Times'], 'document_type': ['article'], 'section_name': [section]}, page=i)
            news = parse_articles(articles)

            body_text = []
            for j in range(10):
                r = requests.get(news[j]['url'])
                data = r.text
                soup = BeautifulSoup(data)
                g_text = soup.find_all("p", {"class": ["story-body-text story-content", "story-body-text"]})
                g_text.extend(soup.find_all(["p", {"itemprop": "articleBody"}]))
                body_tmp = []
                for item in g_text:
                    body_tmp.append(item.text)

                # write out csv (url, headline, body)
                save_dirpath = create_save_dir("csv_documents", section)
                save_filepath = save_dirpath + "/{0}_{1}.csv".format(section, str(i*10+j).zfill(4))
                f = open(save_filepath, 'w')
                try:
                    writer = csv.writer(f)
                    writer.writerow(('url', 'title', 'body'))
                    writer.writerow((news[j]['url'], news[j]['headline'], body_tmp))
                finally:
                    f.close()

                # write article out as .txt document (headline + body)
                save_dirpath = create_save_dir("txt_documents", section)
                save_filepath = save_dirpath + "/{0}_{1}.txt".format(section, str(i*10+j).zfill(4))
                text = [news[j]['headline']] + body_tmp[:-2]
                f = open(save_filepath, 'w')
                try:
                    for item in text:
                        f.write(item)
                finally:
                    f.close()