# handlers/start_handler.py

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config

router = Router()
pending_users=set()


# --- Существующая команда /start ---
@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "unknown"

    # Добавляем пользователя в список отслеживаемых (если используется polling)
    pending_users.add(user_id)

    try:
        chat_member = await message.bot.get_chat_member(chat_id=config.GROUP_ID, user_id=user_id)

        if chat_member.status in ['member', 'administrator', 'creator']:
            await message.answer(config.LINKS_MESSAGE)
        else:
            invite_link = await message.bot.create_chat_invite_link(
                chat_id=config.GROUP_ID,
                name=f"Invite for {user_id}",
                member_limit=1
            )

            kb = InlineKeyboardBuilder()
            kb.row(types.InlineKeyboardButton(text="Присоединиться", url=invite_link.invite_link))
            await message.answer("Подпишитесь на группу для получения ссылок:", reply_markup=kb.as_markup())
    except Exception as e:
        await message.answer("Ошибка при проверке подписки.")
        print(f"[ERROR] {e}")


# --- Новая команда /help ---
HELP_MESSAGE = """
🤖 **Добро пожаловать в бота!**

Этот бот помогает получить доступ к закрытым ссылкам после вступления в приватную группу.

🔹 Чтобы получить ссылки:
1. Нажмите кнопку «Присоединиться»
2. Вступите в группу
3. Бот автоматически отправит вам ссылки

❓ Если возникнут вопросы — напишите @Eriik777
"""

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_MESSAGE)