import telebot
from telebot import types
from fake_useragent import UserAgent
import requests
import random
import string
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_TOKEN = '7367366548:AAGGhOKkI5SchN3Q2hTuaQEaocDtxHdTvoQ'
CHANNEL_USERNAME = '@incelbeck'  # Username канала для проверки
CHAT_USERNAME = '@doxtrollosint'  # Username чата для проверки

bot = telebot.TeleBot(API_TOKEN)

# Хранилище статуса подписки пользователей
user_subscription_status = {}

def check_subscription(user_id):
    """Проверка подписки пользователя на канал и чат"""
    try:
        # Проверка подписки на канал
        channel_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        channel_status = channel_member.status in ['member', 'administrator', 'creator']
        
        # Проверка участия в чате
        chat_member = bot.get_chat_member(CHAT_USERNAME, user_id)
        chat_status = chat_member.status in ['member', 'administrator', 'creator']
        
        return channel_status and chat_status
    except Exception as e:
        logging.error(f"Ошибка проверки подписки для пользователя {user_id}: {e}")
        return False

def subscription_required(func):
    """Декоратор для проверки подписки перед выполнением функции"""
    def wrapper(message):
        user_id = message.from_user.id
        
        if check_subscription(user_id):
            return func(message)
        else:
            # Создаем клавиатуру с кнопками для подписки
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn_channel = types.InlineKeyboardButton("📢 Подписаться на канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
            btn_chat = types.InlineKeyboardButton("💬 Войти в чат", url=f"https://t.me/{CHAT_USERNAME[1:]}")
            btn_check = types.InlineKeyboardButton("✅ Я подписался", callback_data="check_subscription")
            markup.add(btn_channel, btn_chat, btn_check)
            
            bot.reply_to(
                message, 
                "❌ Для использования бота необходимо подписаться на канал и вступить в чат!\n\n"
                "Нажмите кнопки ниже чтобы подписаться, затем нажмите 'Я подписался'",
                reply_markup=markup
            )
    return wrapper

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "mail.ru"]
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    domain = random.choice(domains)
    email = f"{username}@{domain}"
    return email

def generate_phone_number():
    country_codes = ['+7', '+380', '+375']
    country_code = random.choice(country_codes)
    phone_number = ''.join(random.choices('0123456789', k=10))
    formatted_phone_number = f'{country_code}{phone_number}'
    return formatted_phone_number

def send_complaint(chat_id, message, repeats):
    url = 'https://telegram.org/support'
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}
    complaints_sent = 0
    for i in range(repeats):
        email = generate_random_email()
        phone = generate_phone_number()
        try:
            response = requests.post(url, headers=headers, data={'message': message}, timeout=10)
            if response.status_code == 200:
                complaints_sent += 1
                status = "✅ Успешно"
            else:
                status = "❌ Неуспешно"
            logging.info(f'Sent complaint: {message}, Email: {email}, Phone: {phone}, Status: {status}')
            bot.send_message(chat_id, f"✉️ Сообщение: {message}\n📪 Email: {email}\n📞 Телефон: {phone}\n▶️ Статус: {status}")
        except Exception as e:
            logging.error(f"Ошибка при отправке жалобы: {e}")
            bot.send_message(chat_id, f"❌ Ошибка при отправке: {e}")
    return complaints_sent

def sms_bomb(chat_id, phone_number, repeats):
    """Функция для SMS бомбера"""
    # Здесь должен быть ваш код для SMS бомбера
    # Это демонстрационная версия
    urls = [
        "https://api.sms-service.com/send",
        "https://api.sms-provider.ru/send"
    ]
    
    headers = {
        'User-Agent': UserAgent().random,
        'Content-Type': 'application/json'
    }
    
    sent_count = 0
    for i in range(repeats):
        try:
            # Пример запроса (замените на реальные API)
            data = {
                'phone': phone_number,
                'message': f'Код подтверждения: {random.randint(1000, 9999)}'
            }
            
            # Используем случайный URL из списка
            url = random.choice(urls)
            
            # Здесь должен быть реальный запрос к SMS API
            # response = requests.post(url, json=data, headers=headers, timeout=10)
            
            # Для демонстрации просто имитируем отправку
            time.sleep(0.5)
            sent_count += 1
            status = "✅ Отправлено"
            
            bot.send_message(
                chat_id, 
                f"📱 Номер: {phone_number}\n"
                f"📨 Попытка {i+1}/{repeats}\n"
                f"▶️ Статус: {status}"
            )
        except Exception as e:
            logging.error(f"Ошибка SMS бомбера: {e}")
            bot.send_message(chat_id, f"❌ Ошибка: {e}")
    
    return sent_count

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Проверяем подписку
    if check_subscription(message.from_user.id):
        show_main_menu(message)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_channel = types.InlineKeyboardButton("📢 Подписаться на канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        btn_chat = types.InlineKeyboardButton("💬 Войти в чат", url=f"https://t.me/{CHAT_USERNAME[1:]}")
        btn_check = types.InlineKeyboardButton("✅ Я подписался", callback_data="check_subscription")
        markup.add(btn_channel, btn_chat, btn_check)
        
        bot.reply_to(
            message, 
            "👋 Привет! Я многофункциональный бот.\n\n"
            "Для использования бота необходимо подписаться на канал и вступить в чат!\n\n"
            "Нажмите кнопки ниже чтобы подписаться, затем нажмите 'Я подписался'",
            reply_markup=markup
        )
    logging.info(f'User {message.chat.id} started the bot.')

def show_main_menu(message):
    """Показывает главное меню с выбором функций"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_snos = types.InlineKeyboardButton("🔥 Sn0s (Жалобы)", callback_data="snos_menu")
    btn_sms = types.InlineKeyboardButton("💣 SMS Bomb", callback_data="sms_menu")
    btn_channel = types.InlineKeyboardButton("📢 Канал", callback_data="channel_info")
    btn_chat = types.InlineKeyboardButton("💬 Чат", callback_data="chat_info")
    markup.add(btn_snos, btn_sms, btn_channel, btn_chat)
    
    bot.send_message(
        message.chat.id, 
        "🔰 Главное меню\n\n"
        "Выберите нужную функцию:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def callback_check_subscription(call):
    user_id = call.from_user.id
    
    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "✅ Подписка подтверждена! Доступ открыт.")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message)
    else:
        bot.answer_callback_query(
            call.id, 
            "❌ Вы не подписались на канал или не вступили в чат!",
            show_alert=True
        )

@bot.callback_query_handler(func=lambda call: call.data == "channel_info")
def callback_channel_info(call):
    markup = types.InlineKeyboardMarkup()
    btn_channel = types.InlineKeyboardButton("📢 Перейти в канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
    markup.add(btn_channel)
    bot.send_message(
        call.message.chat.id, 
        f"📢 **Наш канал**\n\n{CHANNEL_USERNAME}\n\nПодпишись чтобы быть в курсе обновлений!",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "chat_info")
def callback_chat_info(call):
    markup = types.InlineKeyboardMarkup()
    btn_chat = types.InlineKeyboardButton("💬 Перейти в чат", url=f"https://t.me/{CHAT_USERNAME[1:]}")
    markup.add(btn_chat)
    bot.send_message(
        call.message.chat.id, 
        f"💬 **Наш чат**\n\n{CHAT_USERNAME}\n\nОбщайся с единомышленниками!",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "snos_menu")
def callback_snos_menu(call):
    if not check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Требуется подписка!", show_alert=True)
        return
    
    msg = bot.send_message(call.message.chat.id, "📝 Введите текст жалобы:")
    bot.register_next_step_handler(msg, snos_input_repeats)
    logging.info(f'User {call.message.chat.id} is entering text for snos.')

def snos_input_repeats(message):
    text = message.text
    msg = bot.send_message(message.chat.id, "🔢 Введите количество сообщений для отправки:")
    bot.register_next_step_handler(msg, lambda m: snos_send_messages(m, text))

def snos_send_messages(message, text):
    try:
        repeats = int(message.text)
        if repeats > 100:
            bot.send_message(message.chat.id, "⚠️ Максимальное количество - 100 сообщений за раз.")
            return
            
        bot.send_message(message.chat.id, f"⏳ Отправка {repeats} жалоб...")
        complaints_sent = send_complaint(message.chat.id, text, repeats)
        bot.send_message(
            message.chat.id, 
            f"✅ Готово! Отправлено {complaints_sent} из {repeats} жалоб."
        )
        logging.info(f'User {message.chat.id} sent {repeats} snos messages.')
    except ValueError:
        bot.send_message(message.chat.id, "❌ Ошибка: введите корректное число.")
        logging.error(f'User {message.chat.id} entered an invalid number: {message.text}')

@bot.callback_query_handler(func=lambda call: call.data == "sms_menu")
def callback_sms_menu(call):
    if not check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Требуется подписка!", show_alert=True)
        return
    
    msg = bot.send_message(
        call.message.chat.id, 
        "📱 Введите номер телефона для SMS бомбера\n"
        "Формат: +7XXXXXXXXXX или 8XXXXXXXXXX"
    )
    bot.register_next_step_handler(msg, sms_input_repeats)

def sms_input_repeats(message):
    phone = message.text.strip()
    # Простая валидация номера
    if not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
        bot.send_message(message.chat.id, "❌ Неверный формат номера!")
        return
    
    msg = bot.send_message(message.chat.id, "🔢 Введите количество SMS для отправки:")
    bot.register_next_step_handler(msg, lambda m: sms_send_messages(m, phone))

def sms_send_messages(message, phone):
    try:
        repeats = int(message.text)
        if repeats > 50:
            bot.send_message(message.chat.id, "⚠️ Максимальное количество - 50 SMS за раз.")
            return
            
        bot.send_message(message.chat.id, f"⏳ Запуск SMS бомбера...")
        sent_count = sms_bomb(message.chat.id, phone, repeats)
        bot.send_message(
            message.chat.id, 
            f"✅ Готово! Отправлено {sent_count} из {repeats} SMS."
        )
        logging.info(f'User {message.chat.id} sent {repeats} SMS to {phone}')
    except ValueError:
        bot.send_message(message.chat.id, "❌ Ошибка: введите корректное число.")
        logging.error(f'User {message.chat.id} entered an invalid number: {message.text}')

# Обработка всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Проверяем подписку
    if check_subscription(message.from_user.id):
        show_main_menu(message)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_channel = types.InlineKeyboardButton("📢 Подписаться на канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        btn_chat = types.InlineKeyboardButton("💬 Войти в чат", url=f"https://t.me/{CHAT_USERNAME[1:]}")
        btn_check = types.InlineKeyboardButton("✅ Я подписался", callback_data="check_subscription")
        markup.add(btn_channel, btn_chat, btn_check)
        
        bot.reply_to(
            message, 
            "❌ Для использования бота необходимо подписаться на канал и вступить в чат!\n\n"
            "Нажмите кнопки ниже чтобы подписаться, затем нажмите 'Я подписался'",
            reply_markup=markup
        )

print("Бот запущен...")
bot.polling(none_stop=True)
