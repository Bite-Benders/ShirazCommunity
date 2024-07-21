import os
import asyncio
import django
from asgiref.sync import sync_to_async
from telebot.async_telebot import AsyncTeleBot
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shirazcommunitybot.settings")
django.setup()
from botkeyboard import Keyboard
import aiohttp
import telebot
from group.models import *


async def get_group_from_message(message, exist_data=False):
    if message.chat.type in ['supergroup', 'group', 'channel']:
        group, created = await sync_to_async(Group.objects.get_or_create)(
            chat_id=message.chat.id,
            defaults={'title': message.chat.title}
        )
    else:
        group, created = await sync_to_async(Group.objects.get_or_create)(
            chat_id=1, defaults={'title': 'چت دیفالت',}
        )
    if exist_data:
        return group, created
    else:
        return group


async def get_user_from_message(message):
    if message.from_user.last_name:
        name = message.from_user.first_name + " " + message.from_user.last_name
    else:
        name = message.from_user.first_name
    user, shit_variable = await sync_to_async(User.objects.get_or_create)(
        user_id=message.from_user.id,
        defaults={'username': message.from_user.username or message.from_user.first_name + "(first_name)",
                  "name": name}
    )
    return user

def add_user_to_group(user, group):
    if not group.users.filter(pk=user.pk).exists():
        group.users.add(user)