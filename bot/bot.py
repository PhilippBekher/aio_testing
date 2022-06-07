# amazing_project
import logging

import psycopg2
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from bot.settings import (BOT_TOKEN, HEROKU_APP_NAME,
                          WEBHOOK_URL, WEBHOOK_PATH,
                          WEBAPP_HOST, WEBAPP_PORT, DB_URL)
import datetime, time
from db import database

# db_connection = psycopg2.connect( DB_URL, sslmode = "require")
# db_object = db_connection.cursor()


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    logging.warning(f'Recieved a message from {message.from_user}')

    id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.first_name + ' ' + message.from_user.last_name
    chat_id = message.chat.id

    await database.execute(f"SELECT id FROM users WHERE id = {id}")
    result = database.fetchone()
    message_time = message.date
    unix_time_stamp = time.time()
    await bot.send_message(chat_id,result[0])



# @dp.message_handler(commands=["start"])
# async def start(message: types.Message):
#     logging.warning(f'Recieved a message from {message.from_user}')
#
#     id = message.from_user.id
#     username = message.from_user.username
#     fullname = message.from_user.first_name + ' ' + message.from_user.last_name
#     chat_id = message.chat.id
#
#     db_object.execute(f"SELECT id FROM users WHERE id = {id}")
#     result = db_object.fetchone()
#     message_time = message.date
#     unix_time_stamp = time.time()
#
#     if not result:
#         questions = db_object.execute("SELECT * FROM questions")
#         question_records = db_object.fetchall()
#         await bot.send_message(message.chat.id,
# f"""Hello👋🏼
# I'm going to take you through {len(question_records)} questions to find out your English level 📚🎓
# Please be patient and carefully reply to all the questions🙏🏼
# The test will take no more than 20 minutes😊
# Good luck🤞🏼""")
#
#         db_object.execute(
#             "INSERT INTO users(id, username, current_exercise, fullname, right_answers_number, chat_id, last_message_time, unix_timestamp ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
#             (id, username, 1, fullname, 0, chat_id, message_time,unix_time_stamp ))
#         db_object.execute("SELECT * FROM questions WHERE question_id = 1 ")
#         first_question = db_object.fetchone()
#
#         keyboard = ReplyKeyboardMarkup( resize_keyboard=True,one_time_keyboard=True).row(f'{first_question[1]}', f'{first_question[2]}', f'{first_question[3]}', f'{first_question[4]}')
#         await bot.send_message(message.chat.id,
# f"""{first_question[6]}. Fill in the gap:
# {first_question[0]}""", reply_markup=keyboard )
#
#         db_connection.commit();
#


# @dp.message_handler(content_types=['text'])
# async def after_text(message):
#     questions = db_object.execute("SELECT * FROM questions")
#     question_records = db_object.fetchall()
#     print(question_records)
#     message_time = message.date
#     unix_time_stamp = time.time()
#     id = message.from_user.id
#
#     db_object.execute(f"UPDATE users SET last_message_time = %s WHERE id = {id}",(message_time,))
#     db_connection.commit()
#     db_object.execute(f"UPDATE users SET unix_timestamp = %s WHERE id = {id}", (unix_time_stamp,))
#     db_connection.commit()
#
#
#     db_object.execute(f"SELECT current_exercise, right_answers_number FROM users WHERE id = {id}")
#     result = db_object.fetchone()
#     if(result[0] == 100):
#         return
#
#     current_exercise_right_answer = db_object.execute(f"SELECT right_answer FROM questions WHERE question_id = {result[0]}")
#     right_answer_object = db_object.fetchone()
#     if ((message.text == right_answer_object[0]) ):
#           current_right_answers_number = result[1] + 1
#           db_object.execute(f"UPDATE users SET right_answers_number = %s WHERE id = {id}",
#           (current_right_answers_number,))
#           db_connection.commit();
#
#     if result[0] == len(question_records):
#             current_right_answers_number_object = db_object.execute(f"SELECT right_answers_number FROM users WHERE id = {id}")
#             current_right_answers_number_object_fetched = db_object.fetchone()
#             db_connection.commit();
#
#             level = ''
#             percent_of_right_answers = current_right_answers_number_object_fetched[0]/len(question_records)
#
#             if 0 <= percent_of_right_answers <= 0.17:
#                 level = 'Beginner'
#             elif 0.17 < percent_of_right_answers <= 0.37:
#                 level = 'Elementary'
#             elif 0.37 < percent_of_right_answers <= 0.53:
#                 level = 'Pre-Intermediate'
#             elif 0.53 < percent_of_right_answers <= 0.73:
#                 level = 'Intermediate'
#             elif 0.73 < percent_of_right_answers <= 0.9:
#                 level = 'Upper-Intermediate'
#             else:
#                 level = 'Advanced'
#
#             await bot.send_message(message.chat.id,
# f"""Thank you for taking the test😊
# Number of right answers is: { current_right_answers_number_object_fetched[0] }
# Your level is: {level}
# We'll contact you very soon🙂""")
#             db_object.execute(f"UPDATE users SET level = %s WHERE id = {id}", (level,))
#             db_connection.commit()
#
#             db_object.execute(f"UPDATE users SET current_exercise = %s WHERE id = {id}", (100,))
#             db_connection.commit()




#     if result[0] < len(question_records):
#         next_exercise_id = result[0] + 1
#         db_object.execute(f"SELECT * FROM questions WHERE question_id = {next_exercise_id}")
#         next_exercise = db_object.fetchone()
#         db_object.execute(f"UPDATE users SET current_exercise = %s WHERE id = {id}", (next_exercise_id,))
#
#         keyboard = ReplyKeyboardMarkup(
#             one_time_keyboard=True, resize_keyboard = True
#         ).row(f'{next_exercise[1]}', f'{next_exercise[2]}', f'{next_exercise[3]}', f'{next_exercise[4]}')
#
#         await bot.send_message(message.chat.id,
# f"""{next_exercise[6]}. Fill in the gap:
# {next_exercise[0]}""", reply_markup=keyboard)
#
#     db_connection.commit()








async def on_startup(dp):
    await database.connect()
    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)


async def on_shutdown(dp):
    await database.disconnect()
    logging.warning('Bye! Shutting down webhook connection')


def main():
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
