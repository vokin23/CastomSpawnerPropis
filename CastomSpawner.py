import discord
import asyncio
import json
import re

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

message_data = {}


def get_count_users(leader):
    with open('CustomSpawnPlayerConfig.txt', 'r') as file:
        data = file.read()  # Читаем содержимое файла

    with open('config.json', 'r', encoding='utf-8') as file:
        data1 = json.load(file)

    substring = f'|{data1[leader]["group_id"]}|'
    count = data.count(substring)
    return count


async def read_constant_from_json(constant: object) -> object:
    while True:
        with open('settings.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            constants = data[constant]
            await asyncio.sleep(1)
            return constants


def clear_zero_lines():
    with open('C:\\MGStalker\\servers\\StalkerRP\\profiles\\CustomSpawnPlayerConfig.txt', 'r') as file:
        lines = file.readlines()
        non_empty_lines = [line for line in lines if line.strip() != '']

    with open('C:\\MGStalker\\servers\\StalkerRP\\profiles\\CustomSpawnPlayerConfig.txt', 'w') as file:
        file.writelines(non_empty_lines)


def extract_numbers_with_seven(data):
    numbers = re.findall(r'\b7\d{16}\b', data)
    return numbers


@client.event
async def on_ready():
    print(f'{client.user} запустился!')


@client.event
async def on_message(message):
    if isinstance(message.channel, discord.TextChannel):
        if message.channel.name == 'общее':
            # Игнорируем сообщения ботов
            if message.author == client.user:
                return

            steams_id = extract_numbers_with_seven(message.content)
            propisat = steams_id

            with open('config.json', 'r', encoding='utf-8') as file:
                data = json.load(file)

            with open('donat_slot.json', 'r', encoding='utf-8') as file:
                donat_slots = json.load(file)

            if message.author.name in data:
                if "прописать" in message.content.lower():
                    with open('CustomSpawnPlayerConfig.txt', 'r', encoding='utf-8') as file:
                        lines_inv = file.readlines()

                        for line_inv in lines_inv:
                            for steam_id in steams_id:
                                if steam_id in line_inv:
                                    propisat.remove(steam_id)
                                    first_occurrence = line_inv.find("|")  # находим первое вхождение
                                    second_occurrence = line_inv.find("|", first_occurrence + 1)
                                    third_occurrence = line_inv.find("|", second_occurrence + 1)
                                    gp_id = line_inv[second_occurrence + 1:third_occurrence]
                                    for key, value in data.items():
                                        if "group_id" in value and value["group_id"] == str(gp_id):
                                            gp_name = value["leader"]
                                            await message.channel.send(f'{steam_id} уже находится группировке {gp_name}!')

                        if get_count_users(message.author.name) < data[message.author.name]["slots"] and lines_inv.count(f'{steam_id}') == 0:
                            with open('CustomSpawnPlayerConfig.txt', 'a', encoding='utf-8') as file:
                                if len(propisat) > 0:
                                    for item in propisat:
                                        file.write(f'\n{item}|{data[message.author.name]["parametr"]}|'
                                                   f'{data[message.author.name]["group_id"]}|'
                                                   f'{data[message.author.name]["cords_spawner"]}')

                        elif 10 <= get_count_users(message.author.name) < 15 and lines_inv.count(f'{steam_id}') == 0:
                            try:
                                if donat_slots[steam_id]["rank"] == "10-15":
                                    with open('CustomSpawnPlayerConfig.txt', 'a', encoding='utf-8') as file:
                                        if len(propisat) > 0:
                                            for item in propisat:
                                                file.write(f'\n{item}|{data[message.author.name]["parametr"]}|'
                                                           f'{data[message.author.name]["group_id"]}|'
                                                           f'{data[message.author.name]["cords_spawner"]}')

                            except:
                                await message.channel.send(f'Пропись невозможна!\n'
                                                           f'Либо в групперовке уже занято {data[message.author.name]["slots"]}, либо у {steam_id} нет донат-слота!')

                    # Добавляем реакцию на сообщение
                    await message.add_reaction("👍")

                elif "выписать" in message.content.lower():
                    with open('CustomSpawnPlayerConfig.txt', 'r', encoding='utf-8') as file:
                        lines = file.readlines()

                    filtered_lines = []
                    for line in lines:
                        first_occurrence = line.find("|")  # находим первое вхождение
                        second_occurrence = line.find("|", first_occurrence + 1)
                        third_occurrence = line.find("|", second_occurrence + 1)
                        gp_id2 = line[second_occurrence + 1:third_occurrence]
                        should_add = True
                        for steam_id in steams_id:
                            if steam_id in line and data[message.author.name]["group_id"] == gp_id2:
                                should_add = False
                                break
                        if should_add:
                            filtered_lines.append(line)

                    with open('CustomSpawnPlayerConfig.txt', 'w', encoding='utf-8') as file:
                        file.writelines(filtered_lines)

                    clear_zero_lines()
                    await message.add_reaction("👍")


client.run(asyncio.run(read_constant_from_json("token")))
