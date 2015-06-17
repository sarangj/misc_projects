'''this allows you to interact with GroupMe's API and do some
    neat analysis with it'''

TOKEN = 'your_token'
GROUP_NAME = 'your_group_name'
GROUP_ID = 'your_group_id'
BEFORE_MESSAGE_ID = 'message_id_of_the_latest_message_in_your_group' #you can get this from group_data

#get the base information about this GroupMe
import pandas as pd
import json
import requests
url = 'https://api.groupme.com/v3/groups'
options = {'name':GROUP_NAME, 'token':TOKEN}
group_data = requests.get(url, params=options).text
group_data = json.loads(group_data)

#map the user_id of each individual to his name in the GroupMe (this will be useful later)
user_ids = {person['user_id'].encode('ascii'):person['nickname']
                for person in group_data['response'][0]['member']}

#get metadata for all messages sent in this GroupMe
url_messages = url + '/' + GROUP_ID + '/messages'
options = {'before_id':BEFORE_MESSAGE_ID, 'limit':'100', 'token':TOKEN}
messages_data = requests.get(url_messages, params=options).text
messages_data = json.loads(messages_data)

#this function will pull the metadata for the last 100 messages before a given message_id
def get_last_100_messages(message_id):
    global GROUP_ID
    global TOKEN
    url = 'https://api.groupme.com/v3/groups' + '/' + GROUP_ID + '/messages'
    options = {'before_id':message_id, 'limit':'100', 'token':TOKEN}
    data = requests.get(url, params=options).text
    data = json.loads(data)
    last_message_id = data['response']['messages'][-1]['id'].encode('ascii')
    return data['response']['messages'], last_message_id

#this function will get the last 100 messages before the most recent message,
#then re-seed get_last_100_messages to get the previous 100 before that,
#and so on, until I have all the messages I want
def get_all_messages(initial_message_id):

    all_message_data = []
    last_message_id = initial_message_id
    
    while True:
        all_message_data = all_message_data + get_last_100_messages(last_message_id)[0]
        if len(get_last_100_messages(last_message_id)[0]) != 100:
            return all_message_data    
        else:
            last_message_id = get_last_100_messages(last_message_id)[1]

all_messages = get_all_messages(BEFORE_MESSAGE_ID) #the initial message_id

#I want to perform some operations on the data now. I'm going to put it in a defaultdict for easy insertion.
from collections import defaultdict
favorites = [(item['sender_id'].encode('ascii'), len(item['favorited_by'])) for item in all_messages]
d = defaultdict(list)
for k, v in favorites:
    d.setdefault(k, []).append(v)

likes_per_message = {k: sum(vals)/float(len(vals)) for k, vals in d.viewitems()}
for key, val in likes_per_message.iteritems():
    try:
        print user_ids[key].ljust(25), '%0.4f' % val
    except KeyError:
        continue

messages_per_user = {k: len(vals) for k, vals in d.viewitems()}
for key, val in messages_per_user.iteritems():
    try:
        print user_ids[key].ljust(25), val
    except KeyError:
        continue

total_likes = {k: sum(vals) for k, vals in d.viewitems()}
for key, val in total_likes.iteritems():
    try:
        print user_ids[key].ljust(25), val
    except KeyError:
        continue

# # Follow-up Question

#How many times has each person "liked" the messages of every other person?
from collections import Counter
metadict = defaultdict(list)
for key, name in user_ids.iteritems():
    c = Counter()
    for item in all_messages:
        try:            
            if item['sender_id'] == key:
                c.update(item['favorited_by'])
        except KeyError:
            continue
    for k, v in c.items():
        try:
            metadict.setdefault(user_ids[key], []).append((user_ids[k],v))
        except KeyError:
            continue

#fill in any missing data to account for haters
for lst in metadict.values():
    names = [tpl[0] for tpl in lst]
    for key, name in user_ids.iteritems():
        if name not in names:
            lst.append((name, 0))

#check to see that all lists are the same length
for lst in metadict.values():
    print len(lst) 

#I'm going to create the initial DataFrame for one person, then join it along the same index
#for each of the remaining 19 people. Then I reorder the columns to make viewing easier.
#Let's investigate for "like" alliances among male-male dyads.
df1 = pd.DataFrame(data=sorted(metadict.items()[0][1]), columns=["liker", metadict.keys()[0]]).set_index("liker")
frames = [pd.DataFrame(data=sorted(vals), columns=["liker", key]).set_index("liker") 
          for key, vals in metadict.items()[1:]]
result = df1.join(frames)
column_order = sorted(metadict.keys())
result[column_order]




