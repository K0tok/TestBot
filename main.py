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
        "Список команд данного бота:\n\nstart - Начало работы\nhelp - Справка по командам бота и работе с ним\nabout - Информация об авторе\nrandom - Случайное число от 0 до 100\njoke - Получение случайных шуток или анекдотов\nmath - Вывод случайного примера уравнения",
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
