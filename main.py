from bs4 import BeautifulSoup
import praw, re, time, datetime, urllib2, sys, os, random

# @([\w-]+[LHG]) : regex for low, high, G rank carves. Syntax: @dire-miralis-G / @barioth-L

##########
# CONFIG #
##########

hdr = {'User-Agent': 'MonsterInfoBot from Reddit made by /u/xozzo',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

user_agent = (
"MonsterInfoBot for /r/MonsterHunter on Reddit"
"version 1.0 by /u/xozzo"
)

reddit = praw.Reddit(user_agent = user_agent)

monsterList = ["great-jaggi", "great-baggi", "great-wroggi", "arzuros", "lagombi", "volvidon", 
"qurupeco", "crimson-qurupeco", "barroth", "jade-barroth", "uragaan", "steel-uragaan", 
"duramboros", "rust-duramboros", "rathian", "pink-rathian", "gold-rathian", "rathalos", 
"azure-rathalos", "silver-rathalos", "diablos", "black-diablos", "gigginox", "baleful-gigginox", 
"barioth", "sand-barioth", "royal-ludroth", "purple-ludroth", "gobul", "nibelsnarf", "lagiacrus",
"ivory-lagiacrus", "abyssal-lagiacrus", "agnaktor", "glacial-agnaktor", "nargacuga", 
"green-nargacuga", "lucent-nargacuga", "zinogre", "stygian-zinogre", "plesioth", "green-plesioth",
"brachydios", "ceadeus", "goldbeard-ceadeus", "deviljho", "savage-deviljho", "jhen-mohran", 
"hallowed-jhen-mohran", "alatreon", "dire-miralis"]

#Steve code. Delete this block when removing Steve feature.
Steve1 = '**[Steve](http://i.imgur.com/iCOPN.jpg)**  \n\nPart|Cut|Impact|Shot|Fir|Wat|Ice|Thun|Dra  \n|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|  \nHead|12|0|3|0|0|17|0|0  \nNeck|180|4|20|0|0|17|0|4  \nBack|44|44|10|0|0|17|0|0  \nBelly|4|5|10|0|0|17|0|0  \nFront Leg|13|12|11|0|0|17|0|1  \nBack Leg|31|21|11|0|0|17|0|0  \nTail|1|3|3|7|0|17|0|1  \n\nSteve is too pretty for you.'
Steve2 = '**[Steve](http://i.imgur.com/7SNVtkp.jpg)**  \n\nPart|Cut|Impact|Shot|Fir|Wat|Ice|Thun|Dra  \n|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|  \nHead|15|40|30|0|30|10|25|0  \nNeck|50|20|20|0|15|5|10|5  \nBack|10|15|10|0|30|0|15|0  \nBelly|40|50|30|0|10|5|20|5  \nFront Leg|30|40|55|0|25|5|15|0  \nBack Leg|31|21|11|0|0|17|0|10  \nTail|15|10|10|0|35|5|10|0  \n\n\#STEVE4PRESIDENT'  
Steve3 = '**[Steve](http://i.imgur.com/O1iVTda.jpg)**  \n\nPart|Cut|Impact|Shot|Fir|Wat|Ice|Thun|Dra  \n|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|  \nHead|1|1|1|0|0|0|0|0  \nNeck|0|0|0|0|0|0|0|0  \nBack|0|0|0|0|0|0|0|0  \nBelly|0|0|0|0|0|0|0|0  \nFront Leg|0|0|0|0|0|0|0|0  \nBack Leg|0|0|0|0|0|0|0|0  \nTail|0|0|0|0|0|0|0|0  \n\nSteve is full of sadness and cereal.'
Steve4 = '**[Steve](http://i.imgur.com/snONC83.jpg)**  \n\nPart|Cut|Impact|Shot|Fir|Wat|Ice|Thun|Dra  \n|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|  \nHead|0|0|0|0|0|0|0|0  \nNeck|0|0|0|0|0|0|0|0  \nBack|0|0|0|0|0|0|0|0  \nBelly|0|0|0|0|0|0|0|0  \nFront Leg|0|0|0|0|0|0|0|0  \nBack Leg|100|100|100|50|50|0|50|50  \nTail|100|100|100|50|50|0|50|50  \n\nSteve is a big booty bitch.'

SteveList = [Steve1, Steve2, Steve3, Steve4]

##############	
# END CONFIG #
##############

#############	
# FUNCTIONS #
#############

def sleep(seconds): #use this for extra verbosity in the command line
	print 'Sleeping for ' + str(seconds) + ' seconds, starting %s' % datetime.datetime.now().time()
	time.sleep(seconds)

def login():
	TryingLogin = True
	while TryingLogin:
		try:
			global bot_user, bot_pass
			bot_user = raw_input("Bot username?\n> ")
			bot_pass = raw_input("Bot password?\n> ")
			print "Logging in.."
			reddit.login(bot_user, bot_pass)
			print "Successfully logged in as %s" % bot_user
			TryingLogin = False
			
		except praw.errors.InvalidUserPass:
			print 'Username/Password is wrong. Please re-enter username and password.'
		
		except Exception as e:
			if 'ratelimit' in e:
				print 'You tried logging in too many times in a short interval. Try again.'
				sleep(45)
			else:
				print 'Exception: %s. Trying again.' % e
				time.sleep(2)
				
def replied(comment):
	children = comment.replies
	
	if children:
		for child in children:
			if child.author.name in ["MonsterInfoBot", bot_user]:
				return True

def get_monster_damage(monstername): 
	while True:
		try:
			monstername = monstername.lower() #must be lowercase or Kiranico's analytics go crazy
			text = []
			print 'Getting source code from Kiranico..'
			site = 'http://www.kiranico.com/monster/%s' % monstername
			soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(site, headers=hdr)))
			print 'Site source obtained for %s' % monstername
			damageTable = soup.find('div', id='damage-chart-panel').findAll('tr')
			for tr in damageTable:
				raw = str(tr)
				sub1 = re.sub('<[^>]+>', '|', raw) #replace <anything enclosed in these things> with pipes (|)
				sub2 = re.sub('\n\|', ' ', sub1) #adhering to markdown formatting
				row = re.sub('\xe2\x80\x94', '-', sub2) #unicode to ASCII
				row = row[1:-2] #get rid of some of the extra pipes (|) 
				text.append(row)
			return text
			
		except urllib2.URLError:
			print 'URLError. Could not get site source.'
			sleep(300)
			continue	
			
		except urllib2.HTTPError:
			print 'HTTPError. Could not get site source.'
			sleep(300)
			continue
			
def check_scores():
	print 'Checking scores..'
	myComments = reddit.get_redditor(bot_user).get_comments(limit=100)
	for post in myComments:
		if post.score<=(-1):
			post.delete()
			print 'Post deleted.'
			time.sleep(2)
	print '..done'
	time.sleep(2)

def find_tagged_monster_name(comment):
	monster_name_pattern = '@' + '([\w-]+)'
	return re.search(monster_name_pattern, comment.body, re.IGNORECASE)	

def reply_with_damage_table(comment, name):
	print "Found match to monster list."
	reply_string = ''
	monster_damage = get_monster_damage(name.lower())
	
	for item in monster_damage:
		if item == monster_damage[0]:
			reply_string += item+'\n'
			reply_string += "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n"
		else:
			reply_string += item+'\n'

	comment.reply("**[" + name.title() + "](http://www.kiranico.com/monster/" + name.lower() + ")**  \n\n" + reply_string + "  \n* * *  \n^^^Summon: ^^^prefix ^^^monster ^^^name ^^^with ^^^'@'. ^^^If ^^^there ^^^is ^^^more ^^^than ^^^1 ^^^word, ^^^substitute ^^^the ^^^space ^^^for ^^^a ^^^hyphen, ^^^e.g. ^^^@barioth, ^^^@dire-miralis.  \n^^^Automatically ^^^deletes ^^^if ^^^comment ^^^score ^^^falls ^^^below ^^^0.  \n[^^^Author](/u/xozzo) ^^^| [^^^Source](https://github.com/xozzo/MonsterInfoBot)")
	print "Replied."
	sleep(120)
	
def isDuplicate(comment, name):
	flat_tree = praw.helpers.flatten_tree(comment.submission.comments, nested_attr=u'replies', depth_first=False)
	
	for comm in flat_tree:
		subspecies = re.search('(?=(-'+name+'))', comm.body, re.IGNORECASE)
		if comm.author.name in ["MonsterInfoBot", bot_user] and name in comm.body and comm != comment and not subspecies:
			return True

def too_many_steves(comment): #Steve code. Delete this function when removing Steve feature.
	steve_count = 0
	flat_tree = praw.helpers.flatten_tree(comment.submission.comments, nested_attr=u'replies', depth_first=False)
	
	for comm in flat_tree:
		if comm.author.name in ["MonsterInfoBot", bot_user]:
			its_steve = re.search('steve', comm.body, re.IGNORECASE)
			if its_steve:
				steve_count += 1
			
	if steve_count == 3:
		return True

#################	
# END FUNCTIONS #
#################

#############
# MAIN LOOP #
#############

login()

while True:
	try:
		check_scores()
		#Do NOT run this bot in /r/MonsterHunter: /u/MonsterInfoBot is already running!
		comments_generator = reddit.get_subreddit('test').get_comments(limit = 50)
		print 'New comment generator fetched.'
		
		for comment in comments_generator:
			replied(comment)
			searchObject = find_tagged_monster_name(comment)
			Steve = re.search('@Steve', comment.body, re.IGNORECASE) #Steve code. Delete this block when removing Steve feature.
			
			if Steve and not replied(comment) and comment.author.name not in ["MonsterInfoBot", bot_user]:
				print 'We found Steve!'
				too_many_steves(comment)
				
				if not too_many_steves(comment):
					random.shuffle(SteveList)
					comment.reply(SteveList[0])
					print comment.author.name + ' now knows what Steve is all about.'
					sleep(120)
					
				elif too_many_steves(comment):
					comment.reply('STEVE OVERLOAD!!!')
					print 'Steve overload!'
					sleep(120)
					
			elif searchObject and not replied(comment) and comment.author.name not in ["MonsterInfoBot", bot_user]:
				print 'Found word with @ prefix.'
				name = searchObject.group(1).lower()
				
				if name in monsterList:
					isDuplicate(comment, name)
					
					if not isDuplicate(comment, name):
						reply_with_damage_table(comment, name)
						
					elif isDuplicate(comment, name):
						comment.reply("There is already a post in this submission with information on " + name.title() + ".  \n\nUse Ctrl/Cmd+F to look for the relevant information.")
						print 'There is already a post in this submission with this information (' + name + ').'
						sleep(120)
									
				else:
					print "Name does not exist in monster list. String entered: " + name
					time.sleep(2)
						
			elif not replied(comment): #Comment has no match, or author is bot_user
				print 'Could not find match in comment (%s). Trying next comment..' % comment.id
				time.sleep(2)
									
			elif replied(comment): #Comment has already been processed
				print 'This comment (%s) has already been replied to. Trying next comment..' % comment.id
				time.sleep(2)
				
	#TODO: Catching all exceptions is a faux-pas. Rewrite this!
	except Exception as e:
		print 'Error: %s.' % e
		sleep(180)
		continue
		
#################
# END MAIN LOOP #
#################
