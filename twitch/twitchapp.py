import json
from pathlib import Path

import aiohttp
from typing import Union


class StatusError(Exception):
    """Raised if response status isn't 200 or 401"""

    def __init__(self, response):
        self.status = response['status']
        self.error = response['error']
        self.message = response['message']

    def __str__(self):
        return f"\n{self.error}: {self.status}\n{self.message}"


class TwitchApp:

    def __init__(self, client_id: str, client_secret: str):
        """
        Starts a Twitch session with the given client
        :param client_id: The id of your Twitch app
        :param client_secret: The secret of your Twitch app
        """
        self.session = aiohttp.ClientSession()
        self.base_data = {"client_id": client_id,
                          "client_secret": client_secret,
                          "grant_type": "client_credentials"}
        self.header = None
        try:
            self.tags = json.load(open('./tags.json', 'r', encoding='utf-8'))
        except FileNotFoundError:
            Path('.').mkdir(parents=True, exist_ok=True)
            with open('./tags.json', encoding='utf-8', mode="w") as f:
                json.dump({}, f, indent=4, sort_keys=True, separators=(',', ' : '))
            self.tags = {}

    async def __aenter__(self):
        await self.__token()
        return self

    async def __aexit__(self, *execinfo):
        if not self.session.closed:
            await self.session.close()

    async def __token(self):
        """
        Gets a new Twitch app token
        :return:
        """
        token = await self.session.post('https://id.twitch.tv/oauth2/token', data=self.base_data)
        async with token:
            assert token.status == 200, f"Status: {token.status}, {(await token.json())['message']}"
            self.header = {"Authorization": f"Bearer {(await token.json())['access_token']}",
                           "Client-ID": self.base_data['client_id']}
        return

    async def __error_check(self, status, url, response):
        """
        Checks if the request was unauthorized.
        If yes it get's a new token else it raises an error.
        :param status: status of the request
        :param url: url of the request
        :param response: response of the request
        :return:
        """
        if status == 401:
            await self.__token()
            return await self.session.get(url, headers=self.header)
        else:
            raise StatusError(await response.json())

    async def user(self, users: Union[list, str]):
        """
        Search after one or more Twitch users
        :param users: Name/s of the user/s
        :return:
        """
        users = users if type(users) is list else [users]
        user_response = []
        for i in range(int(len(users) / 100) + 1):
            query = "&".join(f"login={user}" for user in users[100 * i:100 * (i + 1)])
            url = f'https://api.twitch.tv/helix/users?{query}'
            part_user = await self.session.get(url, headers=self.header)
            async with part_user:
                if not part_user.status == 200:
                    part_user = await self.__error_check(part_user.status, url, part_user)
                part_user = await part_user.json()
                user_response.extend(part_user['data'])
        return user_response

    async def stream(self, streamers: Union[list, str]):
        """
        Searches after one or more Twitch streams that are live
        :param streamers: Name/s of the streamer
        :return:
        """
        streamers = streamers if type(streamers) is list else [streamers]
        streams = []
        for i in range(int(len(streamers) / 100) + 1):
            query = "&".join(f"user_login={streamer}" for streamer in streamers[100 * i:100 * (i + 1)])
            url = f'https://api.twitch.tv/helix/streams?{query}'
            part_streams = await self.session.get(url, headers=self.header)
            async with part_streams:
                if not part_streams.status == 200:
                    part_streams = await self.__error_check(part_streams.status, url, part_streams)
                part_streams = await part_streams.json()
                streams.extend(part_streams['data'])
        return streams

    async def tag(self, tags: Union[list, str]):
        """
        Searches after one or more Twitch tags
        :param tags: tag ID of one or more
        :return:
        """
        tags = tags if type(tags) is list else [tags]
        tag_unkown = []
        tag_response = []
        for tag in tags:
            if str(tag) in self.tags:
                tag_response.append(self.tags[tag])
            else:
                tag_unkown.append(tag)
        if len(tag_unkown) != 0:
            for i in range(int(len(tag_unkown) / 100) + 1):
                query = "&".join(f"tag_id={tag}" for tag in tag_unkown[100 * i:100 * (i + 1)])
                url = f'https://api.twitch.tv/helix/tags/streams?{query}'
                part_tags = await self.session.get(url, headers=self.header)
                async with part_tags:
                    if not part_tags.status == 200:
                        part_tags = await self.__error_check(part_tags.status, url, part_tags)
                    part_tags = await part_tags.json()
                    for tag in part_tags['data']:
                        self.tags[tag['tag_id']] = tag
                    tag_response.extend(part_tags['data'])
        with open('./tags.json', 'w') as file:
            json.dump(self.tags, file)
        return tag_response

    async def game(self, games: Union[list, str]):
        """
        Searches after one or more games on Twitch
        :param games: Name/s of the game/s
        :return:
        """
        games = games if type(games) is list else [games]
        response_games = []
        for i in range(int(len(games) / 100) + 1):
            query = "&".join(f"name={game}" for game in games[100 * i:100 * (i + 1)])
            url = f'https://api.twitch.tv/helix/games?{query}'
            part_games = await self.session.get(url, headers=self.header)
            async with part_games:
                if not part_games.status == 200:
                    part_games = await self.__error_check(part_games.status, url, part_games)
                part_games = await part_games.json()
                response_games.extend(part_games['data'])
        return response_games

    async def top_games(self):
        """
        Searches after the top games on Twitch of the moment
        :return:
        """
        url = f'https://api.twitch.tv/helix/games/top'
        top_games = await self.session.get(url, headers=self.header)
        async with top_games:
            if not top_games.status == 200:
                top_games = await self.__error_check(top_games.status, url, top_games)
            top_games = await top_games.json()
        return top_games['data']
