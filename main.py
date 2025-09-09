import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from random import randint

API_TOKEN = "TOKEN"

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

user_id=[]

# Text fayldan savollarni o‘qib olish
def load_questions_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    blocks = content.strip().split("\n\n")

    questions = []
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue
        question_text = lines[0].strip()
        options = []
        correct_option = None
        for idx, line in enumerate(lines[1:]):
            if line.startswith("*"):
                correct_option = idx
                line = line[1:]
            options.append(line.strip())
        questions.append({
            "question": question_text,
            "options": options,
            "correct": correct_option
        })
    return questions

questions = load_questions_from_txt("questions.txt")

questions_numbers = []
while questions_numbers.__len__() != questions.__len__():
        test_number = randint(0, questions.__len__()-1)
        if test_number in questions_numbers:
            pass
        else:
            questions_numbers.append(test_number)

@dp.message(F.text)
async def start_test(message: types.Message):
    if message.from_user.id in user_id:
        await message.answer("Siz testni bir marta topshirishingiz mumkin.\nVa siz topshirdingiz.")
        await message.answer(f"To'g'ri javoblar soni: {response}")
        return
    else:
        await send_question(message.chat.id, 0)

async def send_question(chat_id, question_index):
    if question_index >= len(questions):
        await bot.send_message(chat_id, "✅ Test tugadi. Rahmat!")
        return
    print(questions_numbers)
    print(question_index)
    q1 = questions[questions_numbers[question_index]]
    q = f"{question_index+1})" + q1["question"][4:q1["question"].__len__()]
    builder = InlineKeyboardBuilder()

    for i, option in enumerate(q1["options"]):
        builder.button(
            text=option,
            callback_data=f"{question_index}:{i}"
        )
    builder.adjust(1)
    markup = builder.as_markup()
    await bot.send_message(chat_id, f"<b>{q}</b>", reply_markup=markup)

response = 0

@dp.callback_query()
async def handle_answer(callback: types.CallbackQuery):
    global response
    data = callback.data
    question_index, selected_index = map(int, data.split(":"))
    correct_index = questions[question_index]["correct"]

    if selected_index == correct_index:
        response += 1 
    else:
        pass
    if question_index + 1 >= len(questions):
        user_id.append(callback.from_user.id)
        await callback.message.answer(f"✅ Test tugadi. To'g'ri javoblar soni: {response}")
    await callback.answer()
    await send_question(callback.message.chat.id, question_index + 1)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
