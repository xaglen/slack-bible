# Slack Bible
This script posts a Bible reading to a specified Slack channel every weekday.

# The Reading Plan
The plan is very simple: Monday, Wednesday, and Friday are Old Testament readings. Tuesday and Thursday are for New Testament readings. Every day there is also a reading from the Wisdom Literature (for the purposes of this script that includes Psalms, Proverbs, Ecclesiastes, Song of Solomon, and Lamentations). I am aware that Lamentations is not traditionally considered to be part of the Wisdom Literature.

The Old Testament ordering largely follows the Old Testament canon. This has the advantage of separating the books of Samuel and Kings from the books of Chronicles.

The New Testament is ordered idiosyncratically so as to break up the gospels. Other New Testament writings connected to a given gospel are read after it (for example, the epistles of John follow the gospel of John, the epistles of Peter follow the gospel of Mark, the letters of Paul follow Luke-Acts).

# The Rhythm Of Reading
*tl;dr: this plan takes you through the Old Testament annually and the New Testament twice per year.*

It's a little more complicated than that. In this plan we read the Old Testament 3 times a week, meaning 156 OT readings per fifty-two weeks. There are 126 separate OT readings, so we read through the Old Testament about 1.2 times per year (excluding the wisdom literature).

We read the New Testament 2 times per week, meaning 104 NT readings per fifty-two weeks. Since there are only 55 New Testament readings, we read through the New Testament roughly twice per year (1.9 times). 

We also read a chapter from the wisdom literature each day (five times per week), which works out to 260 readings per year. Given that there are 248 chapters in the wisdom literature (as defined by me), we read through the wisdom literature a little more than once per year.

You will note that these patterns do not sync up. This is a conscious choice so that every time I read the Bible things are juxtaposed in a new way. 

Saturdays are set aside as a catch-up day in case you missed one due to travel or some other constraint, and Sunday is left free since you'll be exposed to the Word at church that morning.

# To Use
1) Create a Slack bot and add it to the channel you want Bible readings posted to. 
2) Copy settings.example.py to settings.py and insert the correct values for your bot's slack token and the channel to post to
3) Set up a cron job to run the script daily. Here is the cron entry I use: `0 5 * * * /usr/bin/python3 /PATH/TO/bible/slack.py > /dev/null 2>&1` - it runs the script at 5am every day.
