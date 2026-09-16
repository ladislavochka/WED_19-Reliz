import os
import json
import telebot
from telebot import types

TOKEN = "8956257923:AAGFI-UljPMl6hlxXoIWAXbMcT6LOP7rUus"
SAVE_FOLDER = "./saved_files"
DB_FILE = "db.json"

bot = telebot.TeleBot(TOKEN)

# Створюємо папку для файлів
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Змінна для тимчасового збереження даних, поки користувач пише опис
user_states = {}

# JSON
def load_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- КОМАНДА /start ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("➕ Новий запис", callback_data="new_record"),
        types.InlineKeyboardButton("📁 Мої записи", callback_data="my_records")
    )
    bot.send_message(message.chat.id, "Головне меню:", reply_markup=keyboard)

# --- ОБРОБКА КНОПОК ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id

    if call.data == "new_record":
        user_states[chat_id] = {'step': 'wait_file'}
        bot.send_message(chat_id, "Надішли мені файл (фото, документ, аудіо тощо):")

    elif call.data == "my_records":
        db = load_db()
        if not db:
            bot.send_message(chat_id, "У тебе поки немає збережених записів.")
            return

        # Створюємо список кнопок для кожного файлу
        keyboard = types.InlineKeyboardMarkup()
        for idx, item in enumerate(db):
            # Текст на кнопці: Опис або назва файлу
            btn_text = f"📄 {item['description']} ({item['file_name']})"
            keyboard.add(types.InlineKeyboardButton(btn_text, callback_data=f"get_{idx}"))

        bot.send_message(chat_id, "Обери файл для завантаження:", reply_markup=keyboard)

    elif call.data.startswith("get_"):
        # Отримуємо номер файлу зі списку
        index = int(call.data.split("_")[1])
        db = load_db()

        if index < len(db):
            record = db[index]
            file_path = record['path']

            if os.path.exists(file_path):
                bot.send_message(chat_id, f"Надсилаю: {record['description']}")
                with open(file_path, 'rb') as f:
                    bot.send_document(chat_id, f)
            else:
                bot.send_message(chat_id, "⚠️ Файл не знайдено на комп'ютері.")

# --- ОПРАЦЮВАННЯ ФАЙЛУ ВІД КОРИСТУВАЧА ---
@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'voice'])
def handle_file_upload(message):
    chat_id = message.chat.id

    if chat_id not in user_states or user_states[chat_id].get('step') != 'wait_file':
        bot.reply_to(message, "Спочатку натисни кнопку **➕ Новий запис** у меню /start")
        return

    # Визначення типу та збереження
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[-1].file_id)
        original_name = f"photo_{message.photo[-1].file_id[:8]}.jpg"
    else:
        content = getattr(message, message.content_type)
        file_info = bot.get_file(content.file_id)
        original_name = getattr(content, 'file_name', f"{message.content_type}_{content.file_id[:8]}")

    downloaded = bot.download_file(file_info.file_path)
    file_path = os.path.join(SAVE_FOLDER, original_name)

    with open(file_path, 'wb') as f:
        f.write(downloaded)

    # Переводимо бота в стан очікування опису
    user_states[chat_id] = {
        'step': 'wait_description',
        'file_path': file_path,
        'file_name': original_name
    }
    bot.reply_to(message, "Файл збережено! Тепер напиши **короткий опис** для цього файлу:")

# --- ОПРАЦЮВАННЯ ТЕКСТУ (ОПИСУ) ---
@bot.message_handler(func=lambda msg: True)
def handle_text(message):
    chat_id = message.chat.id

    if chat_id in user_states and user_states[chat_id].get('step') == 'wait_description':
        description = message.text
        file_data = user_states[chat_id]

        # Записуємо в базу
        db = load_db()
        db.append({
            'file_name': file_data['file_name'],
            'path': file_data['file_path'],
            'description': description
        })
        save_db(db)

        # Очищаємо стан
        del user_states[chat_id]
        bot.reply_to(message, f"Успішно збережено! Опис: '{description}'. Напиши /start для меню.")

print("Бот працює...")
bot.infinity_polling()