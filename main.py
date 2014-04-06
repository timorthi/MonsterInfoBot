from bs4 import BeautifulSoup
import praw, re, time, datetime, urllib2

##########
# CONFIG
##########

hdr = {'User-Agent': 'MonsterInfoBot from Reddit made by /u/xozzo',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

user_agent = (
"Kiranico Monster Information Fetching Bot"
"version 1.0 by /u/xozzo"
)

reddit = praw.Reddit(user_agent = user_agent)

bot_user = raw_input("Bot user?\n> ")
bot_pass = raw_input("Bot password?\n> ")
print "Logging in.."
reddit.login(bot_user, bot_pass)
print "Successfully logged in as %s" % bot_user

with open('bigmonster.txt', 'r') as monsternames:
	monsterList = [line.rstrip() for line in monsternames]
	
##############	
# END CONFIG
##############

def get_info(monstername): #Always pass a lowercase argument to this method - Kiranico's analytics will go crazy otherwise
	while True:
		try:
			print 'Getting source code from Kiranico..'
			site = 'http://www.kiranico.com/monster/%s' % monstername
			request = urllib2.Request(site, headers=hdr) 
			connect = urllib2.urlopen(request)
			soup = BeautifulSoup(connect)
			print 'Site source obtained for %s' % monstername
			damageTable = soup.find('div', id='damage-chart-panel').findAll('tr')
			for tr in damageTable:
				tags = '<[^>]+>' #pattern for <anything enclosed in these things>
				raw = str(tr)
				sub1 = re.sub(tags, '|', raw)
				sub2 = re.sub('\n\|', ' ', sub1)
				row = re.sub('\xe2\x80\x94', '-', sub2)
				row = row[1:-2] #get rid of some of the extra pipes (|) 
				text.append(row)
			break
			
		except urllib2.URLError:
			print 'URLError raised. Could not get site source. Trying again in 5 minutes..'
			time.sleep(300)
			continue
			
		except urllib2.HTTPError:
			print 'HTTPError raised. Could not get site source. Trying again in 5 minutes..'
			time.sleep(300)
			continue
			
def check_scores():
	print 'Checking scores..'
	me = reddit.get_redditor(bot_user)
	myComments = me.get_comments(limit=50)
	for post in myComments:
		if post.score <= (-1):
			post.delete()
			print 'Post deleted.'
			sleep(2)
	print '..done'
	sleep(2)


#############
# MAIN LOOP
#############

while True:
	try:
		#Fellow programmers - do NOT run this bot in /r/MonsterHunter: /u/MonsterInfoBot is already running!
		check_scores()
		comments_generator = reddit.get_subreddit('test').get_comments(limit = 100)
		print 'New comment generator fetched.'
		
		for comment in comments_generator:
			idList = []
			text = []
			reply_string = ''
			with open('commentid.txt', 'r') as idfile:
				idList = [line.rstrip() for line in idfile]
			print 'Initialized/Reinitialized lists and reply string'
			
			pattern = '@' + '((?:[a-z][a-zA-Z0-9][a-z0-9_]*))' #variable monster name
			patternWithHyphen = '@' + '(\w+(?:-\w+)+)' #multiple word monster names
			searchObject = re.search(pattern, comment.body, re.IGNORECASE)
			searchObjectWithHyphen = re.search(patternWithHyphen, comment.body, re.IGNORECASE)
			
			#match to @multiple-worded-name
			if searchObjectWithHyphen and comment.id not in idList and comment.author.name not in ["MonsterInfoBot"]:
					print 'searchObjectWithHyphen found.'
					name_hyphen = searchObjectWithHyphen.group(1)
					
					if name_hyphen.lower() in monsterList:
						print "Found match to monster list."
						get_info(name_hyphen.lower())
						
						for item in text:
							if item == text[0]:
								reply_string += item+'\n'
								reply_string += "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n"
							else:
								reply_string += item+'\n'
						
						comment.reply("**[" + name_hyphen.title() + "](http://www.kiranico.com/monster/" + name_hyphen.lower() + ")**  \n" + reply_string + "  \n* * *  \n^(Summon: prefix monster name with '@'. If there is more than 1 word, substitute the space for a hyphen, e.g. @barioth, @dire-miralis.)  \n^(Will delete post if score is below 0.)  \n^(Have a bug to report/suggestion to make? Message my creator at /u/xozzo!)")
						print "Replied."
						with open('commentid.txt', 'a') as idfile:
							idfile.write(comment.id+'\n')
						print "Comment ID stored."
						print "Sleeping for 2 minutes, starting %s" % datetime.datetime.now().time()
						time.sleep(120)
						continue
						
					else:
						print "Invalid monster name. String entered: " + name_hyphen
						with open('commentid.txt', 'a') as idfile:
							idfile.write(comment.id+'\n')
						print "Comment ID stored."
						print "Sleeping for 30 seconds, starting %s" % datetime.datetime.now().time()
						time.sleep(30)
						continue
			
			#match to @name
			elif searchObject and comment.id not in idList and comment.author.name not in ["MonsterInfoBot"]:
					print 'searchObject found.'
					name = searchObject.group(1)
					
					if name.lower() in monsterList:
						print "Found match to monster list."
						get_info(name.lower())
						
						for item in text:
							if item == text[0]:
								reply_string += item+'\n'
								reply_string += "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n"
							else:
								reply_string += item+'\n'
			
						comment.reply("**[" + name.title() + "](http://www.kiranico.com/monster/" + name.lower() + ")**  \n" + reply_string + "  \n* * *  \n^(Summon: prefix monster name with '@'. If there is more than 1 word, substitute the space for a hyphen, e.g. @barioth, @dire-miralis.)  \n^(Will delete post if score is below 0.)  \n^(Have a bug to report/suggestion to make? Message my creator at /u/xozzo!)")
						print "Replied."
						with open('commentid.txt', 'a') as idfile:
							idfile.write(comment.id+'\n')
						print "Comment ID stored."
						print "Sleeping for 2 minutes, starting %s" % datetime.datetime.now().time()
						time.sleep(120)
						continue
						
					else:
						print "Invalid monster name. String entered: " + name
						with open('commentid.txt', 'a') as idfile:
							idfile.write(comment.id+'\n')
						print "Comment ID stored."
						print "Sleeping for 30 seconds, starting %s" % datetime.datetime.now().time()
						time.sleep(30)
						continue
						
			else:
					#Comment has no match
					if comment.id not in idList and comment.author.name not in ["MonsterInfoBot", "xozzo"]:
						print 'Could not find any matching comments. Trying again..'
						
						with open('commentid.txt', 'a') as idfile:
							idfile.write(comment.id+'\n')
						time.sleep(2)
						continue
						
					#Comment has already been processed
					elif comment.id in idList:
						print 'Comment already in ID list. Trying again..'
						time.sleep(2)
						continue
					
					#Everything else basically	
					else:
						print 'No more new comments. Trying again..'
						time.sleep(2)
						continue
						
	#TODO: Catching all exceptions is a faux-pas. Rewrite this!
	except Exception as e:
		sys.exit()