import telebot
from telebot import types
import db_rabota
import datetime
import json
from config import TOKEN
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        msg = 'Начало работы'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        review = types.KeyboardButton("Посмотреть задания")
        #markup.add(update_reviwes)
        markup.add(review)
        bot.send_message(message.chat.id,msg, reply_markup=markup)
    except Exception as ex:
        print(f"Error start, {ex}")


@bot.message_handler(content_types=['text'])
def func(message):
    try:
        if (message.text == "Посмотреть задания"):
            all_review = db_rabota.get_review_for_rewriting()
            if len(all_review) == 0:
                bot.send_message(message.chat.id, 'Отзывов на переписывание нет')
            else:
                for i in db_rabota.get_review_for_rewriting():
                    bot.send_message(message.chat.id, f"{i[0]}\n{i[4]}\n{i[5]}\n{i[6]}\n{i[1]}")
        else:
            message_reply_id = message.reply_to_message.id
            review_id = message.reply_to_message.text
            review_id = review_id.split('\n', maxsplit = 1)[0]
            new_review = message.text
            db_rabota.update_review_for_rewriting(review_id, new_review)
            #bot.edit_message_text(chat_id=message.chat.id,message_id=message_reply_id, text=f'Отзыв #{review_id} изменён')
            bot.delete_message(message.chat.id,message.id)
            bot.delete_message(message.chat.id, message_reply_id)
    except Exception as ex:
        print(f"Error text, {ex}")



def main():
    
    print ('bot rolling')
    bot.polling(none_stop=True)
    #by valek
try:
    if __name__ == '__main__':
        main()
except Exception as ex:
    print(ex)
    main()