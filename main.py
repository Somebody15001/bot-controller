import discord
import colorama
from colorama import Fore
from time import sleep
colorama.init(autoreset=True)
import threading
import requests
from database import versionHash


# version control
url = "https://raw.githubusercontent.com/Somebody15001/bot-controller/main/version"
response = requests.get(url)
response.raise_for_status()
content = response.text.strip()

if content == versionHash:
    sleep(1)
    print(f"{Fore.LIGHTGREEN_EX}BCD has the latest version ✔")
    sleep(2)
else:
    sleep(1)
    print(f"{Fore.LIGHTRED_EX}BDC has a new version! --> https://github.com/Somebody15001/bot-controller?tab=readme-ov-file ")
    sleep(999999999)


kanalids = "none"
fullwmode = False
print("\n"*50)
print(f'''
{Fore.LIGHTBLUE_EX}
                $$$$$$$\   $$$$$$\  $$$$$$$\  
                $$  __$$\ $$  __$$\ $$  __$$\ 
                $$ |  $$ |$$ /  \__|$$ |  $$ |
                $$$$$$$\ |$$ |      $$ |  $$ |
                $$  __$$\ $$ |      $$ |  $$ |
                $$ |  $$ |$$ |  $$\ $$ |  $$ |
                $$$$$$$  |\$$$$$$  |$$$$$$$  |
                \_______/  \______/ \_______/                           





''')
sleep(1)
enter_token = input(f"{Fore.LIGHTMAGENTA_EX}Please enter your bot token:{Fore.GREEN}")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

class MyClient(discord.Client):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_channel_id = None
        self.msg_mode_enabled = False
        self.wiw_mode_enabled = False
        self.status_text = ""
        self.status_type = ""

    async def setup_hook(self):
        threading.Thread(target=self.command_listener, daemon=True).start()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.unknown, name=""))

    def command_listener(self):
        global kanalids
        global fullwmode
        sleep(4)
        print(f"{Fore.LIGHTBLUE_EX}INFO    {Fore.LIGHTBLACK_EX} software active")
        while True:
            command = input(f"{Fore.BLUE}")  # Konsoldan komut bekler----------------------------------------------***********************
            if command.strip() == "/msg-mode":
                self.full_wiew_off_task()
                self.msg_mode_enabled = True
                kanalids = input(f"{Fore.LIGHTYELLOW_EX}Enter the channel ID:{Fore.GREEN} ")
                self.target_channel_id = int(kanalids)
                self.send_message_task()  # Mesaj gönderme görevini başlat
            elif command.strip() == "/del":
                self.full_wiew_off_task()
                self.delete_messages_task()  # Mesaj silme görevini başlat
            elif command.strip() == "/wiw":
                self.full_wiew_off_task()
                self.wiw_mode_enabled = True    
                self.set_wiw_status()  # /wiw komutuyla statüyü ayarlama
            elif command.strip() == "/ban":
                self.full_wiew_off_task()
                self.ban_user_task()  # Banlama görevini başlat
            elif command.strip() == "/kick":
                self.full_wiew_off_task()
                self.kick_user_task()  # Kickleme görevini başlat
            elif command.strip() == "/role":
                self.full_wiew_off_task()
                self.assign_role_task()  # Rol atama görevini başlat
            elif command.strip() in ["/help", "/?"]:
                self.full_wiew_off_task()
                self.help_task()  # help komutunu çalıştır
            elif command.strip() == "/unban":
                self.full_wiew_off_task()
                self.unban_user_task() # unban komutunu çalıştır
            elif command.strip() == "/full-view":
                if fullwmode == True:
                    print(f"{Fore.RED}full view mode already enabled")
                else:
                    print(f"{Fore.LIGHTGREEN_EX}full view mode enabled")
                    fullwmode = True
            elif command.strip() == "/fv-off": # full view'i kapat
                if fullwmode == False:
                    print(f"{Fore.LIGHTRED_EX}full view mode already disabled")
                else:
                    self.full_wiew_off_task() 
            else:
                print(f"{Fore.LIGHTRED_EX}Invalid Command")

    def full_wiew_off_task(self):
        global fullwmode
        if fullwmode == True:
            print(f"{Fore.RED}full view mode disabled")
            fullwmode = False


    def help_task(self):
        print(f'''{Fore.LIGHTMAGENTA_EX}
                         /msg-mode ----> /mm-off
                         /full-view ---> /fv-off
                         /del
                         /wiw
                         /kick
                         /ban
                         /unban
                         /role
                      ''')
    def unban_user_task(self):
        guild_id = int(input(f"{Fore.LIGHTYELLOW_EX}Enter the server ID:{Fore.GREEN} "))
        user_id = int(input(f"{Fore.LIGHTYELLOW_EX}Enter the user ID:{Fore.GREEN} "))
        self.loop.create_task(self.unban_user(guild_id, user_id))

    async def unban_user(self, guild_id, user_id):
        guild = self.get_guild(guild_id)
        if guild:
            member = guild.get_member(user_id)
            if member:
                try:
                    await member.unban()
                    print(f"{Fore.LIGHTGREEN_EX}Successfully un banned user:{Fore.YELLOW} {member.name}")
                except discord.Forbidden:
                    print(f"{Fore.RED}Bot does not have permission to un ban members!")
                except Exception as e:
                    print(f"{Fore.RED}Error: {e}")
        else:
            print(f"{Fore.RED}Server not found!")

    def ban_user_task(self):
        guild_id = int(input(f"{Fore.LIGHTYELLOW_EX}Enter the server ID:{Fore.GREEN} "))
        user_id = int(input(f"{Fore.LIGHTYELLOW_EX}Enter the user ID:{Fore.GREEN} "))
        self.loop.create_task(self.ban_user(guild_id, user_id))

    async def ban_user(self, guild_id, user_id):
        guild = self.get_guild(guild_id)
        if guild:
            member = guild.get_member(user_id)
            if member:
                try:
                    await member.ban(reason="Banned by bot command")
                    print(f"{Fore.LIGHTGREEN_EX}Successfully banned user:{Fore.YELLOW} {member.name}")
                except discord.Forbidden:
                    print(f"{Fore.RED}Bot does not have permission to ban members!")
                except Exception as e:
                    print(f"{Fore.RED}Error: {e}")
            else:
                print(f"{Fore.RED}User not found in the server!")
        else:
            print(f"{Fore.RED}Server not found!")

    def kick_user_task(self):
        guild_id = int(input(f"{Fore.LIGHTYELLOW_EX}Enter the server ID:{Fore.GREEN} "))
        user_id = int(input(f"{Fore.LIGHTYELLOW_EX}Enter the user ID:{Fore.GREEN} "))
        self.loop.create_task(self.kick_user(guild_id, user_id))


    async def kick_user(self, guild_id, user_id,):
        guild = self.get_guild(guild_id)
        if guild:
            member = guild.get_member(user_id)
            if member:
                try:
                    await member.kick(reason= f"Kicked from {user_id}(BCD)")
                    print(f"{Fore.LIGHTGREEN_EX}Successfully kicked user:{Fore.YELLOW}{member.name}")
                except discord.Forbidden:
                    print(f"{Fore.RED}Bot does not have permission to kick members!")
                except Exception as e:
                    print(f"{Fore.RED}Error: {e}")
            else:
                print(f"{Fore.RED}User not found in the server!")
        else:
            print(f"{Fore.RED}Server not found!")

    def send_message_task(self):
        sleep(2)
        print(f"{Fore.LIGHTGREEN_EX}msg mode enabled")
        while self.msg_mode_enabled:
            sleep(1)
            try:
                message = input()  # Kullanıcıdan mesaj alın
                if message == "/mm-off":
                    self.msg_mode_enabled = False
                    print(f"{Fore.LIGHTRED_EX}msg mode disabled")
                else:
                    self.loop.create_task(self.send_message_to_channel(message))
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")

    async def send_message_to_channel(self, message):
        channel = self.get_channel(self.target_channel_id)
        if channel:
            await channel.send(message)
        else:
            print(f"{Fore.RED}Channel not found!")

    async def on_message(self, message):
        if self.msg_mode_enabled:
            if int(kanalids) == message.channel.id:
                print(f"{Fore.YELLOW}{message.author}:{Fore.RESET} {message.content}")
        elif fullwmode:
                print(f"{Fore.YELLOW}{message.author}:{Fore.RESET} {message.content}               {Fore.LIGHTYELLOW_EX}|{Fore.MAGENTA}{message.guild.name} {Fore.LIGHTYELLOW_EX}[{Fore.LIGHTCYAN_EX}{message.channel.name}{Fore.LIGHTYELLOW_EX}]")  

    def delete_messages_task(self):
        kanalids = input(f"{Fore.LIGHTYELLOW_EX}Enter the channel ID:{Fore.GREEN} ")
        mesaj_sayisi = int(input(f"{Fore.LIGHTYELLOW_EX}Enter the number of messages to delete:{Fore.LIGHTRED_EX} "))
        self.loop.create_task(self.delete_messages(kanalids, mesaj_sayisi))  # Mesaj silme görevini başlat

    async def delete_messages(self, channel_id, num_messages):
        await self.wait_until_ready() 
        channel = self.get_channel(int(channel_id)) 
        if channel:
            try:
                messages = []
                async for message in channel.history(limit=num_messages):
                    messages.append(message)
                    
                for msg in messages:
                    try:
                        await msg.delete()
                        print(f"{Fore.LIGHTRED_EX}Deleted message: {msg.content} ({Fore.YELLOW}{msg.author}{Fore.RESET})")
                    except discord.Forbidden:
                        print(f"{Fore.RED}Bot does not have permission to delete messages! Ensure the bot has the 'Manage Messages' permission.")
                    except discord.HTTPException as e:
                        print(f"{Fore.RED}HTTP Exception occurred: {e} - Possibly a rate limit issue or invalid request.")
                    except Exception as e:
                        print(f"{Fore.RED}Error deleting message: {e}")
            except discord.NotFound:
                print(f"{Fore.RED}Channel with ID {channel_id} not found!")
            except discord.Forbidden:
                print(f"{Fore.RED}Bot does not have permission to access channel {channel_id}.")
            except Exception as e:
                print(f"{Fore.RED}Error fetching messages: {e}")

    def set_wiw_status(self):
        self.status_text = input(f"{Fore.LIGHTYELLOW_EX}Enter status text:{Fore.GREEN} ")
        status_type = input(f"{Fore.LIGHTYELLOW_EX}Enter status type(p=playing, s=streaming, l=listening, w=watching):{Fore.GREEN} ")

        status_types = {
            "p": discord.ActivityType.playing, 
            "s": discord.ActivityType.streaming,
            "l": discord.ActivityType.listening,
            "w": discord.ActivityType.watching
        }

        if status_type.lower() in status_types:
            self.status_type = status_types[status_type.lower()]
            self.loop.create_task(self.update_wiw_status())
        else:
            print(f"{Fore.RED}Invalid status type! Use one of: playing, streaming, listening, watching")

    async def update_wiw_status(self):
        await self.wait_until_ready()
        activity = discord.Activity(type=self.status_type, name=self.status_text)
        await self.change_presence(activity=activity)
        print(f"{Fore.LIGHTGREEN_EX}Status updated to: {self.status_text} ({self.status_type.name})")

    def assign_role_task(self):
        guild_id = int(input(f"{Fore.LIGHTYELLOW_EX}Enter the server ID:{Fore.GREEN} "))
        user_id = int(input(f"{Fore.LIGHTYELLOW_EX}Enter the user ID:{Fore.GREEN} "))
        role_id = int(input(f"{Fore.LIGHTYELLOW_EX}Enter the role ID:{Fore.GREEN} "))
        self.loop.create_task(self.assign_role(guild_id, user_id, role_id))

    async def assign_role(self, guild_id, user_id, role_id):
        guild = self.get_guild(guild_id)
        if guild:
            member = guild.get_member(user_id)
            role = guild.get_role(role_id)
            if member and role:
                try:
                    await member.add_roles(role)
                    print(f'{Fore.LIGHTGREEN_EX}Successfully assigned role "{role.name}" to user {Fore.YELLOW}{member.display_name}')
                except discord.Forbidden:
                    print(f"{Fore.RED}Bot does not have permission to assign roles!")
                except Exception as e:
                    print(f"{Fore.RED}Error: {e}")
            else:
                if not member:
                    print(f"{Fore.RED}User not found in the guild!")
                if not role:
                    print(f"{Fore.RED}Role not found!")
        else:
            print(f"{Fore.RED}Guild not found!")

client = MyClient(intents=intents)
client.run(enter_token)