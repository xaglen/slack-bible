"""
Posts a daily Bible reading to Slack
"""
import logging
#from systemd.journal import JournaldLogHandler
import csv
import sys
from datetime import date
import urllib.parse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import settings

logger = logging.getLogger(__name__)
#journald_handler = JournaldLogHandler()
#journald_handler.setFormatter(logging.Formatter('[%(levelname)s] %message)s'))
#logger.addHandler(journald_handler)
logger.setLevel(logging.INFO)

client = WebClient(token=settings.SLACK_TOKEN)

start = date(2012, 10, 22)
today = date.today()
weeks = (today-start).days//7

#print(weeks)
with open('/www/vhosts/xastanford.org/wsgi/xadb/scripts/bible/nt.csv', newline='') as csvfile:
    new_testament = list(csv.reader(csvfile, quoting=csv.QUOTE_NONE))
    new_testament_entries = sum(1 for row in new_testament)
    csvfile.close()

with open('/www/vhosts/xastanford.org/wsgi/xadb/scripts/bible/ot.csv', newline='') as csvfile:
    old_testament = list(csv.reader(csvfile, quoting=csv.QUOTE_NONE))
    old_testament_entries = sum(1 for row in old_testament)
    csvfile.close()

day_of_week = date.today().weekday()

#print(day_of_week)

ot_progress = 3*weeks # through the OT thrice as fast as if reading once a week
nt_progress = 2*weeks # NT is twice as fast

try:
    if day_of_week==0:
        passage = old_testament[ot_progress % old_testament_entries]
    elif day_of_week==1:
        passage = new_testament[nt_progress % new_testament_entries]
    elif day_of_week==2:
        ot_progress = ot_progress + 1
        ot_index = ot_progress % old_testament_entries
        passage = old_testament[ot_index]
    elif day_of_week==3:
#        print("Weeks: {weeks} NT entries: {nt}  result:{result}".format(weeks=weeks, nt=new_testament_entries, result=((2*weeks)%new_testament_entries)+1))
# ERROR ALERT  = Thursday Oct 27 2022 weeks was 522 and the calculation resulted in 55 (54 should be the max for nt entries)
# I need to redo this logic - maybe move the calculation outside the index and then modulus the result in the index?
#        passage = new_testament[(2*weeks)%new_testament_entries+1]
        nt_progress = nt_progress + 1
        nt_index = nt_progress % new_testament_entries
        passage = new_testament[nt_index]
    elif day_of_week==4:
        ot_progress = ot_progress + 2
        ot_index = ot_progress % old_testament_entries
        passage = old_testament[ot_index]
    else:
        sys.exit() # it's the weekend or there is a logic error
except IndexError: #weird - just wrap around
    if day_of_week in [0, 2, 4]:
        passage=old_testament[0]
    else:
        passage=new_testament[0]
#print(passage)

passage_string = "Main reading: <http://www.biblegateway.com/passage/?search={}&version=NIV'|{}>".format(urllib.parse.quote(passage[0]),passage[0])
#print(passage_string)

wisdom_books = {'Psalms':150, 'Proverbs':31, 'Job':42, 'Song of Songs':8, 'Ecclesiastes':12, 'Lamentations':5}

wisdom_chapters=sum(wisdom_books.values())

progress=(weeks*5+day_of_week) % wisdom_chapters

if progress<=150:
    wisdom_passage = "Psalm {}".format(progress)
elif progress<=181:
    wisdom_passage = "Proverbs {}".format(progress-150)
elif progress<=223:
    wisdom_passage = "Job {}".format(progress-181)
elif progress<=231:
    wisdom_passage = "Song of Songs {}".format(progress-223)
elif progress<=243:
    wisdom_passage = "Ecclesiastes {}".format(progress-231)
elif progress<=248:
    wisdom_passage = "Lamentations {}".format(progress-243)
else:
    wisdom_passage =""

if day_of_week==5 or day_of_week==6:
    wisdom_passage_string=""
else:
    wisdom_passage_string = "Wisdom reading: <http://www.biblegateway.com/passage/?search={}&version=NIV'|{}>".format(urllib.parse.quote(wisdom_passage),wisdom_passage)

#print (passage_string)
#print(wisdom_passage_string)

slack_message = "Today's Bible readings. See the schedule: <https://github.com/xaglen/slack_bible|GitHub>:\n* {}\n* {}".format(passage_string,wisdom_passage_string)

try: 
    resp=client.chat_postMessage(
        channel=settings.SLACK_CHANNEL,
        text=slack_message
    )
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    message = "Slack error posting Bible reading"
    logger.info(message)
    logger.info(e)
    logger.info(e.response)
#    print(message)
#    print(e)
except TypeError as e:
    message = "TypeError posting Bible reading: {}".format(repr(e))
    logger.info(message)
#    print(message+": "+repr(e))
except:
    e = repr(sys.exc_info()[0])
    message = "Error posting Bible reading: {}".format(e)
    logger.info(message)
#    print(message+": "+e)
