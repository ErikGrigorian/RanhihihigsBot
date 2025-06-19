# main.py

import asyncio
from aiogram import Bot, Dispatcher, types
from handlers.start import router, pending_users
import config


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Начать"),
        types.BotCommand(command="/help", description="Помощь и информация")
    ]
    await bot.set_my_commands(commands)


async def check_subscriptions(bot: Bot):
    while True:
        for user_id in list(pending_users):
            try:
                chat_member = await bot.get_chat_member(config.GROUP_ID, user_id)
                if chat_member.status in ['member', 'administrator', 'creator']:
                    await bot.send_message(user_id, config.LINKS_MESSAGE)
                    pending_users.discard(user_id)
            except Exception as e:
                print(f"[ERROR] Не удалось проверить пользователя {user_id}: {e}")

        await asyncio.sleep(10)


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    # Устанавливаем команды
    await set_commands(bot)

    dp.include_router(router)

    # Запуск фоновой проверки
    asyncio.create_task(check_subscriptions(bot))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())