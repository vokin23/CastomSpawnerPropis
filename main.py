import discord
import json


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


@client.event
async def on_ready():
    print(f'{client.user} запустился!')

@client.event
async def on_message(message):
    if message.channel.name == 'общее':
        # Игнорируем сообщения ботов
        if message.author == client.user:
            return

        steam_id = message.content[message.content.index("7"):message.content.index("7") + 18]

        with open('config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        if message.author.name in data:
            if "прописать" in message.content.lower():
                with open('CustomSpawnPlayerConfig.txt', 'r', encoding='utf-8') as file:
                    lines_inv = file.readlines()

                    for line_inv in lines_inv:
                        if steam_id in line_inv:
                            await message.channel.send(f'{steam_id} уже находится группировке!')
                            break

                        with open('CustomSpawnPlayerConfig.txt', 'a', encoding='utf-8') as file:
                            file.write(f'\n{steam_id}|{data[message.author.name]["parametr"]}|'
                                       f'{data[message.author.name]["group_id"]}|'
                                       f'{data[message.author.name]["cords_spawner"]}')

            elif "выписать" in message.content.lower():
                with open('CustomSpawnPlayerConfig.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    filtered_lines = [line for line in lines if steam_id not in line]

                with open('CustomSpawnPlayerConfig.txt', 'w') as file:
                    file.writelines(filtered_lines)

                clear_zero_lines()

            # Добавляем реакцию на сообщение
            await message.add_reaction("👍")

client.run('Token')
