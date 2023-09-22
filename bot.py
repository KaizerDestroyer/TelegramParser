from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import csv

api_id = 
api_hash = ""
phone = ""

client = TelegramClient(phone, api_id, api_hash)

client.start()

group_name = "Казахи в Дубай"  # Замените на точное название вашей группы

# Найти ID группы по ее названию
async def find_group_id():
    async for dialog in client.iter_dialogs():
        if dialog.title == group_name:
            return dialog.entity.id

async def main():
    group_id = await find_group_id()
    if not group_id:
        print(f"Группа с названием '{group_name}' не найдена.")
        return

    offset_id = 0
    limit = 100
    keywords = ["Арендую машину", "Аренда машины"]  

    all_messages = []
    total_messages = 0
    total_count_limit = 0

    while True:
        history = await client(GetHistoryRequest(
            peer=group_id,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        
        if not history.messages:
            break
        
        messages = history.messages
        for message in messages:
            if any(keyword in message.message.lower() for keyword in keywords):
                all_messages.append(message.message)
        
        offset_id = messages[-1].id
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    if all_messages:
        print("Сохраняем данные в файл...")
        with open("chats.csv", "w", encoding="UTF-8") as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            for message in all_messages:
                writer.writerow([message])
        print('Парсинг сообщений успешно выполнен.')
    else:
        print('Не найдено сообщений с ключевыми словами.')

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())