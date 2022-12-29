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
import feedparser
from pprint import pprint

logger = logging.getLogger(__name__)
#journald_handler = JournaldLogHandler()
#journald_handler.setFormatter(logging.Formatter('[%(levelname)s] %message)s'))
#logger.addHandler(journald_handler)
logger.setLevel(logging.INFO)

client = WebClient(token=settings.SLACK_TOKEN)

today = date.today()

day_of_week = date.today().weekday()

feed_url="http://www.edginet.org/mcheyne/rss_feed.php?type=rss_2.0&tz=-8&cal=classic&bible=niv"
feed = feedparser.parse(feed_url)
if settings.DEBUG:
    pprint(feed)

if today.year%2==1:
    readings = "Today's <http://www.edginet.org/mcheyne/info.html|M'Cheyne> readings (Carson year one):\n"
else:
    readings = "Today's <http://www.edginet.org/mcheyne/info.html|M'Cheyne> readings (Carson year two):\n" 

for entry in feed.entries:
    if today.year%2==0 and 'Secret' in entry.title:
        title = entry.title.rsplit(' ', 1)[0]
        readings += "* <{link}|{title}>\n".format(title=title, link=entry.links[0].href)
        year_tag = "first year"
    elif today.year%2==1 and 'Family' in entry.title:
        title = entry.title.rsplit(' ', 1)[0]
        readings += "* <{link}|{title}>\n".format(title=title, link=entry.links[0].href)
        year_tag = "second year"

try: 
    resp=client.chat_postMessage(
        channel="xa-mcheyne",
        text=readings
    )
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    message = "Slack error posting Bible reading"
    if settings.DEBUG:
        print(message)
        print(e)
        print(e.response)
    else:
        logger.info(message)
        logger.info(e)
        logger.info(e.response)
except TypeError as e:
    message = "TypeError posting Bible reading: {}".format(repr(e))
    if settings.DEBUG:
        print(message+": "+repr(e))
    else:
        logger.info(message)
except:
    e = repr(sys.exc_info()[0])
    message = "Error posting Bible reading: {}".format(e)
    if settings.DEBUG:
        print(message)
    else:
        logger.info(message)
