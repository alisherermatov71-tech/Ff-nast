import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

TOKEN = "8811948718:AAGucLw_3ia7EIWp5OfWUMUunjN80l9VFh8"

# Міндетті канал автоматты түрде қосылды
BOT_SETTINGS = {"required_channel": "@alibiznezmen"}

ADMIN_IDS = [8078029788]

router = Router()

# Настройкалар базасы
settings_data = {
    "iphone11": (
        "📱 **iPhone 11 / 11 Pro Настройкасы (200 шк)**\n\n"
        "• Жалпы көрініс (Общий): **190**\n"
        "• Коллиматор (Red Dot): **185**\n"
        "• 2x Прицел: **175**\n"
        "• 4x Прицел: **180**\n"
        "• Снайпер көрінісі: **110**\n"
        "• Обзор (Басқару): **150**\n\n"
        "🎯 **От кнопкасы (Размер):** `45%`\n"
        "📍 **Орналасуы:** Экранның төменгі оң жақ бұрышы."
    ),
    "iphone12": (
        "📱 **iPhone 12 / 12 Pro Настройкасы (200 шк)**\n\n"
        "• Жалпы көрініс (Общий): **195**\n"
        "• Коллиматор (Red Dot): **190**\n"
        "• 2x Прицел: **180**\n"
        "• 4x Прицел: **185**\n"
        "• Снайпер көрінісі: **120**\n"
        "• Обзор (Басқару): **160**\n\n"
        "🎯 **От кнопкасы (Размер):** `42%`\n"
        "📍 **Орналасуы:** Орталықтан сәл төмен."
    ),
    "iphone13": (
        "📱 **iPhone 13 / 13 Pro Настройкасы (200 шк)**\n\n"
        "• Жалпы көрініс (Общий): **198**\n"
        "• Коллиматор (Red Dot): **193**\n"
        "• 2x Прицел: **185**\n"
        "• 4x Прицел: **190**\n"
        "• Снайпер көрінісі: **130**\n"
        "• Обзор (Басқару): **170**\n\n"
        "🎯 **От кнопкасы (Размер):** `40%`\n"
        "📍 **Орналасуы:** Төменгі бөлік."
    ),
    "iphone14": (
        "📱 **iPhone 14 / 14 Pro Настройкасы (200 шк)**\n\n"
        "• Жалпы көрініс (Общий): **200**\n"
        "• Коллиматор (Red Dot): **195**\n"
        "• 2x Прицел: **190**\n"
        "• 4x Прицел: **192**\n"
        "• Снайпер көрінісі: **140**\n"
        "• Обзор (Басқару): **180**\n\n"
        "🎯 **От кнопкасы (Размер):** `38%`\n"
        "📍 **Орналасуы:** Экран ортасының асты."
    ),
    "iphone15": (
        "📱 **iPhone 15 / 15 Pro Настройкасы (200 шк)**\n\n"
        "• Жалпы көрініс (Общий): **200**\n"
        "• Коллиматор (Red Dot): **198**\n"
        "• 2x Прицел: **194**\n"
        "• 4x Прицел: **196**\n"
        "• Снайпер көрінісі: **150**\n"
        "• Обзор (Басқару): **185**\n\n"
        "🎯 **От кнопкасы (Размер):** `35%`\n"
        "📍 **Орналасуы:** Динамикалық аймақтан төмен."
    ),
    "iphone16": (
        "📱 **iPhone 16 / 16 Pro Настройкасы (200 шк)**\n\n"
        "• Жалпы көрініс (Общий): **200**\n"
        "• Коллиматор (Red Dot): **200**\n"
        "• 2x Прицел: **196**\n"
        "• 4x Прицел: **198**\n"
        "• Снайпер көрінісі: **160**\n"
        "• Обзор (Басқару): **190**\n\n"
        "🎯 **От кнопкасы (Размер):** `36%`\n"
        "📍 **Орналасуы:** Оң жақ төмен."
    ),
    "iphone17": (
        "🔥 **iPhone 17 / 17 Pro Max (Pro Gamer 200 шк)**\n\n"
        "• Жалпы көрініс (Общий): **200**\n"
        "• Коллиматор (Red Dot): **200**\n"
        "• 2x Прицел: **200**\n"
        "• 4x Прицел: **200**\n"
        "• Снайпер көрінісі: **170**\n"
        "• Обзор (Басқару): **200**\n\n"
        "🎯 **От кнопкасы (Размер):** `34%`\n"
        "📍 **Орналасуы:** Авто-хедшот үшін идеальный!"
    ),
}


# FSM күйлері
class AdminStates(StatesGroup):
  waiting_for_model_key = State()
  waiting_for_model_text = State()
  waiting_for_delete_key = State()
  waiting_for_channel = State()


def get_main_menu():
  buttons = []
  for key in settings_data.keys():
    name = "📱 " + key.replace("iphone", "iPhone ").upper()
    buttons.append([InlineKeyboardButton(text=name, callback_data=f"model_{key}")])
  return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_menu():
  return InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="⬅️ Артқа қайту", callback_data="back_to_menu"
              )
          ]
      ]
  )


# Каналға тіркелуді тексеру
async def check_subscription(user_id: int, bot: Bot):
  channel = BOT_SETTINGS.get("required_channel")
  if not channel or channel == "@none":
    return True
  try:
    member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    if member.status in ["member", "administrator", "creator"]:
      return True
  except Exception:
    pass
  return False


@router.message(Command("start"))
async def cmd_start(message: Message, bot: Bot):
  is_subscribed = await check_subscription(message.from_user.id, bot)

  if not is_subscribed:
    channel = BOT_SETTINGS.get("required_channel")
    sub_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Каналға қосылу", url=f"https://t.me/{channel[1:]}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Тексеру", callback_data="check_sub"
                )
            ],
        ]
    )
    await message.answer(
        "⚠️ **Ботты қолдану үшін төмендегі арнамызға тіркеліңіз!**\n\n"
        "Тіркеліп болған соң «✅ Тексеру» батырмасын басыңыз.",
        reply_markup=sub_keyboard,
        parse_mode="Markdown",
    )
    return

  await show_start_menu(message)


async def show_start_menu(message: Message):
  text = (
      "🔥 **Free Fire Настройка Ботына қош келдіңіз!**\n\n"
      "Төмендегі тізімнен өз iPhone телефоныңызды таңдаңыз:"
  )
  await message.answer(text, reply_markup=get_main_menu(), parse_mode="Markdown")


@router.callback_query(F.data == "check_sub")
async def process_check_sub(callback: CallbackQuery, bot: Bot):
  is_subscribed = await check_subscription(callback.from_user.id, bot)
  if is_subscribed:
    await callback.message.delete()
    await show_start_menu(callback.message)
  else:
    await callback.answer(
        "❌ Сіз әлі каналға тіркелмедіңіз!", show_alert=True
    )


# Админ панель
@router.message(Command("admin"))
async def cmd_admin(message: Message):
  if message.from_user.id not in ADMIN_IDS:
    await message.answer("❌ Бұл команда тек әкімшіге арналған!")
    return

  current_ch = BOT_SETTINGS.get("required_channel")
  admin_keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="➕ Настройка қосу", callback_data="admin_add"
              ),
              InlineKeyboardButton(
                  text="🗑 Настройка өшіру", callback_data="admin_delete"
              ),
          ],
          [
              InlineKeyboardButton(
                  text="📢 Канал қосу / Өзгерту", callback_data="admin_set_channel"
              ),
              InlineKeyboardButton(
                  text="❌ Каналды өшіру", callback_data="admin_remove_channel"
              ),
          ],
          [
              InlineKeyboardButton(
                  text="⬅️ Шығу", callback_data="back_to_menu"
              )
          ],
      ]
  )
  await message.answer(
      f"🛠 **Админ панельге қош келдіңіз!**\n\n"
      f"📌 Қазіргі міндетті канал: `{current_ch}`\n\n"
      f"Не істегіңіз келеді?",
      reply_markup=admin_keyboard,
      parse_mode="Markdown",
  )


# --- Админ: Настройка қосу ---
@router.callback_query(F.data == "admin_add")
async def admin_add_start(callback: CallbackQuery, state: FSMContext):
  if callback.from_user.id not in ADMIN_IDS:
    return
  await callback.message.answer(
      "Жаңа модельдің коды мен атын жазыңыз (Мысалы: `iphone18`):"
  )
  await state.set_state(AdminStates.waiting_for_model_key)
  await callback.answer()


@router.message(AdminStates.waiting_for_model_key)
async def admin_get_key(message: Message, state: FSMContext):
  await state.update_data(model_key=message.text.strip().lower())
  await message.answer(
      "Енді осы модельдің **толық настройка мәтінін** жіберіңіз:"
  )
  await state.set_state(AdminStates.waiting_for_model_text)


@router.message(AdminStates.waiting_for_model_text)
async def admin_get_text(message: Message, state: FSMContext):
  data = await state.get_data()
  key = data.get("model_key")
  settings_data[key] = message.text
  await state.clear()
  await message.answer(
      f"✅ Сәтті қосылды! (`{key}`)\n/admin арқылы басқаруға болады."
  )


# --- Админ: Настройканы өшіру ---
@router.callback_query(F.data == "admin_delete")
async def admin_delete_start(callback: CallbackQuery, state: FSMContext):
  if callback.from_user.id not in ADMIN_IDS:
    return
  text = "🗑 Өшіргіңіз келген модельдің **ключын** жазыңыз:\n\nБар ключылар:\n"
  for k in settings_data.keys():
    text += f"- `{k}`\n"
  await callback.message.answer(text, parse_mode="Markdown")
  await state.set_state(AdminStates.waiting_for_delete_key)
  await callback.answer()


@router.message(AdminStates.waiting_for_delete_key)
async def admin_process_delete(message: Message, state: FSMContext):
  key = message.text.strip().lower()
  if key in settings_data:
    del settings_data[key]
    await state.clear()
    await message.answer(
        f"✅ `{key}` настройкасы сәтті өшірілді!", parse_mode="Markdown"
    )
  else:
    await message.answer("❌ Мұндай ключ табылмады. Қайта жазыңыз:")


# --- Админ: Міндетті каналды қосу / өзгерту ---
@router.callback_query(F.data == "admin_set_channel")
async def admin_set_channel_start(callback: CallbackQuery, state: FSMContext):
  if callback.from_user.id not in ADMIN_IDS:
    return
  await callback.message.answer(
      "📢 Жаңа каналдың username-ін жазыңыз (Мысалы: `@alibiznezmen`):"
  )
  await state.set_state(AdminStates.waiting_for_channel)
  await callback.answer()


@router.message(AdminStates.waiting_for_channel)
async def admin_save_channel(message: Message, state: FSMContext):
  ch = message.text.strip()
  if not ch.startswith("@"):
    ch = "@" + ch
  BOT_SETTINGS["required_channel"] = ch
  await state.clear()
  await message.answer(
      f"✅ Міндетті канал сәтті ауыстырылды: `{ch}`", parse_mode="Markdown"
  )


# --- Админ: Міндетті каналды өшіру ---
@router.callback_query(F.data == "admin_remove_channel")
async def admin_remove_channel(callback: CallbackQuery):
  if callback.from_user.id not in ADMIN_IDS:
    return
  BOT_SETTINGS["required_channel"] = "@none"
  await callback.message.answer(
      "✅ Міндетті канал функциясы өшірілді! Енді қолданушылар каналға тіркелмей-ақ ботты қолдана алады."
  )
  await callback.answer()


@router.callback_query(F.data.startswith("model_"))
async def show_settings(callback: CallbackQuery):
  model_code = callback.data.split("_")[1]
  response_text = settings_data.get(model_code, "Настройка табылмады.")
  await callback.message.edit_text(
      response_text, reply_markup=get_back_menu(), parse_mode="Markdown"
  )
  await callback.answer()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
  text = (
      "🔥 **Free Fire Настройка Ботына қош келдіңіз!**\n\n"
      "Төмендегі тізімнен өз iPhone телефоныңызды таңдаңыз:"
  )
  await callback.message.edit_text(
      text, reply_markup=get_main_menu(), parse_mode="Markdown"
  )
  await callback.answer()


async def main():
  bot = Bot(token=TOKEN)
  dp = Dispatcher()
  dp.include_router(router)

  print("Бот жұмыс істеп тұр...")
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
