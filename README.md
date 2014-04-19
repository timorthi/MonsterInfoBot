MonsterInfoBot
===============  

**[Reddit Link](http://www.reddit.com/r/MonsterHunter/comments/229ljg/introducing_umonsterinfobot/)**  

A reddit bot for /r/MonsterHunter that filters comments for @monster-names and fetches relevant information from kiranico.com  

**There is already an instance of the bot running in /r/MonsterHunter. If you want to test it, use /r/test instead. The code uses /r/test by default.**  

There is no need for you to edit `bigmonster.txt` and `commentid.txt`:  
`bigmonster.txt` is just a storage for the list of monsters for the comments to be cross-checked against. Clone this file along with the python file; `commentid.txt` stores the proccessed comment IDs. If the file does not exist, it will create one for you.  

Features
===============  
- The bot only gives you its damage chart (hitzones and elemental weaknesses) at the moment. See below for future plans.  
- Use `@` to prefix a monster name in your comment, e.g. `@sand-barioth`, `@lagiacrus`. It's case insensitive.  
- One monster per comment only. Bot only reads the first '@ word' it sees - even wrong ones.  
- The bot does not read edited comments.
- Large monsters only.  
- The bot only works for MH3U monsters since Kiranico only has information for that game.  
- The bot deletes any of its posts that has a negative comment score.  

Running Locally  
===============  
1. Fork/clone the project.  
2. Install python 2.6+ (not 3.x).  
3. Get [pip](http://www.pip-installer.org/en/latest/installing.html) or easy_install.  
4. Use pip or easy_install to get `beautifulsoup4`.  
5. Use pip or easy_install to get `praw`.  
6. Run `python main.py`.  
7. Do not point to /r/MonsterHunter to prevent duplicate posts!  

Changelog
===============
**4.6.14**  
- Added functionality where bot deletes post if comment score <=-1.  

**4.8.14**  
- Creates commentid.txt if not found in local directory.  

Merged pull request by @icbat:  
- Factoring out code and placed them into functions
- Prepping code for implementation of new functions  

**4.12.14**
- Made a login function and added exception handling for failed logins  
- Changed method names in preparation for carve/drop feature implementation  
- Changed some console logs to improve comprehensibility  

**4.19.14**
- Bot no longer replies with duplicate information. 
- Replaced get_comments with comment_stream.
- Bot will retry connection if connection to Reddit/Kiranico fails.

To Do
===============
- Code is extremely messy, not even close to PEP8 standard. Gotta clean it up, but I'll save this for when most of the main features are implemented.
- Host bot online.
- Selective information posting (carve/drop): Regex is done. Have to work on parsing the page.
- Update bot comment to include how to summon for carve/drops when feature is done.  
- Remove the need for a text file to store comment IDs.

Contributors
===============
icbat