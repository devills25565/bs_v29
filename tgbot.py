import telebot 
import random 
import json
import sqlite3
from telebot import types
from config import token, adminID

admin=[adminID]
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in admin:
    	bot.reply_to(message, "Главное меню | команды: \n/shop - Настройки магазина.\n/server - управление игрой.\n/player - аккаунты выдача.\n\n/profile - просмотр акккаунта.\n/infobot - информация о боте.")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")
        
@bot.message_handler(commands=['shop'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in admin:
    	bot.reply_to(message, "- Магазин -\n/list - Посмотреть список акций.\n/new_offer - создает новую акцию.\n/remove_offer - Удалить акцию.\n/auto_shop - Обновить магазин.")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['server'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in admin:
    	bot.reply_to(message, "- Сервер -\n/theme - Изменить всем фон\n/new_code - Добавить новый код Автора.\n/del_code - Удалить код Автора.\n/code_list - Список кодов Автора")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['player'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in admin:
    	bot.reply_to(message, "- Аккаунты -\n/add_vip - Выдать вип статус.\n/del_vip - Забрать вип статус.\n---\n/add_gems - Выдать гемов игроку.\n/add_star - выдать старпойнтов\n/add_gold - выдать голды\n/add_tickets - выдать тикетов\n---\n/win_solo - выдать соло побед\n/win_party - выдать 3х3 побед\n---\n/ban - Выдать бан игроку.\n/unban - Разбанить игрока\n---\n/name - Просмотр ника по ID\n/nikc - Просмотр ID по NAME\n/id - поиск по нику\n---\n/gems - Просмотр кол-ва Гемов по ID\n/token - посмотреть токен игрока\n/star - посмоть старпойнты игрока\n/gold - посмотреть голду игрока")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['infobot'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in admin:
    	bot.reply_to(message, "- Информация о боте -\n\nversion: v2.0")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

# Функция для получения списка всех акций из файла offers.json
def get_offers():
    # Читаем данные из файла offers.json
    with open("Logic/offers.json", "r",encoding='utf-8') as f:
        data = json.load(f)

    # Генерируем текстовый список всех акци
    offer_list = "Список акций:\n"
    for offer_id, offer_data in data.items():
        vault=offer_data['ShopType']
        daily=offer_data['ShopDisplay']
        current=""
        types=""
        if vault==1:current="Золото"
        elif vault==0:current="Кристаллы"
        if daily==1:types="Ежедневная"
        elif daily==0:types="Обычная"
        offer_list += f"\nАкция #{offer_id}\n"
        offer_list += f"Название: {offer_data['OfferTitle']}\n"
        offer_list += f"Тип: {types}\n"
        offer_list += f"Боец: {offer_data['BrawlerID'][0]}\n"
        offer_list += f"Скин: {offer_data['SkinID'][0]}\n"
        offer_list += f"Валюта: {current}\n"
        offer_list += f"Стоимость: {offer_data['Cost']}\n"
        offer_list += f"Множитель: {offer_data['Multiplier'][0]}\n"

    # Возвращаем текстовый список всех акций
    return offer_list
# Обработчик команды /list
@bot.message_handler(commands=['list'])
def handle_list_offers(message):
    # Получаем список всех акций из файла offers.json
    offer_list = get_offers()

    # Отправляем пользователю список всех акций
    bot.send_message(chat_id=message.chat.id, text=offer_list)
    
    
@bot.message_handler(commands=['new_offer'])
def add_offer(message):
    user_id = message.from_user.id
    if user_id in admin:
    	if len(message.text.split()) < 2:
    	   bot.reply_to(message, 'Используйте команду /new_offer с аргументами в формате: /new_offer <ID> <OfferTitle> <Cost> <Multiplier> <BrawlerID> <SkinID> <OfferBGR> <ShopType> <ShopDisplay>')
    	   return
    	offer_data = message.text.split()
    	new_offer = {
            'ID': [int(offer_data[1]), 0, 0],
            'OfferTitle': offer_data[2],
            'Cost': int(offer_data[3]),
            'OldCost': 0,
            'Multiplier': [int(offer_data[4]), 0, 0],
            'BrawlerID': [int(offer_data[5]), 0, 0],
            'SkinID': [int(offer_data[6]), 0, 0],
            'WhoBuyed': [],
            'Timer': 86400,
            'OfferBGR': offer_data[7],
            'ShopType': int(offer_data[8]),
            'ShopDisplay': int(offer_data[9])
    	}
    	with open('Logic/offers.json', 'r',encoding='utf-8') as f:
    	   offers = json.load(f)
    	offers[str(len(offers))] = new_offer
    	with open('Logic/offers.json', 'w',encoding='utf-8') as f:
    	   json.dump(offers, f, indent=4)
    	bot.reply_to(message, 'Новая акция добавлена!')
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['remove_offer'])
def remove_offer(message):
    user_id = message.from_user.id
    if user_id in admin:
    	if len(message.text.split()) != 2:
    	   bot.reply_to(message, 'Используйте команду /remove_offer с аргументом в формате: /remove_offer <ID>')
    	   return
    	offer_id = message.text.split()[1]
    	with open('Logic/offers.json', 'r', encoding='utf-8') as f:
    		offers = json.load(f)
    	if offer_id not in offers:
    		bot.reply_to(message, f'Акция с ID {offer_id} не найдена')
    		return
    	offers.pop(offer_id)
    	with open('Logic/offers.json', 'w', encoding='utf-8') as f:
    		json.dump(offers, f)
    	bot.reply_to(message, f'Акция с ID {offer_id} удалена')
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")
# Определяем функцию-обработчик для команды /theme
@bot.message_handler(commands=['theme'])
def theme(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Выбери ID темы\n0 - Обычная\n1 - Новый год (Снег)\n2 - Красный новый год\n3 - От клеш рояля\n5 - Желтые панды\n6 - Фиолетовый булл\n7 - Роботы Зелёный фон\n8 - Фиолетовый фон\n9 - Пиратский фон\n11 - Футбольный фон\nИспользовать команду /theme ID")
        else:
            user_id = message.from_user.id
            theme_id = message.text.split()[1]
            conn = sqlite3.connect("database/Player/plr.db")
            c = conn.cursor()
            c.execute(f"UPDATE plrs SET theme={theme_id}")
            conn.commit()
            c.execute("SELECT * FROM plrs")
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Айди всех записей был изменён на {theme_id}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")
#коды автора
@bot.message_handler(commands=['new_code'])
def new_code(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /new_code Название Кода(На англ)")
        else:
            code = message.text.split()[1]
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if code not in config["CCC"]:
                config["CCC"].append(code)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Новый код {code}, Был добавлен!")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Код {code} уже существует!")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['code_list'])
def code_list(message):
    with open('config.json', 'r') as f:
        data = json.load(f)
    code_list = '\n'.join(data["CCC"])
    bot.send_message(chat_id=message.chat.id, text=f"Список кодов: \n{code_list}")
    	
    	
@bot.message_handler(commands=['del_code'])
def del_code(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /del_code Название Кода")
        else:
            code = message.text.split()[1]
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if code in config["CCC"]:
                config["CCC"].remove(code)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Код {code}, Был удалён!")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Код {code} не найден!")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")
 #конец кодов
#Вип Старт
 
@bot.message_handler(commands=['add_vip'])
def add_vip(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /add_vip ID(Можно узнать в профиле профиле при поставке цветного ника)")
        else:
            vip_id = int(message.text.split()[1])
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if vip_id not in config["vips"]:
                config["vips"].append(vip_id)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Вип статус был выдан игроку с ID {vip_id}")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Вип статус уже есть у ID {vip_id}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

		
@bot.message_handler(commands=['del_vip'])
def del_vip(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /del_vip ID(Можно узнать в профиле профиле при поставке цветного ника)")
        else:
            code = int(message.text.split()[1])
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if code in config["vips"]:
                config["vips"].remove(code)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Вип статус был удален у игрока с ID {code}")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Вип статус не найден у игрока с ID {code}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

# add_gems
@bot.message_handler(commands=['add_gems'])
def add_gems(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /add_gems ID AMMOUNT")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            ammount = message.text.split()[2]
            gems = message.text.split()
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE plrs SET gems = ? WHERE lowID = ?", (ammount, id))
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Игроку с айди {id} Выдали {ammount} Гемов, теперь у игрока {gems} Гемов")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

# add_star
@bot.message_handler(commands=['add_star'])
def add_gems(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /add_star ID AMMOUNT")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            ammount = message.text.split()[2]
            gems = message.text.split()
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE plrs SET starpoints = ? WHERE lowID = ?", (ammount, id))
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Игроку с айди {id} Выдали {ammount} старок, теперь у игрока {gems} старок")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

# add_gold
@bot.message_handler(commands=['add_gold'])
def add_gems(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /add_gold ID AMMOUNT")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            ammount = message.text.split()[2]
            gems = message.text.split()
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE plrs SET gold = ? WHERE lowID = ?", (ammount, id))
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Игроку с айди {id} Выдали {ammount} gold, теперь у игрока {gems} gold")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")
		
# add_tickets 
@bot.message_handler(commands=['add_tickets'])
def add_gems(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /add_tickets ID AMMOUNT")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            ammount = message.text.split()[2]
            gems = message.text.split()
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE plrs SET tickets = ? WHERE lowID = ?", (ammount, id))
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Игроку с айди {id} Выдали {ammount} тиков, теперь у игрока {gems} тиков")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")
		
# win_solo
@bot.message_handler(commands=['win_solo'])
def add_gems(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /win_solo ID AMMOUNT")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            ammount = message.text.split()[2]
            gems = message.text.split()
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE plrs SET sdWINS = ? WHERE lowID = ?", (ammount, id))
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Игроку с айди {id} Выдали {ammount} побед, теперь у игрока {gems} соло побед")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['unban'])
def unban(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /unban ID")
        else:
            vip_id = int(message.text.split()[1])
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if vip_id in config["banID"]:
                config["banID"].remove(vip_id)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Бан был снять с ID {vip_id}")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"У игрока нет бана ID {vip_id}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")
		
@bot.message_handler(commands=['ban'])
def ban(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /ban ID")
        else:
            vip_id = int(message.text.split()[1])
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if vip_id not in config["banID"]:
                config["banID"].append(vip_id)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Бан был выдан игроку {vip_id}")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Бан уже есть у игрока {vip_id}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

# nick
@bot.message_handler(commands=['nick'])
def add_gems(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /nick ID NICKNAME")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            nick = message.text.split()[2]
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE plrs SET name = ? WHERE lowID = ?", (nick, id))
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Игроку с айди {id} был изменен ник на {nick}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

# name
@bot.message_handler(commands=['name'])
def name_val(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /name ID")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("SELECT [name] from plrs WHERE lowID = ?", (id,))
            row = cursor.fetchone()
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"НикНейм у ID {id} - {row}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")
       
@bot.message_handler(commands=['id'])
def name_val(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /id ID")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("SELECT [lowID] from plrs WHERE name = ?", (id,))
            row = cursor.fetchone()
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"{id} - ID:{row}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

# gems
@bot.message_handler(commands=['gems'])
def gems_val(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /gems ID")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("SELECT [gems] from plrs WHERE lowID = ?", (id,))
            row = cursor.fetchone()
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Количество гемов у ID {id} - {row}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

# gold
@bot.message_handler(commands=['gold'])
def gold_val(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /gold ID")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("SELECT [gold] from plrs WHERE lowID = ?", (id,))
            row = cursor.fetchone()
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Количество золота у ID {id} - {row}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

# старки
@bot.message_handler(commands=['star'])
def gems_val(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /star ID")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("SELECT [starpoints] from plrs WHERE lowID = ?", (id,))
            row = cursor.fetchone()
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Количество старок у ID {id} - {row}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

# ТИКИТЫ
@bot.message_handler(commands=['tickets'])
def gems_val(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /tickets ID")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("SELECT [tickets] from plrs WHERE lowID = ?", (id,))
            row = cursor.fetchone()
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Количество тикитов у ID {id} - {row}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

#token
@bot.message_handler(commands=['token'])
def gems_val(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /token ID")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("SELECT [token] from plrs WHERE lowID = ?", (id,))
            row = cursor.fetchone()
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Токен игрока с iD {id} - {row}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

#INFO PLAYER
@bot.message_handler(commands=['profile'])
def gems_val(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /profile ID")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            conn = sqlite3.connect("database/Player/plr.db")
#
            cursor = conn.cursor()
            cursor.execute("SELECT [name] from plrs WHERE lowID = ?", id)
            name = cursor.fetchone()
#
            cursor = conn.cursor()
            cursor.execute("SELECT [gems] from plrs WHERE lowID = ?", id)
            gems = cursor.fetchone()
#
            cursor = conn.cursor()
            cursor.execute("SELECT [gold] from plrs WHERE lowID = ?", id)
            gold = cursor.fetchone()
#
            cursor = conn.cursor()
            cursor.execute("SELECT [trophies] from plrs WHERE lowID = ?", id)
            trof = cursor.fetchone()
#
            cursor = conn.cursor()
            cursor.execute("SELECT [token] from plrs WHERE lowID = ?", id)
            tokenID = cursor.fetchone()
#
            cursor = conn.cursor()
            cursor.execute("SELECT [vip] from plrs WHERE lowID = ?", id)
            vip = cursor.fetchone()
#
            conn.commit()
            conn.close()                
            bot.send_message(chat_id=message.chat.id, text=f"- Профиль игрока - [{id}]\n\n- Информация.\nник - {name}\nтокен - {tokenID}\n\n- Баланс -\nГемы - {gems}\nЗолото - {gold}\n\n- Статистика.\nТрофеи - {trof}\nВип пропуск - {vip}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

#vip_list
@bot.message_handler(commands=['vips'])
def gems_val(message):
    user_id = message.from_user.id
    if user_id in admin:
            user_id = message.from_user.id
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("SELECT vip from plrs")
            row = cursor.fetchall()
            cursor.execute("SELECT lowID from plrs")
            rof = cursor.fetchall()
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"IDs\n\n{rof}\n\n\nVIPs\n\n{row}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")



# Запускаем бота
print('start! :D')
bot.polling()
