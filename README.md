# Slack Bible
This script posts a Bible reading to a specified Slack channel every weekday.

#The Reading Plan
The plan is very simple: Monday, Wednesday, and Friday are Old Testament readings. Tuesday and Thursday are for New Testament readings. Every day there is also a reading from the Wisdom Literature (for the purposes of this script that includes Psalms, Proverbs, Eccelesiastes, Song of Solomon, and Lamentations). I am aware that Lamentations is not traditionally considered to be part of the Wisdom Literature.

The Old Testament ordering largely follows the Old Testament canon. This has the advantage of separating the books of Samuel and Kings from the books of Chronicles.

The New Testament is ordered idiosyncractically so as to break up the gospels. Other New Testament writings connected to the gospel are read after it (for example, the epistles of John follow the gospel of John, the epistles of Peter follow the gospel of Mark, the letters of Paul follow Luke-Acts).

#To Use
1) Create a Slack bot and add it to the channel you want Bible readings posted to. 
2) Copy settings.example.py to settings.py and insert the correct values for your bot's slack token and the channel to post to
3) Set up a cron job to run the script daily. Here is the cron entry I use: `0 5 * * * /usr/bin/python3 /PATH/TO/bible/slack.py > /dev/null 2>&1` - it runs the script at 5am every day.
