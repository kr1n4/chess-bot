import os
import random
import time
import requests
import telebot
from telebot import types

Укажите ваш API-токен от @BotFather здесь или задайте через переменную окружения

BOT_TOKEN = os.getenv("BOT_TOKEN", "9027594374:AAEOb20_NrIg2QUG-JhwDxEjRWlys1w5nXg")
bot = telebot.TeleBot(BOT_TOKEN)

Временная база данных пользователей (In-Memory)

users_db = {}  # {user_id: {"score": 0, "current_task": int}}
clocks_db = {}  # {user_id: {"white_time": int, "black_time": int, "inc": int, "last_click": float, "msg_id": int}}

---------------------------------------------------------------------


БАЗА ДАННЫХ: РОВНО 30 ХИТРЫХ ЗАДАЧ (Без спойлеров в тексте, хитрые варианты)


---------------------------------------------------------------------

TACTOR_TASKS = [
{"id": 1, "theme": "Вилка", "desc": "Ход белых. 🔹 Обнаружьте тактическую слабость на королевском фланге соперника и получите материальный перевес.", "fen": "r1bqk2r/ppp2ppp/2np1n2/4p3/2B1P3/2NP1N2/PPP2PPP/R1BQK2R w KQkq - 0 6", "correct": "Ng5", "variants": ["Ng5", "d4", "Bxf7+", "O-O"]},
{"id": 2, "theme": "Связка", "desc": "Ход черных. 🔹 Заметьте незащищенный мотив в центре белых и свяжите ключевую фигуру противника.", "fen": "rnbqk2r/pppp1ppp/5n2/4p3/1bB1P3/2N5/PPPP1PPP/R1BQK1NR b KQkq - 4 4", "correct": "Nxe4", "variants": ["Nxe4", "O-O", "d6", "Bxc3"]},
{"id": 3, "theme": "Спёртый мат", "desc": "Ход белых. 🔹 Изящный финал близок. Найдите форсированную матовую конструкцию против зажатого короля.", "fen": "r1b1kbnr/pppp1ppp/2n5/4p3/7q/4P3/PPPP1PPP/RNBQKBNR w KQkq - 0 4", "correct": "Nf3", "variants": ["Nf3", "Be2", "h3", "Qe2"]},
{"id": 4, "theme": "Отвлечение", "desc": "Ход белых. 🔹 Защита черного короля кажется надежной, но одна из фигур перегружена. Отвлеките её!", "fen": "rn1qkbnr/ppp1pppp/8/3p4/6b1/5NP1/PPPPPP1P/RNBQKB1R w KQkq - 1 3", "correct": "Ne5", "variants": ["Ne5", "Bg2", "c4", "h3"]},
{"id": 5, "theme": "Разрушение рокировки", "desc": "Ход белых. 🔹 Королевское убежище черных держится на волоске. Пожертвуйте фигуру ради вскрытия линий.", "fen": "rnbqk2r/ppp2ppp/3b1n2/3pp3/8/3P1NP1/PPPNPPBP/R1BQK2R w KQkq - 2 5", "correct": "e4", "variants": ["e4", "c4", "O-O", "d4"]},
{"id": 6, "theme": "Пешечный прорыв", "desc": "Ход белых. 🔹 Пешечная структура определяет исход эндшпиля. Создайте проходную пешку точным ударом.", "fen": "8/8/8/4kppp/8/8/5PPP/6K1 w - - 0 1", "correct": "f4+", "variants": ["f4+", "h4", "g4", "Kf2"]},
{"id": 7, "theme": "Вилка", "desc": "Ход черных. 🔹 Белые неосторожно вывели тяжелую фигуру. Накажите их двойным ударом коня.", "fen": "rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 3 3", "correct": "Nxe4", "variants": ["Nxe4", "Nc6", "Bc5", "d6"]},
{"id": 8, "theme": "Связка", "desc": "Ход белых. 🔹 Противник связал вашего коня, но оставил дыру на диагонали. Опровергните этот выпад.", "fen": "rnbqk1br/pppp1ppp/5n2/4p3/1bB1P3/2N5/PPPP1PPP/R1BQK1NR w KQkq - 4 4", "correct": "Nge2", "variants": ["Nge2", "Bxf7+", "O-O", "a3"]},
{"id": 9, "theme": "Отвлечение", "desc": "Ход белых. 🔹 Черный ферзь контролирует важное поле. Найдите способ увести его с огневой рубежа.", "fen": "rnbqkbnr/ppp2ppp/3p4/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 4", "correct": "Qxf7#", "variants": ["Qxf7#", "Bxf7+", "Ne2", "Nh3"]},
{"id": 10, "theme": "Спёртый мат", "desc": "Ход белых. 🔹 Проведите классическую комбинацию с удушением вражеского монарха на краю доски.", "fen": "rnbqkb1r/pppp1ppp/8/4p3/2B1n3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4", "correct": "Bxf7+", "variants": ["Bxf7+", "Nxe5", "O-O", "Qe2"]},
{"id": 11, "theme": "Вилка", "desc": "Ход белых. 🔹 Вскройте центр и создайте неотразимую вилку пешкой или фигурой на две активные цели.", "fen": "rnbqkbnr/ppp2ppp/4p3/3p4/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 3", "correct": "exd5", "variants": ["exd5", "e5", "Nc3", "d4"]},
{"id": 12, "theme": "Связка", "desc": "Ход черных. 🔹 Воспользуйтесь тем, что король белых задержался в центре, и выиграйте темп через связку.", "fen": "rnbqkbnr/ppp2ppp/3p4/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 1 3", "correct": "Be7", "variants": ["Be7", "Nf6", "Bg4", "Nc6"]},
{"id": 13, "theme": "Отвлечение", "desc": "Ход белых. 🔹 Пожертвуйте легкую фигуру, чтобы разрушить геометрию обороны черных.", "fen": "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3", "correct": "d4", "variants": ["d4", "Bc4", "Bb5", "Nc3"]},
{"id": 14, "theme": "Спёртый мат", "desc": "Ход белых. 🔹 Докажите, что плохая координация фигур соперника карается быстрым разгромом.", "fen": "rnbqkbnr/1ppp1ppp/p7/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 0 3", "correct": "Qh5", "variants": ["Qh5", "Bxf7+", "Nf3", "d4"]},
{"id": 15, "theme": "Разрушение рокировки", "desc": "Ход белых. 🔹 Конь противника прыгнул слишком далеко вперед. Срежьте оборонительные подпорки.", "fen": "rnbqkbnr/ppp2ppp/3p4/4p3/2B1P3/4N3/PPPP1PPP/RNBQK2R w KQkq - 0 4", "correct": "O-O", "variants": ["O-O", "Bxf7+", "Qf3", "d4"]},
{"id": 16, "theme": "Пешечный прорыв", "desc": "Ход черных. 🔹 Атакуйте пешечную цепь белых с фланга, открывая дорогу своей проходной пешке.", "fen": "8/8/8/p7/P7/1k6/8/2K5 b - - 0 1", "correct": "Kxa4", "variants": ["Kxa4", "Kb4", "Kc3", "Ka3"]},
{"id": 17, "theme": "Вилка", "desc": "Ход белых. 🔹 Найдите скрытую коневую вилку после короткого размена в центре.", "fen": "r1bqkbnr/ppp2ppp/2n5/3pp3/3PP3/5N2/PPP2PPP/RNBQKB1R w KQkq - 0 4", "correct": "Nxe5", "variants": ["Nxe5", "exd5", "dxe5", "Bb5"]},
{"id": 18, "theme": "Связка", "desc": "Ход черных. 🔹 Зафиксируйте вражеского коня мертвой связкой и подготовьте на него накат.", "fen": "rnbqkbnr/ppp2ppp/3p4/4p3/3PP3/5N2/PPP2PPP/RNBQKB1R b KQkq - 0 3", "correct": "exd4", "variants": ["exd4", "Nd7", "Nf6", "f6"]},
{"id": 19, "theme": "Отвлечение", "desc": "Ход белых. 🔹 Фигуры соперника скучковались. Отвлеките защитника ключевого полей.", "fen": "r1bqk1nr/pppp1ppp/2n5/2b1p3/4P3/5N2/PPPPBPPP/RNBQK2R w KQkq - 4 4", "correct": "O-O", "variants": ["O-O", "Nxe5", "d3", "c3"]},
{"id": 20, "theme": "Спёртый мат", "desc": "Ход черных. 🔹 Белые допустили зловещий зевок по большой диагонали. Окружите короля.", "fen": "rnbqkbnr/pppp1ppp/8/4p3/4P3/5Q2/PPPP1PPP/RNB1KBNR b KQkq - 1 2", "correct": "Nf6", "variants": ["Nf6", "Nc6", "Qf6", "d6"]},
{"id": 21, "theme": "Разрушение рокировки", "desc": "Ход белых. 🔹 Подготовьте почву для разрушения длинной рокировки соперника, вскрыв вертикаль.", "fen": "r3kbnr/ppp2ppp/2np1n2/4p3/4P1b1/2NP1NP1/PPP1BP1P/R1BQK2R w KQkq - 1 6", "correct": "Be3", "variants": ["Be3", "h3", "Nxe5", "O-O"]},
{"id": 22, "theme": "Пешечный прорыв", "desc": "Ход белых. 🔹 Превратите минимальное позиционное преимущество in ферзя точным маршем.", "fen": "8/8/8/6p1/5pP1/5P2/4k1K1/8 w - - 0 1", "correct": "Kh3", "variants": ["Kh3", "Kh2", "Kf1", "Kg1"]},
{"id": 23, "theme": "Вилка", "desc": "Ход черных. 🔹 Контратакуйте белых в дебюте четырех коней, поставив вилку на вилку.", "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R b KQkq - 5 4", "correct": "Nxe4", "variants": ["Nxe4", "Bc5", "Bb4", "d6"]},
{"id": 24, "theme": "Связка", "desc": "Ход белых. 🔹 Свяжите тяжелую фигуру черных, воспользовавшись их плохим развитием.", "fen": "r1bqk2r/ppp2ppp/2np1n2/1B2p3/4P3/2NP1N2/PPP2PPP/R1BQK2R w KQkq - 0 6", "correct": "d4", "variants": ["d4", "Bxc6+", "O-O", "h3"]},
{"id": 25, "theme": "Отвлечение", "desc": "Ход черных. 🔹 Ферзь белых перегружен защитой коня и матовых полей. Сделайте отвлекающий ход.", "fen": "rnbqkbnr/ppp2ppp/8/3pp3/4P3/5Q2/PPPP1PPP/RNB1KBNR b KQkq - 1 3", "correct": "Nf6", "variants": ["Nf6", "dxe4", "c6", "Be6"]},
{"id": 26, "theme": "Спёртый мат", "desc": "Ход белых. 🔹 Реализуйте фатальную ошибку черных в защите Кара-Канн изящным маневром.", "fen": "rnbqkbnr/pp2pppp/2p5/3p4/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 3", "correct": "exd5", "variants": ["exd5", "e5", "Nc3", "d4"]},
{"id": 27, "theme": "Разрушение рокировки", "desc": "Ход черных. 🔹 Король белых раскрылся. Найдите способ навсегда лишить его права на рокировку.", "fen": "rnbqk1nr/ppp2ppp/3p4/4p3/2B1P3/2P2N2/PPPP1PPP/RNBQK2R b KQkq - 1 4", "correct": "Nf6", "variants": ["Nf6", "Bg4", "Be7", "h6"]},
{"id": 28, "theme": "Пешечный прорыв", "desc": "Ход белых. 🔹 Отрежьте вражеского короля от вашей проходной пехоты решающим ходом.", "fen": "8/8/pK6/8/k7/8/8/8 w - - 0 1", "correct": "Kxa6", "variants": ["Kxa6", "Kbp5", "Kb7", "Kc5"]},
{"id": 29, "theme": "Вилка", "desc": "Ход белых. 🔹 Накажите черных за раннюю и агрессивную вылазку ферзя сокрушительной вилкой.", "fen": "rnb1kbnr/ppp1pppp/8/q7/8/2N5/PPPP1PPP/R1BQKBNR w KQkq - 2 4", "correct": "d4", "variants": ["d4", "Nf3", "b4", "e5"]},
{"id": 30, "theme": "Связка", "desc": "Ход белых. 🔹 Объявите рентген-атаку на вертикаль Е, сковав ключевые ресурсы черных.", "fen": "rnbqkbnr/ppp2ppp/8/3pp3/4P3/8/PPPPNPPP/RNBQKB1R w KQkq - 0 3", "correct": "exd5", "variants": ["exd5", "d3", "Nc3", "d4"]}
]

---------------------------------------------------------------------


ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ


---------------------------------------------------------------------

def init_user(user_id):
if user_id not in users_db:
users_db[user_id] = {"score": 0, "current_task": -1}
def get_rank(score):
if score <= 200:
return "Новичок 👶 (Базовый уровень)"
elif score <= 400:
return "Юный Разрядник 🛡️ (Умеет видеть простые угрозы)"
elif score <= 600:
return "Кандидат в Мастера (КМС) ⚔️ (Сильный тактик)"
else:
return "Гроссмейстер Клуба 👑 (Элита, открывший все секреты)"
def get_board_image_url(fen):
return f"lichess1.org{requests.utils.quote(fen)}&theme=brown&piece=cburnett"
def send_main_menu(chat_id):
markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup.add(
types.KeyboardButton("🏫 Академия шахмат"),
types.KeyboardButton("🧩 Тренажер тактики"),
types.KeyboardButton("🏆 Мой профиль")
)
lines = "═" * 20
bot.send_message(
chat_id,
f"{lines}\n👑 ДОБРО ПОЖАЛОВАТЬ В ШАХМАТНЫЙ КЛУБ! 👑\n{lines}\n"
f"🔹 Развивайте тактическое зрение\n"
f"🔹 Решайте уникальные задачи-ловушки\n"
f"🔹 Повышайте свой рейтинг до Гроссмейстера!",
reply_markup=markup
)

---------------------------------------------------------------------


ОБРАБОТЧИКИ МЕНЮ


---------------------------------------------------------------------

@bot.message_handler(commands=['start'])
def handle_start(message):
init_user(message.from_user.id)
send_main_menu(message.chat.id)
@bot.message_handler(func=lambda m: m.text == "🏆 Мой профиль")
def handle_profile(message):
user_id = message.from_user.id
init_user(user_id)
data = users_db[user_id]
text = (
f"════════════════════\n"
f"🏆 ВАШ ШАХМАТНЫЙ ПРОФИЛЬ\n"
f"════════════════════\n"
f"🔹 Ваш ID: {user_id}\n"
f"✅ Текущий рейтинг: {data['score']} очков\n"
f"👑 Звание: {get_rank(data['score'])}\n"
f"════════════════════"
)
bot.send_message(message.chat.id, text, parse_mode="Markdown")

---------------------------------------------------------------------


РАЗДЕЛ: ТРЕНАЖЕР ТАКТИКИ (30 задач с random.shuffle)


---------------------------------------------------------------------

@bot.message_handler(func=lambda m: m.text == "🧩 Тренажер тактики")
def handle_tactics_menu(message):
markup = types.InlineKeyboardMarkup()
markup.add(types.InlineKeyboardButton("▶️ Начать решать", callback_data="tactic_start"))
bot.send_message(
message.chat.id,
"🧩 ДОБРО ПОЖАЛОВАТЬ В ТРЕНАЖЕР ТАКТИКИ!\n\n"
"🔹 Каждая правильная задача: +10 очков\n"
"❌ Каждая ошибка: -5 очков\n\n"
"Готовы проверить себя?",
reply_markup=markup,
parse_mode="Markdown"
)
@bot.callback_query_handler(func=lambda c: c.data == "tactic_start")
def start_tactic_task(call):
user_id = call.from_user.id
init_user(user_id)
task = random.choice(TACTOR_TASKS)
users_db[user_id]["current_task"] = task["id"]
variants = list(task["variants"])
random.shuffle(variants)
markup = types.InlineKeyboardMarkup(row_width=2)
buttons = [types.InlineKeyboardButton(v, callback_data=f"ans_{v}") for v in variants]
markup.add(*buttons)
try:
bot.delete_message(call.message.chat.id, call.message.message_id)
except Exception:
pass
img_url = get_board_image_url(task["fen"])
bot.send_photo(
call.message.chat.id,
img_url,
caption=f"🧩 Задача на тему: {task['theme']}\n\n{task['desc']}",
reply_markup=markup,
parse_mode="Markdown"
)
@bot.callback_query_handler(func=lambda c: c.data.startswith("ans_"))
def handle_tactic_answer(call):
user_id = call.from_user.id
init_user(user_id)
user_ans = call.data.replace("ans_", "")
task_id = users_db[user_id]["current_task"]
task = next((t for t in TACTOR_TASKS if t["id"] == task_id), None)
if not task:
bot.send_message(call.message.chat.id, "❌ Произошла ошибка. Начните заново.")
return
try:
bot.delete_message(call.message.chat.id, call.message.message_id)
except Exception:
pass
if user_ans == task["correct"]:
users_db[user_id]["score"] += 10
text = f"✅ ВЕРНО! (+10 очков рейтинга)\n\nПравильный ход: {task['correct']}. Вы великолепно рассчитали вариант!"
else:
users_db[user_id]["score"] = max(0, users_db[user_id]["score"] - 5)
text = f"❌ ОШИБКА! (-5 очков рейтинга)\n\nВы попались в шахматную ловушку. Правильный ответ был: {task['correct']}."
markup = types.InlineKeyboardMarkup()
markup.add(types.InlineKeyboardButton("▶️ Следующая задача", callback_data="tactic_start"))
bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

---------------------------------------------------------------------


РАЗДЕЛ: АКАДЕМИЯ ШАХМАТ


---------------------------------------------------------------------

@bot.message_handler(func=lambda m: m.text == "🏫 Академия шахмат")
def handle_academy(message):
markup = types.InlineKeyboardMarkup(row_width=2)
markup.add(
types.InlineKeyboardButton("👶 Как ходят фигуры", callback_data="aca_pieces"),
types.InlineKeyboardButton("⚡ Особые правила", callback_data="aca_rules"),
types.InlineKeyboardButton("📐 Дебюты и Гамбиты", callback_data="aca_openings"),
types.InlineKeyboardButton("♟️ Стратегия Pro", callback_data="aca_strategy"),
types.InlineKeyboardButton("🎨 Визуализатор FEN", callback_data="aca_fen"),
types.InlineKeyboardButton("⏱️ Шахматные часы", callback_data="aca_clocks")
)
bot.send_message(message.chat.id, "🏫 ШАХМАТНАЯ АКАДЕМИЯ\n\nВыберите тему для интерактивного изучения теоретических основ или запуска встроенных инструментов:", reply_markup=markup)
@bot.callback_query_handler(func=lambda c: c.data.startswith("aca_"))
def handle_academy_callbacks(call):
topic = call.data.replace("aca_", "")
if topic == "pieces":
text = (
"👶 КАК ХОДЯТ ШАХМАТНЫЕ ФИГУРЫ:\n\n"
"🔹 ♙ Пешка — Ходит на 1 поле вперед (из нач. позиции на 2). Бьет по диагонали.\n"
"🔹 ♘ Конь — Ходит буквой 'Г'. Единственная фигура, прыгающая через другие.\n"
"🔹 ♗ Слон — Скользит только по диагоналям своего цвета.\n"
"🔹 ♖ Ладья — Перемещается по прямым горизонталям и вертикалям.\n"
"🔹 ♕ Ферзь — Сильнейшая фигура. Сочетает возможности Ладьи и Слона.\n"
"🔹 ♔ Король — Главная фигура. Ходит на 1 любое поле вокруг себя."
)
bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
elif topic == "rules":
text = (
"⚡ ОСОБЫЕ ПРАВИЛА В ШАХМАТАХ:\n\n"
"🔹 Рокировка — Одновременный ход Короля и Ладьи для защиты.\n"
"❌ Условия запрета: Король или Ладья уже ходили; Королю объявлен шах; Поля, через которые идет король, атакованы врагом.\n\n"
"🔹 Взятие на проходе (En Passant) — Если пешка соперника прыгнула на 2 поля мимо вашей пешки на 5-й (4-й для черных) горизонтали, вы имеете право забрать её ответным диагональным ходом на битое поле."
)
bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
elif topic == "openings":
text = (
"📐 ПОПУЛЯРНЫЕ ДЕБЮТЫ И ГАМБИТЫ:\n\n"
"🔹 Сицилианская защита (1.e4 c5) — Самый боевой ответ на e4.\n"
"🔹 Испанская партия (1.e4 e5 2.Nf3 Nc6 3.Bb5) — Вечная классика.\n"
"🔹 Ферзевый гамбит (1.d4 d5 2.c4) — Жертва фланговой пешки ради тотального контроля центра."
)
img = get_board_image_url("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")
bot.send_photo(call.message.chat.id, img, caption=text, parse_mode="Markdown")
elif topic == "strategy":
text = (
"♟️ СТРАТЕГИЯ PRO-УРОВНЯ:\n\n"
"🔹 Цугцванг — Положение в партии, когда любой ход игрока ведет к ухудшению его позиции.\n"
"🔹 Оппозиция королей — Противостояние королей через одно поле, где тот, чей ход, вынужден отступить.\n"
"🔹 Изолированная пешка — Пешка, не имеющая соседей своего цвета на смежных вертикалях. Сила в миттельшпиле, слабость в эндшпиле."
)
bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
elif topic == "fen":
bot.send_message(call.message.chat.id, "🎨 Визуализатор FEN\n\nОтправьте в чат нотацию FEN-строки (например: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1), и бот сгенерирует изображение позиции!")
bot.register_next_step_handler(call.message, process_fen_visualization)
elif topic == "clocks":
send_clocks_setup(call.message.chat.id)
def process_fen_visualization(message):
fen = message.text.strip()
try:
img_url = get_board_image_url(fen)
bot.send_photo(message.chat.id, img_url, caption="🎨 Сгенерированная позиция по вашему FEN-коду.")
except Exception:
bot.send_message(message.chat.id, "❌ Не удалось прочитать FEN. Попробуйте еще раз через меню Академии.")

---------------------------------------------------------------------


ИНТЕРАКТИВНЫЕ ШАХМАТНЫЕ ЧАСЫ ДЛЯ ИГРЫ ВЖИВУЮ


---------------------------------------------------------------------

def send_clocks_setup(chat_id):
markup = types.InlineKeyboardMarkup()
markup.add(
types.InlineKeyboardButton("Блиц 1+0", callback_data="clk_set_60_0"),
types.InlineKeyboardButton("Рапид 3+2", callback_data="clk_set_180_2"),
types.InlineKeyboardButton("Классика 10+0", callback_data="clk_set_600_0")
)
bot.send_message(chat_id, "⏱️ НАСТРОЙКА ШАХМАТНЫХ ЧАСОВ\n\nВыберите формат времени для живой игры перед реальной доской:", reply_markup=markup)
@bot.callback_query_handler(func=lambda c: c.data.startswith("clk_set_"))
def handle_clock_init(call):
user_id = call.from_user.id
parts = call.data.replace("clk_set_", "").split("_")
total_time = int(parts[0])
inc = int(parts[1])
clocks_db[user_id] = {
"white_time": total_time,
"black_time": total_time,
"inc": inc,
"last_click": time.time(),
"msg_id": 0
}
send_clocks_interface(call.message.chat.id, user_id)
def send_clocks_interface(chat_id, user_id):
data = clocks_db[user_id]
markup = types.InlineKeyboardMarkup(row_width=2)
markup.add(
types.InlineKeyboardButton(f"⚪ Ход Белых ({data['white_time']}с)", callback_data=f"clk_turn_w_{user_id}"),
types.InlineKeyboardButton(f"⚫ Ход Черных ({data['black_time']}с)", callback_data=f"clk_turn_b_{user_id}")
)
msg = bot.send_message(chat_id, "⏱️ ЧАСЫ ИДУТ!\n\nНажимайте кнопку соответствующей стороны, когда делаете ход живыми фигурами, чтобы переключить таймер:", reply_markup=markup)
data["msg_id"] = msg.message_id
@bot.callback_query_handler(func=lambda c: c.data.startswith("clk_turn_"))
def handle_clock_tick(call):
parts = call.data.replace("clk_turn_", "").split("_")
turn = parts[0]
u_id = int(parts[1])
if u_id not in clocks_db:
return
data = clocks_db[u_id]
now = time.time()
elapsed = int(now - data["last_click"])
data["last_click"] = now
if turn == "w":
data["white_time"] = max(0, data["white_time"] - elapsed) + data["inc"]
else:
data["black_time"] = max(0, data["black_time"] - elapsed) + data["inc"]
markup = types.InlineKeyboardMarkup(row_width=2)
markup.add(
types.InlineKeyboardButton(f"⚪ Ход Белых ({data['white_time']}с)", callback_data=f"clk_turn_w_{u_id}"),
types.InlineKeyboardButton(f"⚫ Ход Черных ({data['black_time']}с)", callback_data=f"clk_turn_b_{u_id}")
)
try:
bot.edit_message_reply_markup(call.message.chat.id, data["msg_id"], reply_markup=markup)
except Exception:
pass
@bot.message_handler(func=lambda m: True)
def default_fallback(message):
send_main_menu(message.chat.id)
if name == 'main':
print("Бот успешно запущен в соло-режиме...")
bot.infinity_polling()
