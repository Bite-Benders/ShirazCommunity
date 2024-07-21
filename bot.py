import os
import asyncio
import django
from asgiref.sync import sync_to_async
from telebot.async_telebot import AsyncTeleBot
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shirazcommunitybot.settings")
django.setup()
from bot_utiles import *
from botkeyboard import Keyboard
# bot token
bot = AsyncTeleBot('')
import requests
import random
import aiohttp
import json
import time
import telebot
from group.models import *

# greeting to new users
@bot.message_handler(content_types=['new_chat_members'])
async def greet_new_members(message):
    for new_member in message.new_chat_members:
        await bot.send_message(message.chat.id, f"به تیم خودت خوش اومدی ! {new_member.first_name}")


# main menu commend hanndeler
@bot.message_handler(commands=['menu'])
async def menu(message):
    # if in group update the users and admins
    if message.chat.type == 'supergroup' or message.chat.type == 'group':

        group = await get_group_from_message(message)
        if await group.get('is_active'):

            user = await get_user_from_message(message)
            await sync_to_async(add_user_to_group)(user, group)
        admins = await bot.get_chat_administrators(message.chat.id)
        admin_list = []
        for admin in admins:
            user, shit_variable = await sync_to_async(User.objects.get_or_create)(user_id=admin.user.id,
                                                                                  defaults={
                                                                                      'username': admin.user.username or admin.user.first_name + "(first_name)",
                                                                                      "name": admin.user.first_name})
            admin_list.append(user)
        await sync_to_async(group.users.add)(*admin_list)
    return await bot.reply_to(message, 'menu',
                              reply_markup=await Keyboard.main_menu())

@bot.callback_query_handler(func=lambda call: 'act' in call.data)
async def action_callback(call):
    data = json.loads(call.data)
    action = data['act']
    match action:
        case 'mention':
            group = await get_group_from_message(call.message)
            user_category = await sync_to_async(UserCategory.objects.filter)(pk=data['id'])
            user_category = await sync_to_async(list)(user_category)
            user_category = user_category[0]
            users = await sync_to_async(user_category.users.all)()
            user_category_name = await user_category.get('category_name')
            mention = f'{user_category_name}\n'
            users = await sync_to_async(list)(users)
            for user in users:
                mention += await tag_user(user) + ' '
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id,)
            thread_id = call.message.message_thread_id if hasattr(call.message, 'message_thread_id') else None
            message_params = {}
            if thread_id != None:
                message_params = {'message_thread_id': thread_id}
            try:
                return await bot.send_message(
                    chat_id=call.message.chat.id,
                    text=mention,
                    reply_markup=await Keyboard.wrong_mention(),
                    parse_mode='Markdown',
                    **message_params
                )
            except:
                return await bot.send_message(
                    chat_id=call.message.chat.id,
                    text=mention,
                    reply_markup=await Keyboard.wrong_mention(),
                    parse_mode='Markdown',
                ) 





@bot.callback_query_handler(func=lambda call: True)
async def handle_button_click(call):
    match call.data:
        case 'back_button':
            return await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='main menu',reply_markup=await Keyboard.main_menu())

        case 'mention_button':
            group = await get_group_from_message(call.message)
            group_user_name = await group.get('users_name')
            user_categorys = UserCategory.objects.filter(group=group)
            return await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="کیا رو صدا کنم ؟؟📢📢",
                                  reply_markup=await Keyboard.mention(group_user_name=group_user_name or '👨‍👩‍👦‍👦منشن همه', user_categories=user_categorys))
        case 'mention_all_button':
            group = await get_group_from_message(call.message)
            users = await sync_to_async(group.users.all)()
            mention = 'منشن همه\n'
            users = await sync_to_async(list)(users)
            for user in users:
                mention += await tag_user(user) + ' '
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id,)
            return await bot.send_message(
                chat_id=call.message.chat.id,
                text=mention,
                reply_markup=await Keyboard.wrong_mention(),
                parse_mode='Markdown'
            )



# saving only the users that are in the groups that has is active on
@bot.message_handler(content_types=['text'])
async def message_controler(message):
    group = await get_group_from_message(message)
    if await group.get('is_active'):
        user = await get_user_from_message(message)
        await sync_to_async(add_user_to_group)(user, group)
        user.message_count += 1
        await sync_to_async(user.save)()



async def main():
    await bot.polling()


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            break
        except Exception as e:
            time.sleep(5)
            print(f'error {e}')
    exit()

