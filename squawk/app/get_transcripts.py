import requests
from bs4 import BeautifulSoup
from collections import defaultdict

words = defaultdict(list)

# NYTimes URLs
nyturls = ['http://www.nytimes.com/2015/12/16/us/politics/transcript-main-republican-presidential-debate.html',
           'http://www.nytimes.com/2015/11/11/us/politics/transcript-republican-presidential-debate.html',
           'http://www.nytimes.com/2015/10/29/us/politics/transcript-republican-presidential-debate.html']

# Time URLs
timeurls = ['http://time.com/3988276/republican-debate-primetime-transcript-full-text/',
            'http://time.com/4037239/second-republican-debate-transcript-cnn/']

def get_transcript(url, words_dict, tag_options=None):

    now_talking = ''

    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    speakers = [item.contents[0].split(':')[0] for item in soup.find_all('p', tag_options)[1:-1]]
    speakers = list(set([item for item in speakers if item.upper() == item and '(' not in item]))
    if 'MORE' in speakers: speakers.remove('MORE')  # come up with a better way to separate the one-off caps words

    for item in soup.find_all('p', tag_options)[1:-1]:
        if item.contents[0].split(':')[0] in speakers and item.contents[0].split(':')[0] != now_talking:
            now_talking = item.contents[0].split(':')[0]
            words[now_talking].append(item.contents[0].split(':')[1])
        if item.contents[0].split(':')[0] not in speakers and '(' not in item.contents[0].split(':')[0]:
            words[now_talking].append(item.contents[0].split(':')[0])

    return words_dict

if __name__ == '__main__':
    for url in nyturls:
        get_transcript(url, words, tag_options={'class':'story-body-text story-content'})

    for url in timeurls:
        get_transcript(url, words)

    # cleaning
    for speaker in speakers:
        words[speaker] = [statement.replace(u'\u2019', '') for statement in words[speaker]]
        words[speaker] = [statement.replace(u'...', '') for statement in words[speaker]]
        words[speaker] = [statement.replace(u'Mr.', 'Mr') for statement in words[speaker]]
        words[speaker] = [statement.replace(u'\u201c', '') for statement in words[speaker]]
        words[speaker] = [statement.replace(u'\u201d', '') for statement in words[speaker]]
