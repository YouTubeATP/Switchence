#+= imports =+#
import sys
import os
import time
if sys.version_info < (3, 8):
	os.system('cls' if os.name == 'nt' else 'clear')
	print('[Warning] Your version of Python is lower than the recommended Python version')
	print('This program officially supports Python version 3.8 and higher')
	print(sys.version_info)
	vInput = input('Do you wish to continue (Y/N)? ')
	if not vInput.lower() in ['yes', 'y']:
		sys.exit(0)
import json
import webbrowser
import ctypes
import random
try:  # only try for the modules that need to be installed
	import requests
	from pypresence import Presence
	from colorama import Fore, init
	init()
	os.system('cls' if os.name == 'nt' else 'clear')
except ImportError as missingmod:
	os.system('cls' if os.name == 'nt' else 'clear')
	print(f'[Error] Module \'{missingmod.name}\' is missing')
	module = input('Would you like to install all of the required modules? ')
	if module in ['yes', 'y']:
		print('[Info] Installing now...')
		try:
			os.system('pip install --upgrade pip')
			os.system('pip install pypresence')
			os.system('pip install requests')
			os.system('pip install colorama')
			print('\n[Info] Successfully installed all of the required modules! Please restart Switchence')
			time.sleep(600)
			sys.exit(0)
		except Exception as error:
			print('Error in installing required modules automatically. Please install them manually. Error below')
			print(error)
			time.sleep(600)
			sys.exit(0)
	else:
		print('[Info] Installation of required modules cancelled')
		time.sleep(600)
		sys.exit()
initializeTime = time.time()


#+= important functions =+#
class log:
	def __init__(self, text, color):
		self.text = text
		self.color = color

	def error(text: str):
		changeWindowTitle('Error')
		clear()
		print(f'{Fore.LIGHTRED_EX}[Error]{Fore.RESET} {text}')
		print('Please report this error on the Switchence GitHub issue page if this error happens consistently')
		time.sleep(5)
		webbrowser.open('https://github.com/Aethese/Switchence/issues/', new=2, autoraise=True)
		time.sleep(600)
		sys.exit(1)

	def info(text: str, close):  # second param is for if i want switchence to close after printing info
		changeWindowTitle('Info')
		print(f'{Fore.LIGHTGREEN_EX}[Info]{Fore.RESET} {text}')
		if close:
			clear()
			print(f'{Fore.LIGHTGREEN_EX}[Info]{Fore.RESET} {text}')
			print('This program will now close in 10 minutes')
			time.sleep(600)
			sys.exit(0)

	def loading(text: str, color):  # color is the color of the loading text
		if color == 'green':
			color = Fore.LIGHTGREEN_EX
		elif color == 'yellow':
			color = Fore.LIGHTYELLOW_EX
		else:
			color = Fore.LIGHTRED_EX
		print(f'{Fore.LIGHTCYAN_EX}[Loading] {color}{text}{Fore.RESET}')


class config:
	def update(self, changeto):  # self = setting being changed
		with open('config.json', 'r') as jfile:
			jFile = json.load(jfile)
			for i in jFile['config']:
				i[self] = changeto
		with open('config.json', 'w') as jfile:
			json.dump(jFile, jfile, indent=4)

	@staticmethod
	def create(swcode):
		try:  # fucking global vars
			global sw, version, updatenotifier, configfname, showbutton, autoupdate, favorites
			configjson = {'config': [{
				'sw-code': swcode,
				'version': '1.9.3',
				'update-notifier': True,
				'fname': False,
				'show-button': True,
				'auto-update': False,
				'favorites': []
			}]}
			log.loading('Got settings to save, saving them...', 'yellow')
			with open('config.json', 'w') as jsonfile:
				json.dump(configjson, jsonfile, indent=4)
			with open('config.json', 'r') as jsonfile:  # actually get the info lol
				jsonFile = json.load(jsonfile)
				for details in jsonFile['config']:
					sw = details['sw-code']
					version = details['version']
					updatenotifier = details['update-notifier']
					configfname = details['fname']
					showbutton = details['show-button']
					autoupdate = details['auto-update']
					favorites = details['favorites']
				log.loading('Config file settings set!', 'green')
		except Exception as error:
			log.error(f'Couldn\'t create config settings | {error}')


log.loading('Loading initial functions...', 'yellow')
def clear():
	os.system('cls' if os.name == 'nt' else 'clear')  # *supposedly* multiplatform supported clear
clear()


def changeWindowTitle(title):
	if os.name == 'nt':  # hopefully multiplatform support
		ctypes.windll.kernel32.SetConsoleTitleW(f'Switchence | {title}')
changeWindowTitle('Loading...')


def reopen(path):
	fileName = os.path.basename(__file__)
	if not path:
		return fileName  # just to get path
	if os.path.isfile('Switchence.exe'):  # TODO: add support for if they changed file name lol
		sys.exit(0)  # TODO: actually reopen exe file lol
	elif '.py' in fileName:  # even exe files are considered .py files :/
		os.system(f'python3 {fileName}')
	else:
		sys.exit(1)


def updateProgram(onlinever):
	changeWindowTitle(f'Updating to version {onlinever}')
	log.info(f'Updating to version {onlinever}...', False)
	currentFile = reopen(False)
	if os.path.isfile('Switchence.exe'):
		config.update('auto-update', False)  # fixes infinite error loop lol
		log.info('The exe file does not currently support auto updating', True)
	currentOnlineVersion = requests.get('https://raw.githubusercontent.com/Aethese/Switchence/main/main.py')
	if currentOnlineVersion.status_code != 200:  # request to get raw code was not successful
		log.error(f'Status code is not 200, it is {currentOnlineVersion.status_code}, so the program will not update')
	elif currentOnlineVersion.status_code == 429:  # being rate limited
		log.info('Woah, slow down! You\'re being rate limited!', True)
	onlineVersionBinary = currentOnlineVersion.content  # get binary version of raw code
	with open(currentFile, 'wb') as file:  # thanks to https://stackoverflow.com/users/13155625/dawid-januszkiewicz
		file.write(onlineVersionBinary)  # for getting this to work!
	config.update('version', onlinever)
	changeWindowTitle(f'Updated to version {onlinever}')
	ro = input('Would you like to reopen Switchence? ')
	if ro in ['yes', 'y']:
		reopen(True)
	log.info(f'Finished updating to version {onlinever}', True)


#+= variables =+#
# just pre defining variables
beta = False  # if current build is a test build
version = None
oVersion = None  # online version
sw = None
updatenotifier = None
configfname = None
showbutton = None
autoupdate = None
gamenames = []
gamefnames = []
chosenOne = ''
updateAvailable = False
announcement = None
favorites = None
tips = None

#+= loading config file =+#
log.loading('Checking for config file...', 'yellow')
if os.path.isfile('config.json'):
	log.loading('Found config file, attempting to read contents...', 'yellow')
	try:
		with open('config.json', 'r') as jsonfile:
			jsonFile = json.load(jsonfile)
			for details in jsonFile['config']:
				sw = details['sw-code']
				version = details['version']
				updatenotifier = details['update-notifier']
				configfname = details['fname']
				showbutton = details['show-button']
				autoupdate = details['auto-update']
				favorites = details['favorites']
			log.loading('Loaded config settings!', 'green')
	except Exception:  # if some settings are missing, recreate the file while saving some settings
		if sw is None:  # in case an empty config file is found
			sw = ''
		if version is None:
			version = '1.9.3'
		log.loading('Missing config settings found, creating them...', 'red')
		log.loading('This means some settings will be reset to default', 'red')
		config.create(sw)
elif os.path.isfile('config.json') is False:
	log.loading('Config file not found, attempting to create one...', 'yellow')
	sw = ''  # sw var is needed in function below, so it needs to be pre defined
	config.create(sw)

#+= game list =+#
log.loading('Attempting to load game list...', 'yellow')
gamejson = requests.get('https://raw.githubusercontent.com/Aethese/Switchence/main/games.json')  # auto update game list :)
if gamejson.status_code != 200:
	log.error(f'Failed to get game list with status code {gamejson.status_code}')
elif gamejson.status_code == 429:
	log.info('Woah, slow down! You\'re being rate limited!', True)
gamejsontext = gamejson.text
games = json.loads(gamejsontext)
oVersion = games['version']
announcement = games['announcement']
tips = games['tips']
log.loading('Game list loaded!', 'green')

log.loading('Attempting to read game list info...', 'yellow')
for details in games['games']:
	gamenames.append(details['name'])
	gamefnames.append(details['fname'])
log.loading('Successfully read game list info!', 'green')

#+= checking version =+#
log.loading('Checking file version...', 'yellow')
if version in [None, '']:  # checks your version
	log.loading('File version not found, attempting to create...', 'red')
	config.update('version', oVersion)
	log.loading('Successfully created file version!', 'green')
elif version != oVersion:
	updateAvailable = True

#+= rpc =+#
log.loading('Attempting to start Rich Presence...', 'yellow')
RPC = Presence('803309090696724554')
RPC.connect()
log.loading('Successfully started Rich Presence!', 'green')


#+= some more important functions =+#
def changePresence(swstatus, gameimg, gamefname):
	start_time = time.time()
	string = time.strftime('%H:%M', time.localtime())
	if beta:  # set small image to indicate build ran by user is a beta build or not
		smallText = 'Switchence Beta'
		smallImg = 'gold_icon'
	else:
		smallText = f'Switchence v{version}'
		smallImg = 'switch_png'
	if swstatus is False:
		if showbutton:
			RPC.update(large_image=gameimg, large_text=gamefname, small_image=smallImg, small_text=smallText, details=gamefname,
					   buttons=[{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}], start=start_time)
		else:
			RPC.update(large_image=gameimg, large_text=gamefname, small_image=smallImg, small_text=smallText, details=gamefname, start=start_time)
		print(f'Set game to {Fore.LIGHTGREEN_EX}{gamefname}{Fore.RESET} at {string}')
		changeWindowTitle(f'Playing {gamefname}')
	else:
		if showbutton:
			RPC.update(large_image=gameimg, large_text=gamefname, small_image=smallImg, small_text=smallText, details=gamefname,
					state=f'SW-{sw}', buttons=[{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}], start=start_time)
		else:
			RPC.update(large_image=gameimg, large_text=gamefname, small_image=smallImg, small_text=smallText, details=gamefname, state=f'SW-{sw}', start=start_time)
		print(f'Set game to {Fore.LIGHTGREEN_EX}{gamefname}{Fore.RESET} at {string} with friend code \'SW-{sw}\' showing')
		changeWindowTitle(f'Playing {gamefname}')


def changeUpdateNotifier():
	picked = input('\nWhat setting do you want the Update Notifier to be set to, on or off? ')
	picked = picked.lower()
	if picked in ['on', 'true', 't']:  # why do you want this on tbh
		config.update('update-notifier', True)
		log.info(f'Update notifier set to {Fore.LIGHTGREEN_EX}TRUE{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen(True)
	elif picked in ['off', 'off', 'f']:
		config.update('update-notifier', False)
		log.info(f'Update notifier set to {Fore.LIGHTRED_EX}FALSE{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen(True)


def changeFNameSetting():
	length = 'short' if configfname is False else 'full'
	print(f'\nYour current setting is set to: {Fore.LIGHTGREEN_EX}{length}{Fore.RESET}')
	k = input('What do you want to change it setting to? \'Full\' for full game names or \'short\' for shortened game names ')
	k = k.lower()
	if k in ['full', 'f']:
		config.update('fname', True)
		log.info(f'Set game name to {Fore.LIGHTGREEN_EX}Full{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen(True)
	elif k in ['short', 's']:
		config.update('fname', False)
		log.info(f'Set game name to {Fore.LIGHTGREEN_EX}Short{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen(True)


def changeAutoUpdate():
	print(f'\nYour current Auto Update setting is set to {Fore.LIGHTGREEN_EX}{autoupdate}{Fore.RESET}')
	ask = input('What would you like to change it to? On or off? ')
	ask = ask.lower()
	if ask == 'on':
		config.update('auto-update', True)
		log.info(f'Set Auto Update setting to {Fore.LIGHTGREEN_EX}True{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen(True)
	elif ask == 'off':
		config.update('auto-update', False)
		log.info(f'Set Auto Update setting to {Fore.LIGHTRED_EX}False{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen(True)
	else:
		log.error('Keeping auto update setting the same since you did not answer correctly')


def addFavorite():
	favask = input('Would you like to add or remove a favorite? ')
	if favask in ['remove', 'r']:
		if not favorites:
			log.info('Your favorite list is currently empty', True)
		rask = input('What game would you like to remove from your favorites? ')
		if rask not in favorites:
			log.info(f'{rask} is currently not in your favorite list', True)
		favorites.remove(rask)
		config.update('favorites', favorites)
		log.info(f'Successfully removed {rask} from your favorite list', True)
	else:
		addask = input('What game would you like to add to your favorites? ')
		favorites.append(addask)
		config.update('favorites', favorites)
		log.info(f'Successfully added {addask} to your favorite list', True)


def form():
	log.info('Opening the form...', False)
	webbrowser.open('https://forms.gle/ofCZ8QXQYxPvTcDE7', new=2, autoraise=True)
	log.info('Form is now open! Thanks for being willing to fill out the form!', True)


def shortcut(game: int, favs) -> int:
	for i in range(len(favs)):
		if i + 1 == game:
			return favs[i]
	log.error('You don\'t have that many favorites in your favorite list. Use the \'shortcut\' command to figure out how shortcuts work')


#+= looking for game status before picking a game =+#
log.loading('Attempting to set looking for game status...', 'yellow')
startTime = time.time()
if showbutton:
	RPC.update(large_image='switch_png', large_text='Searching for a game', details='Searching for a game',
				buttons=[{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}], start=startTime)
elif showbutton is False:
	RPC.update(large_image='switch_png', large_text='Searching for a game', details='Searching for a game', start=startTime)
log.loading('Successfully set looking for game status!', 'green')

#+= home page =+#
changeWindowTitle('Picking a game')
clear()
print('''
 .d8888b.                d8b 888             888                                          
d88P  Y88b               Y8P 888             888                                          
Y88b.                        888             888                                          
 "Y888b.   888  888  888 888 888888  .d8888b 88888b.   .d88b.  88888b.   .d8888b  .d88b.  
    "Y88b. 888  888  888 888 888    d88P"    888 "88b d8P  Y8b 888 "88b d88P"    d8P  Y8b 
      "888 888  888  888 888 888    888      888  888 88888888 888  888 888      88888888 
Y88b  d88P Y88b 888 d88P 888 Y88b.  Y88b.    888  888 Y8b.     888  888 Y88b.    Y8b.     
 "Y8888P"   "Y8888888P"  888  "Y888  "Y8888P 888  888  "Y8888  888  888  "Y8888P  "Y8888    
Made by: Aethese
''')

#+= handle announcement and tips =+#
if announcement not in [None, '']:
	print(f'{Fore.LIGHTCYAN_EX}[Announcement]{Fore.RESET} {announcement}')
print(f'{Fore.LIGHTCYAN_EX}[Tip]{Fore.RESET} {random.choice(tips)}\n')

#+= handle new update =+#
if updateAvailable:
	if autoupdate:
		log.info('New update found, updating to latest version...', False)
		time.sleep(1)
		updateProgram(oVersion)
	if updatenotifier:  # this will show if auto updates aren't on
		log.info(f'Your current version of Switchence {Fore.LIGHTRED_EX}v{version}{Fore.RESET} is not up to date', False)
		log.info(f'You can update Switchence to the current version {Fore.LIGHTRED_EX}v{oVersion}{Fore.RESET} by turning on Auto Updates or by visiting the official GitHub page', False)
		log.info('If you wish to turn on auto updates type \'auto update\' below', False)
		log.info('If you wish to turn off update notifications, type \'update notifier\' below', False)
		log.info('If you want to visit the GitHub page to update to the latest version type \'github\' below\n', False)
		time.sleep(1)

#+= pick game =+#
print('Here are the current games:')
if favorites:
	favorites.sort()  # sort alphabetically
	print(Fore.LIGHTYELLOW_EX+', '.join(favorites))
if configfname is False:
	print(Fore.WHITE+', '.join(gamenames))  # reset yellow color from above
else:
	print(Fore.WHITE+', '.join(gamefnames)) # reset yellow color from above
initializeTime = time.time() - initializeTime
x = input('\nWhat game do you wanna play? ')
x = x.lower()

#+= input options =+#
if x in ['github', 'gh', 'g']:
	log.info('Opening GitHub page...', False)
	time.sleep(1)
	webbrowser.open('https://github.com/Aethese/Switchence/', new=2, autoraise=True)
	log.info('GitHub page opened', True)
elif x in ['update notifier', 'update-notifier', 'un', 'u-n']:
	changeUpdateNotifier()
elif x in ['change name', 'change-name', 'cn', 'c-n']:
	changeFNameSetting()
elif x in ['auto update', 'auto-update', 'au', 'a-u']:
	changeAutoUpdate()
elif x in ['initialize', 'init', 'i']:
	log.info(f'Time Switchence took to initialize: {initializeTime}', True)
elif x in ['favorite', 'f']:
	addFavorite()
elif x == 'form':
	form()
elif x in ['shortcut', 'shortcuts', 's']:
	log.info(f'''You currently have {Fore.LIGHTRED_EX}{len(favorites)}{Fore.RESET} favorites in your favorite list
Let\'s say you want to pick the first one, just type {Fore.LIGHTRED_EX}1{Fore.RESET} to pick your first favorite''', True)
elif x in ['discord', 'd']:
	log.info('Opening Discord server link...', False)
	time.sleep(1)
	webbrowser.open('https://discord.gg/238heBqmZb', new=2, autoraise=True)
	log.info('Discord server link opened!', True)
elif x in ['options', 'o']:
	log.info(f'''The current options are:
\'github\' this will bring up the public GitHub repo
\'discord\' this will bring up the public Discord server
\'update notifier\' which toggles the built-in update notifier, this is set to {Fore.LIGHTCYAN_EX}{updatenotifier}{Fore.RESET}
\'change name\' this will toggle how game names are shown on the game select screen, this is set to {Fore.LIGHTCYAN_EX}{configfname}{Fore.RESET}
\'auto update\' which toggles the built-in auto updater, this is {Fore.LIGHTCYAN_EX}{autoupdate}{Fore.RESET}
\'initialize\' this will let you know how long it took Switchence to initialize
\'favorite\' this will let you favorite a game show it shows up 
\'form\' this will bring up the Google form that has questions related to Switchence (please fill it out!)
\'shortcut\' this will tell you how shortcuts work
\'options\' this will bring up this page''', True)

#+= sw handling =+#
y = input(f'Do you want to show your friend code, SW-{sw} (you can change this by typing \'change\')? ')
y = y.lower()
if y in ['yes', 'y']:
	if sw in [None, '']:
		log.info('Friend code not set, continuing with setting set to off', False)
		y = 'n'
elif y in ['change', 'c']:
	c = input('What is your new friend code (just type the numbers)? ')
	b = input(f'Is \'SW-{c}\' correct? ')
	b = b.lower()
	if b in ['yes', 'y']:
		config.update('sw-code', c)
		sw = c
		log.info(f'Friend code changed to SW-{c}', False)
		y = 'y'
	else:
		log.info('Friend code not changed, continuing with setting set to off', False)
		y = 'n'

#+= search for game =+#
try:
	xInt = int(x)
except ValueError:
	xInt = None
if isinstance(xInt, int):  # for shortcuts
	x = shortcut(xInt, favorites)
for n in games['games']:
	z = n['name']
	o = n['fname']
	if z.lower() == x:
		chosenOne = z
		break
	elif o.lower() == x:
		chosenOne = o
		break
else:
	log.info(f'The game you specified, {Fore.LIGHTGREEN_EX}{x}{Fore.RESET}, is not in the current game list', True)

#+= send info to changePresence function about game picked =+#
for i in games['games']:
	if chosenOne in [i['name'], i['fname']]:
		img = i['name']  # the short game name is the same as the img name
		fname = i['fname']
		if y in ['yes', 'y']:
			changePresence(True, img, fname)
			break
		changePresence(False, img, fname)  # sw code showing is off
		break

#+= just needed, trust me =+#
while True:
	time.sleep(15)
