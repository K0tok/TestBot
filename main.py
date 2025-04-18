import telebot
import config
import random

bot = telebot.TeleBot(config.TG_API_TOKEN)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)

keyboard1.row("Привет", "Пока")
keyboard1.row("Какая сегодня погода?")

keyboard_commands = telebot.types.ReplyKeyboardMarkup(True)
keyboard_commands.row("/start", "/help", "/about")
keyboard_commands.row("/random", "/joke", "/math")

simpleAnswerKeyboard = telebot.types.InlineKeyboardMarkup()
yesButton = telebot.types.InlineKeyboardButton("Да", callback_data="yes")
noButton = telebot.types.InlineKeyboardButton("Нет", callback_data="no")
simpleAnswerKeyboard.row(yesButton, noButton)

gameKeyboard = telebot.types.ReplyKeyboardMarkup(True)
gameKeyboard.row("Больше ⬆️", "Меньше ⬇️")
gameKeyboard.row("Угадал!")

gameCount = 0

f = open("data/fun.txt", "r", encoding="UTF-8")
jokes = f.read().split("\n")
f.close()


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать в ЭДС!", reply_markup=keyboard1)


@bot.message_handler(commands=["help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Список команд данного бота:\n\n/start - Начало работы\n/help - Справка по командам бота и работе с ним\n/about - Информация об авторе\n/random - Случайное число от 0 до 100\n/joke - Получение случайных шуток или анекдотов\n/math - Вывод случайного примера уравнения\n/play - игра с угадыванием числа",
        reply_markup=keyboard_commands,
    )


@bot.message_handler(commands=["joke"])
def send_joke(message):
    bot.send_message(message.chat.id, jokes[random.randint(0, 7)])


@bot.message_handler(commands=["random", "rnd"])
def send_rnd(message):
    bot.send_message(message.chat.id, random.randint(0, 100))


@bot.message_handler(commands=["about"])
def send_about(message):
    bot.send_message(message.chat.id, "Создатель бота: @K0tok")


@bot.message_handler(commands=["calc", "math"])
def send_calculation(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Отправь мне простой пример, а я его решу!")
    bot.register_next_step_handler(message, second_message)


def second_message(message):
    first_text = message.text
    # symbol = ""
    # res = 0
    # err = False
    # if "+" in first_text:
    #     task = first_text.split("+")
    #     symbol = "+"
    #     res = int(task[0]) + int(task[1])
    # elif "-" in first_text:
    #     task = first_text.split("-")
    #     symbol = "-"
    #     res = int(task[0]) - int(task[1])
    # elif "/" in first_text:
    #     task = first_text.split("/")
    #     symbol = "/"
    #     res = int(task[0]) / int(task[1])
    # elif "*" in first_text:
    #     task = first_text.split("*")
    #     symbol = "*"
    #     res = int(task[0]) * int(task[1])
    # else:
    #     bot.send_message(message.chat.id, "Неверный формат ввода, попробуйте снова!")
    #     err = True
    # if not err:
    #     bot.send_message(message.chat.id, f"{task[0]} {symbol} {task[1]} = {res}")
    bot.send_message(message.chat.id, f"{first_text}={eval(first_text)}")


@bot.message_handler(commands=["game", "play"])
def send_gamerule(message: telebot.types.Message):
    count = 0
    bot.send_message(
        message.chat.id,
        "Давай поиграем в игру! Загадай число от 1 до 100, а я его угадаю.\nИграем?;)",
        reply_markup=simpleAnswerKeyboard,
    )


def game(message, low, high, num):
    global gameCount
    first_text = message.text
    if gameCount == 0:
        bot.send_message(
            message.chat.id,
            f"Начнём игру!\nЗагадай число от 1 до 100 и отвечай на мои вопросы.\n\nМне кажется, что ты загадал число - 50",
            reply_markup=gameKeyboard,
        )
        gameCount += 1
        bot.register_next_step_handler(message, game, low, high, num)
    else:
        if "Угадал!" in first_text:
            bot.send_message(
                message.chat.id,
                f"Ура! Твоё число {num}. Я угадал его за {gameCount} попыток.",
            )
            gameCount = 0
        elif "Больше" in first_text:
            low = num + 1
            num = (high + low) // 2
            bot.send_message(
                message.chat.id,
                f"Твоё число - {num}?",
                reply_markup=gameKeyboard,
            )
            gameCount += 1
            bot.register_next_step_handler(message, game, low, high, num)
        elif "Меньше" in first_text:
            high = num - 1
            num = (high + low) // 2
            bot.send_message(
                message.chat.id,
                f"Твоё число - {num}?",
                reply_markup=gameKeyboard,
            )
            gameCount += 1
            bot.register_next_step_handler(message, game, low, high, num)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global gameCount
    if callback.data == "yes":
        game(callback.message, 0, 100, 50)
    if callback.data == "no":
        gameCount = 0
        bot.send_message(callback.message.chat.id, "Поиграем в другой раз)")


@bot.message_handler(func=lambda message: True)
def echo_all(message: telebot.types.Message):
    if message.text == "Привет":
        bot.reply_to(message, f"Привет, {message.from_user.first_name}!")
    if message.text == "Какая сегодня погода?":
        bot.reply_to(message, f"Замечательная!")
    if message.text == "Пока":
        bot.reply_to(
            message,
            f"Досвидания, {message.from_user.first_name}.\nБуду скучать!",
        )


bot.infinity_polling()
