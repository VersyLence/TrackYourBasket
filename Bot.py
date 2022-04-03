from discord.ext import commands
import discord
from settings import a
import requests
from bs4 import BeautifulSoup
from getpass import getpass
from mysql.connector import *
from math import *
from datetime import date

bot = commands.Bot(command_prefix = a['pref'])

@bot.command()
async def info(ctx):
    await ctx.send(f'+-weather [Country] [City], \n+-hello \n+-cost \n+-BD')


@bot.command()
async def hello(ctx): #hello - название команды ctx - контекст всего
    author = ctx.message.author #Создание переменной с пользователем

    await ctx.send(f'Hello, {author.mention}!') #mention - упоминание send - отправить

@bot.command()
async def weather(ctx, country:str,city:str): #hello - название команды ctx - контекст всего
    countryl=country.lower()
    cityl=city.lower()
    url = 'https://world-weather.ru/pogoda/'+countryl+'/'+cityl+'/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    weather = soup.find_all('div', class_='weather-now horizon')
    temprature = weather[0].find('div', id='weather-now-number')
    additional = weather[0].find(id='weather-now-description').find_all('dd')

    await ctx.send(f'Погода в {city.capitalize()}:\nТемпература: {temprature.text}.\nОщущается как: {additional[0].text}.\nВлажность:{additional[2].text}.')

@bot.command()
async def cost(ctx):
    lists = ['https://eda.yandex.ru/retail/omsk/magnit/catalog/19280?placeSlug=magnit_sazonova_33','https://eda.yandex.ru/retail/omsk/lenta/catalog/19280?placeSlug=lenta_vpmtc','https://eda.yandex.ru/retail/omsk/ashan_gipermarket/catalog/19280?placeSlug=ashan_gipermarket_bulvar_arxitektorov_35','https://eda.yandex.ru/retail/omsk/magnit/catalog/21661?placeSlug=magnit_sazonova_33','https://eda.yandex.ru/retail/omsk/lenta/catalog/21661?placeSlug=lenta_vpmtc', 'https://eda.yandex.ru/retail/omsk/ashan_gipermarket/catalog/21661?placeSlug=ashan_gipermarket_bulvar_arxitektorov_35']
    list2 = ['Milk','Milk','Milk','Pasta', 'Pasta','Pasta']
    list3 = ['Magnit','Lenta', 'Auchan','Magnit','Lenta', 'Auchan']
    numbers = [1,6,8,1,2,3]
    datet =  date.today()
    date1 = str(datet)
    date1 = date1[:5]+ date1[6:]
    for i in range(len(lists)):
        url=lists[i]
        response=requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        step1 = soup.find_all('span', class_='UiKitPrice_price UiKitPrice_l UiKitPrice_medium')
        step2 = step1[numbers[i]]
        await ctx.send(f'Цена {list2[i]} ({list3[i]}): {step2.text}')
        s=step2.text
        try:
            with connect(
                host="localhost",
                user='root',
                password='megivan25',
                database="rating",
            )as connection: 
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id FROM cost WHERE shop = '%s'" % date1)
                    _lastUpdateResult = cursor.fetchall()
                    if (_lastUpdateResult == []):
                        for i in range(len(lists)):
                            cursor.execute("INSERT INTO cost (title, price, date, shop) VALUES (%s, %s, %s, %s)", (list2[i], list3[i], s[:2]+' p', datet))   #price = Название магазина  shop - дата
                    connection.commit()
        except Error as e:
            print(e)


@bot.command()
async def BD(ctx):
    try:
        with connect(
            host="localhost",
            user='root',
            password='megivan25',
            database="rating",
        )as connection:
            select_query = "SELECT * FROM cost"
            with connection.cursor() as cursor:
                cursor.execute(select_query)
                result = cursor.fetchall()
                for row in result:
                    await ctx.send(row)

    except Error as e:
        print(e)


@bot.command()
async def clear(ctx):
    try:
        with connect(
            host="localhost",
            user='root',
            password='megivan25',
            database='rating'
        ) as connection:
            insert_movies_query = """
            DELETE FROM cost"""
            delet = " ALTER TABLE cost AUTO_INCREMENT=0"
            with connection.cursor() as cursor:
                cursor.execute(insert_movies_query)
                cursor.execute(delet)
                connection.commit()

    except Error as e:
        print(e)


@bot.command() 
async def comp(ctx, product:str):
    try:
        with connect(
            host="localhost",
            user='root',
            password='megivan25',
            database='rating'
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM cost WHERE title = '%s'" % product)
                result = cursor.fetchall()
                for row in result:
                    await ctx.send(row)
    except Error as e:
        print(e)

bot.run(a['token'])