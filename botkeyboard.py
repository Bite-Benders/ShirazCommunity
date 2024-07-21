from asgiref.sync import sync_to_async
from telebot import types
import telebot
import os 
import django 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shirazcommunitybot.settings")
django.setup()

class Keyboard:
    @staticmethod
    async def main_menu():
        main_menu = telebot.types.InlineKeyboardMarkup(row_width=2)
        bottons = [
            telebot.types.InlineKeyboardButton('صدا میخوام کنم📢', callback_data='mention_button'),
        ]
        main_menu.add(*bottons)
        return main_menu





    @staticmethod
    async def mention(user_categories, group_user_name):
        mentions_menu = telebot.types.InlineKeyboardMarkup(row_width=2)
        mentions_buttons = [
            telebot.types.InlineKeyboardButton(group_user_name, callback_data='mention_all_button'),
        ]
        user_categories = await sync_to_async(list)(user_categories)
        for user_category in user_categories:
            category_name = await user_category.get('category_name')
            category_id = await user_category.get('id')
            callback_data = f'{{"act": "mention", "id": {category_id}}}'
            mentions_buttons.append(telebot.types.InlineKeyboardButton(category_name, callback_data=callback_data))
        mentions_buttons.append(telebot.types.InlineKeyboardButton('🔙برگردیم عقب', callback_data='back_button'))
        mentions_menu.add(*mentions_buttons)
        return mentions_menu



    @staticmethod
    async def wrong_mention():
        wrong_mention_menu = telebot.types.InlineKeyboardMarkup(row_width=1)
        wrong_mention_button = telebot.types.InlineKeyboardButton('🔙اشتباه منشن کردی؟', callback_data='mention_button')
        wrong_mention_menu.add(wrong_mention_button)
        return wrong_mention_menu


    @staticmethod
    async def back_button():
        back_menu = telebot.types.InlineKeyboardMarkup(row_width=1)
        back_button = [
            telebot.types.InlineKeyboardButton('برگردیم عقب🔙', callback_data='back_button'),
        ]
        back_menu.add(*back_button)
        return back_menu





