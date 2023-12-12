import discord
import json
import re


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

message_data = {}


def clear_zero_lines():
    with open('CustomSpawnPlayerConfig.txt', 'r') as file:
        lines = file.readlines()
        non_empty_lines = [line for line in lines if line.strip() != '']

    with open('CustomSpawnPlayerConfig.txt', 'w') as file:
        file.writelines(non_empty_lines)


def extract_numbers_with_seven(data):
    numbers = re.findall(r'\b7\d{16}\b', data)
    return numbers



@client.event
async def on_ready():
    print(f'{client.user} запустился!')

@client.event
async def on_message(message):
    if message.channel.name == 'общее':
        # Игнорируем сообщения ботов
        if message.author == client.user:
            return

        steams_id = extract_numbers_with_seven(message.content)
        propisat = steams_id

        with open('config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

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
                                gp_id = line_inv[second_occurrence + 1]
                                for key, value in data.items():
                                    if "group_id" in value and value["group_id"] == str(gp_id):
                                        gp_name = value["leader"]
                                        await message.channel.send(f'{steam_id} уже находится группировке {gp_name}!')

                    with open('CustomSpawnPlayerConfig.txt', 'a', encoding='utf-8') as file:
                        if len(propisat) > 0:
                            for item in propisat:
                                file.write(f'\n{item}|{data[message.author.name]["parametr"]}|'
                                           f'{data[message.author.name]["group_id"]}|'
                                           f'{data[message.author.name]["cords_spawner"]}')

                # Добавляем реакцию на сообщение
                await message.add_reaction("✅")

            elif "выписать" in message.content.lower():
                with open('CustomSpawnPlayerConfig.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                filtered_lines = [line for line in lines if not any(steam_id in line for steam_id in steams_id)]

                with open('CustomSpawnPlayerConfig.txt', 'w') as file:
                    file.writelines(filtered_lines)

                clear_zero_lines()
                # Добавляем реакцию на сообщение
                await message.add_reaction("✅")


client.run('Token')