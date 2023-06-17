import asyncio
import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
from config import token
from test import morph

from main import check_news_update

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

def get_json(ner, date):
    dict_news = list()

    with open("news_dict.json", "r", encoding="utf-8") as read_file:
        data = json.load(read_file)
        day = None
        month = None
        year = None
        print('gf')
        for new in data.keys():
            ner_tec, _ = morph(str(data[new]['article_full_desc']))
            _, data_tec = morph(str(data[new]['article_data']))
            c = True
            for n in ner:
                if n not in ner_tec:
                    c = False
            if len(date) != 0:
                day = date.day
                month = date.month
                year = date.year
            for d in data_tec:
                if day is not None and day != d.day:
                    c = False
                if month is not None and month != d.day:
                    c = False
                if year is not None and year != d.day:
                    c = False
            if c == True:
                dict_news.append([data[new]['article_data'], data[new]['article_full_desc']])
                print(dict_news)
    return dict_news




@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def process_text_message(message: types.Message):
    text,r=morph(message.text)
    list_news = get_json(text,r)
    print(list_news)
    for news in list_news:
        result = str(news[0]) + "\n" + str(news[1])
        await message.answer(result)
    else:
        await message.answer("Нет таких новостей")



    await message.answer("1")



# @dp.message_handler(Text(equals="Сводка"))
# async def get_news_summary(message: types.Message):
#     with open("news_dict.json",encoding="utf-8") as file:
#         news_dict = json.load(file)
#
#     for k, v in sorted(news_dict.items())[-5:]:
#         text = prediction(message.text)



if __name__ == '__main__':
    executor.start_polling(dp)






