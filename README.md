# TwitchAPI Wrapper
A Twitch Wrapper for Python 3.6 or higher for the new Twitch API with its App Token
### Installation
```
pip install twitch-MagicaFreak
```
## Getting Started
To start a session with Twitch you just use:
```
from twitch.twitch import Twitch

async with Twitch("client_id","client_secret") as example_name:
```
Now to get something from the Twitch App you just use your name and the function you want.
As an example:
```
from twitch.twitch import Twitch

async with Twitch("client_id","client_secret") as example_name:
    await example_name.user('MagicaFreak')
```

##Functions
All the functions that exist at the moment

### Twitch User
It gets the user by his username
```
from twitch.twitch import Twitch

async with Twitch("client_id","client_secret") as example_name:
    await example_name.user('Username')
```
This can be done for multiple users too
```
from twitch.twitch import Twitch

async with Twitch("client_id","client_secret") as example_name:
    await example_name.user(['Username1', 'Username2', 'Username3'])
```
And it returns a list of users that you searched for

### Twitch Stream
It gets the stream that is live by the name of the streamer
```
from twitch.twitch import Twitch

async with Twitch("client_id","client_secret") as example_name:
    await example_name.stream('Streamername')
```
This can be done for multiple streams too
```
from twitch.twitch import Twitch

async with Twitch("client_id","client_secret") as example_name:
    await example_name.stream(['Streamername1', 'Streamername2', 'Streamername3'])
```
And it returns a list of streams that you searched for

### Twitch Tags
It gets the tag by the tag ID
```
from twitch.twitch import Twitch

async with Twitch("client_id","client_secret") as example_name:
    await example_name.tag('tag ID')
```
This can be done for multiple tags too
```
from twitch.twitch import Twitch

async with Twitch("client_id","client_secret") as example_name:
    await example_name.tag(['tagID1', 'tagID2', 'tagID3'])
```
And it returns a list of tags that you searched for

### Twitch game
It gets the game by its name
```
from twitch.twitch import Twitch

async with Twitch("client_id","client_secret") as example_name:
    await example_name.game('game name')
```
This can be done for multiple games too
```
from twitch.twitch import Twitch

async with Twitch("client_id","client_secret") as example_name:
    await example_name.game(['gamename1', 'gamename2', 'gamename3'])
```
And it returns a list of the games that you searched for

### Twitch Top Games
It gets the top games of the moment
```
from twitch.twitch import Twitch

async with Twitch("client_id","client_secret") as example_name:
    await example_name.top_games()
```
And it returns a list of the top games