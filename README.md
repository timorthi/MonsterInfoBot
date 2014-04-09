MonsterInfoBot
===============

A reddit bot for /r/MonsterHunter that filters comments for @monster-names and fetches relevant information from kiranico.com  

**There is already an instance of the bot running in /r/MonsterHunter. If you want to test it, use /r/test instead. The code uses /r/test by default.**  

There is no need for you to edit `bigmonster.txt` and `commentid.txt`:  
`bigmonster.txt` is just a storage for the list of monsters for the comments to be cross-checked against; `commentid.txt` stores the proccessed comment IDs.


Changelog
===============
**4.6.14**  
- Added functionality where bot deletes post if comment score <=-1.  

**4.8.14**  
- Creates commentid.txt if not found in local directory.  
Merged pull request by @icbat:  
- Factoring out code and placed them into functions
- Prepping code for implementation of new functions  

Running Locally
===============

1. Fork/clone the project
2. Install python 2.6+ (not 3.x)
3. Get [pip](http://www.pip-installer.org/en/latest/installing.html) or easy_install
4. Use pip or easy_install to get `beautifulsoup4`
5. Use pip or easy_install to get `praw`
6. Run `python main.py`
7. Do not point to r/MonsterHunter to prevent duplicate posts!

To Do
===============
- Code is extremely messy, not even close to PEP8 standard. Gotta clean it up, but I'll save this for when most of the main features are implemented.
- Bot is missing **a lot** of exception handling. If reddit, kiranico or my internet is down, the bot will just crash. Speaking of which..
- I should probably host the bot online, but since this is only the early stages of the bot, I guess it's alright to host it on my computer for the time being. My computer is on 24/7. I can't guarantee the same for internet.  
- Exception handling for login.  
- Selective information posting (carve/drop): Regex is done. Have to work on parsing the page.
- Update bot comment to include how to summon for carve/drops when feature is done.

Contributors
===============
icbat