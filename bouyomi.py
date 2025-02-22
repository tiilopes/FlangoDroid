import re

import aiohttp
from twitchio import Message

import config_bot



class Bouyomi:
    def __init__(self):
        self.port = int(config_bot.bouyomi_port)
        self.bot_content = config_bot.bouyomi_bot_content
        self.listener_content = config_bot.bouyomi_content
    
    async def bouyomi(self, message: Message, formated_msg):
        
        msg = message.content
        display_name = message.author.display_name
        login_id = message.author.name
        
        if re.search('{raw_msg}', self.listener_content):
            bouyomi_message = self.listener_content.format(sender_name=login_id, sender_disp=display_name, raw_msg=msg, emote_del_msg=formated_msg)
            await self.bouyomi_send(bouyomi_message)
        
        elif re.search('{emote_del_msg}', self.listener_content):
            if not formated_msg:
                return
            bouyomi_message = self.listener_content.format(sender_name=login_id, sender_disp=display_name, raw_msg=msg, emote_del_msg=formated_msg)
            await self.bouyomi_send(bouyomi_message)
        
        else:
            bouyomi_message = self.listener_content.format(sender_name=login_id, sender_disp=display_name, raw_msg=msg, emote_del_msg=formated_msg)
            await self.bouyomi_send(bouyomi_message)

    async def bouyomi_bot(self, message: Message, translated, disp_name, login):
        
        bouyomi_message = self.bot_content.format(bot_name=login, bot_disp=disp_name, msg=translated, sender_name=message.author.name, sender_disp=message.author.display_name)
        await self.bouyomi_send(bouyomi_message)
    
    async def bouyomi_send(self, msg):
        params = {'text':msg}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get('http://localhost:{}/Talk'.format(self.port), params=params, timeout=0.5) as res:
                    if res.status == 200:
                        pass
            except Exception as e:
                print('棒読みちゃんに接続できませんでした...')
                print(e)
