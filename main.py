from bs4 import BeautifulSoup
import praw, re, datetime, time, urllib2, random

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
	"""
	Logs in to Reddit via the command line. This will be the bot account.
	"""
	trying_login = True
	while trying_login:
		try:
			global bot_user, bot_pass
			bot_user = raw_input("Bot username?\n> ")
			bot_pass = raw_input("Bot password?\n> ")
			print "Logging in.."
			reddit.login(bot_user, bot_pass)
			print "Successfully logged in as %s" % bot_user
			trying_login = False
			
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
	"""
	Takes a comment object as an argument. Returns `True` if any of its child
	comments are replied to by "MonsterInfoBot" or whatever the current user
	is.
	"""
	children = comment.replies
	
	if children:
		for child in children:
			if child.author.name in ["MonsterInfoBot", bot_user]:
				return True

def get_monster_damage(monster_name):
	"""
	Takes a monster name as an argument, looks it up on Kiranico and scrapes
	the resulting page for the damage chart. Using regex, convert HTML
	to Reddit-appropriate Markdown. Returns a list where each element
	represents a row in the damage chart.
	"""
	while True:
		try:
			monster_name = monster_name.lower() #must be lowercase or Kiranico's analytics will be affected
			text = []
			print 'Getting source code from Kiranico..'
			site = 'http://www.kiranico.com/monster/%s' % monster_name
			soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(site, headers=hdr)))
			print 'Site source obtained for %s' % monster_name
			damage_table = soup.find('div', id='damage-chart-panel').findAll('tr')
			for tr in damage_table:
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
	"""
	Checks if any of the comments made by the bot falls below -1. Deletes
	the comment if true.
	"""
	print 'Checking scores..'
	my_comments = reddit.get_redditor(bot_user).get_comments(limit=100)
	for post in my_comments:
		if post.score<=(-1):
			post.delete()
			print 'Post deleted.'
			time.sleep(2)
	print '..done'
	time.sleep(2)

def find_tagged_monster_name(comment):
	"""
	Takes a comment object as an argument. Returns the result of a regex
	search on the comment body for anything with the syntax @monster_name.
	"""
	monster_name_pattern = '@' + '([\w-]+)'
	return re.search(monster_name_pattern, comment.body, re.IGNORECASE)	

def reply_with_damage_table(comment, name):
	"""
	Takes a comment object and monster name as arguments. Generates a reply
	in appropriate Reddit formatting and replies to the comment that summoned
	the bot.
	"""
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
	
def is_duplicate(comment, name):
	"""
	Takes a comment object and monster name as arguments. Check if the bot
	has already posted the chart for the given monster in the current
	submission. Iterating through the submission's comments 
	using the following conditions for each comment:
		1. Bot has replied to this comment.
		2. Monster name is in comment body.
		3. This comment is not the comment in which the function is checking against.
		4. The regex search for a subspecies "-monster_name" returns false.
		
	If all of these conditions are met, then `comment` is a duplicate and the
	function returns `True`.
	"""
	flat_tree = praw.helpers.flatten_tree(comment.submission.comments, nested_attr=u'replies', depth_first=False)
	
	for comm in flat_tree:
		subspecies = re.search('(?=(-'+name+'))', comm.body, re.IGNORECASE)
		if comm.author.name in ["MonsterInfoBot", bot_user] and name in comm.body and comm != comment and not subspecies:
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
			search_object = find_tagged_monster_name(comment)
					
			if search_object and not replied(comment) and comment.author.name not in ["MonsterInfoBot", bot_user]:
				print 'Found word with @ prefix.'
				name = search_object.group(1).lower()
				
				if name in monsterList:
					is_duplicate(comment, name)
					
					if not is_duplicate(comment, name):
						reply_with_damage_table(comment, name)
						
					elif is_duplicate(comment, name):
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
				
	except Exception as e:
		print 'Error: %s.' % e
		sleep(180)
		continue
		
#################
# END MAIN LOOP #
#################
