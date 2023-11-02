import discord
import asyncio
import io
import chat_exporter
from discord.utils import get
from config import *
from database import *
from bot import *

class addMemberModal(discord.ui.Modal, title="Add a member"):
    answer = discord.ui.TextInput(label='Place Member ID here', style=discord.TextStyle.short, required=True, max_length=128)

    async def on_submit(self, interaction: discord.Interaction):
        tchannel = interaction.channel
        author = interaction.user
        guild = interaction.guild
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        ticketInfo = TicketData.find(cursor, tchannel.id)
        TicketData.close(connection)
        try:
            ltype = (ticketInfo[4])
        except IndexError:
            ltype = str("N/A")
        
        try:
            amember = discord.utils.get(guild.members, id=int(self.children[0].value))
        except Exception:
            amember = None
        if amember == None:
            embed = discord.Embed(description=f'''I couldn't find that member, are you sure that is a valid member id? This is what I got: {self.children[0].value}''', color=embedColor)
            embed.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            embed.set_author(name=f'{author}', icon_url=author.display_avatar)
            try:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except discord.HTTPException:
                await interaction.response.send_message(f'''I couldn't find that member, are you sure that is a valid member id? This is what I got: {self.children[0].value}''', ephemeral=True)
        elif amember != None:
            try:
                for allowedRoles in list(channelPerms[f"{ltype}"]):
                    prole = discord.utils.get(guild.roles, id=allowedRoles)
                    if prole in amember.roles:
                        allowedAcess = True
                    else:
                        pass
            except TypeError:
                prole = get(guild.roles, id=channelPerms[f"{ltype}"])
                if prole in author.roles:
                    allowedAcess = True
                else:
                    pass
            if (allowedAcess == True):
                embed2 = discord.Embed(description=f'''I can't add that member!''', color=embedColor)
                embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
                embed2.set_author(name=f'{author}', icon_url=author.display_avatar)
                try:
                    await interaction.response.send_message(embed=embed2, ephemeral=True)
                except discord.HTTPException:
                    await interaction.response.send_message(f'''I can't add that member!`''', ephemeral=True)
            else:
                await tchannel.set_permissions(amember, send_messages=True, read_messages=True)
                embed2 = discord.Embed(description=f'''Member added. ✅''', color=embedColor)
                embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
                embed2.set_author(name=f'{author}', icon_url=author.display_avatar)
                try:
                    await interaction.response.send_message(embed=embed2, ephemeral=True)
                except discord.HTTPException:
                    await interaction.response.send_message(f'''Member added. ✅''', ephemeral=True)
                embed3 = discord.Embed(title="**__Member Added__**", description=f'''{amember.mention} has been added to the ticket by {author.mention}''', color=embedColor)
                embed3.set_thumbnail(url=f'{amember.avatar}')
                embed3.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
                try:
                    await tchannel.send(embed=embed3)
                except discord.HTTPException:
                    await tchannel.send(f'{amember.mention} **has been added to the ticket by {author.mention}**')

class removeMemberModal(discord.ui.Modal, title="Remove a member"):
    answer = discord.ui.TextInput(label='Place Member ID here', style=discord.TextStyle.short, required=True, max_length=128)

    async def on_submit(self, interaction: discord.Interaction):
        tchannel = interaction.channel
        author = interaction.user
        guild = interaction.guild
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        ticketInfo = TicketData.find(cursor, tchannel.id)
        TicketData.close(connection)
        try:
            ltype = (ticketInfo[4])
        except IndexError:
            ltype = str("N/A")
        
        try:
            amember = discord.utils.get(guild.members, id=int(self.children[0].value))
        except Exception:
            amember = None
        if amember == None:
            embed = discord.Embed(description=f'''I couldn't find that member, are you sure that is a valid member id? This is what I got: {self.children[0].value}''', color=embedColor)
            embed.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            embed.set_author(name=f'{author}', icon_url=author.display_avatar)
            try:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except discord.HTTPException:
                await interaction.response.send_message(f'''I couldn't find that member, are you sure that is a valid member id? This is what I got: {self.children[0].value}''', ephemeral=True)
        elif amember != None:
            allowedAcess = False
            try:
                for allowedRoles in list(channelPerms[f"{ltype}"]):
                    prole = discord.utils.get(guild.roles, id=allowedRoles)
                    if prole in amember.roles:
                        allowedAcess = True
                    else:
                        pass
            except TypeError:
                prole = get(guild.roles, id=channelPerms[f"{ltype}"])
                if prole in author.roles:
                    allowedAcess = True
                else:
                    pass
            if (allowedAcess == True):
                embed2 = discord.Embed(description=f'''I can't remove that member!''', color=embedColor)
                embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
                embed2.set_author(name=f'{author}', icon_url=author.display_avatar)
                try:
                    await interaction.response.send_message(embed=embed2, ephemeral=True)
                except discord.HTTPException:
                    await interaction.response.send_message(f'''I can't remove that member!`''', ephemeral=True)
            else:
                await tchannel.set_permissions(amember, send_messages=False, read_messages=False)
                embed2 = discord.Embed(description=f'''Member removed. ✅''', color=embedColor)
                embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
                embed2.set_author(name=f'{author}', icon_url=author.display_avatar)
                try:
                    await interaction.response.send_message(embed=embed2, ephemeral=True)
                except discord.HTTPException:
                    await interaction.response.send_message(f'''Member removed. ✅''', ephemeral=True)

class renameChannelModal(discord.ui.Modal, title="Rename a Ticket Channel"):
    answer = discord.ui.TextInput(label='Place new name of ticket channel here', style=discord.TextStyle.short, required=True, max_length=32)
    async def on_submit(self, interaction: discord.Interaction):
        tchannel = interaction.channel
        author = interaction.user
        if f"{self.children[0].value}" == '':
            embed4 = discord.Embed(description=f'''You didn't provide a valid answer! Please try again. I got {self.children[0].value}''', color=embedColor)
            embed4.set_author(name=f'{author}', icon_url=author.display_avatar)
            embed4.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                await interaction.response.send_message(embed=embed4, ephemeral=True)
            except discord.HTTPException:
                await interaction.response.send_message(f'''You didn't provide a valid answer! Please try again. I got {self.children[0].value}''', ephemeral=True)
        else:
            embed2 = discord.Embed(description=f'Channel Renamed ✅', color=embedColor)
            embed2.set_author(name=f'{author}', icon_url=author.display_avatar)
            embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            await tchannel.edit(name=self.children[0].value)
            await interaction.response.send_message(embed=embed2, ephemeral=True)

    
class optionsMenu(discord.ui.View):
    @discord.ui.button(label="Принять тикет", emoji="🚩", style=discord.ButtonStyle.gray)
    async def claim(self, interaction:discord.Interaction, button: discord.Button):
        tchannel = interaction.channel
        author = interaction.user
        guild = interaction.guild
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        ticketInfo = TicketData.find(cursor, tchannel.id)
        syslogc = get(guild.channels, id=ticketLogsChannelID)
        if (ticketInfo[2]) != "No":
            embed1 = discord.Embed(description=f'This ticket has already been claimed!', color=embedColor)
            embed1.set_author(name=f'{author}', icon_url=author.display_avatar)
            embed1.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                await interaction.response.edit_message(embed=embed1, view=None)
            except discord.HTTPException:
                await interaction.response.edit_message(f"This ticket has already been claimed!", view=None)
        else:
            embed3 = discord.Embed(description=f'Тикет принят ✅', color=embedColor)
            embed3.set_author(name=f'{author}', icon_url=author.display_avatar)
            embed3.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                await interaction.response.edit_message(embed=embed3, view=None)
            except discord.HTTPException:
                await interaction.response.edit_message(f"Тикет принят ✅", view=None)
            
            embed2 = discord.Embed(title="**__Ticket Claimed__**", description=f'''{author.mention} принял тикет.''', color=embedColor)
            embed2.set_author(name=f'{author}', icon_url=author.display_avatar)
            embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                await tchannel.send(embed=embed2)
            except discord.HTTPException:
                await tchannel.send(f'''**__Ticket Claimed__**\n{author.mention} has claimed this ticket.''')
            TicketData.edit(connection, cursor, ticketInfo, author.id, ticketInfo[5])
            embed1 = discord.Embed(title='Ticket Claimed', description=f'{author.mention} has claimed ticket {tchannel.mention}', color=embedColor)
            embed1.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                message2 = await syslogc.send(embed=embed1)
            except discord.HTTPException:
                message2 = await syslogc.send(f"**{author.mention} has claimed ticket {tchannel.mention}**")
            else:
                pass
        TicketData.close(connection)

    @discord.ui.button(label="Добавить пользователя", emoji="👥", style=discord.ButtonStyle.green)
    async def addmember(self, interaction:discord.Interaction, button: discord.ui.button):
        await interaction.response.send_modal(addMemberModal())
        author = interaction.user
        embed2 = discord.Embed(description=f'Кнопку можно нажать только один раз!', color=embedColor)
        embed2.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
        embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')  
        await interaction.edit_original_response(embed=embed2, view=None)

    @discord.ui.button(label="Удалить пользователя", emoji="👋", style=discord.ButtonStyle.red)
    async def removemember(self, interaction:discord.Interaction, button: discord.ui.button):
        await interaction.response.send_modal(removeMemberModal())
        author = interaction.user
        embed2 = discord.Embed(description=f'Кнопку можно нажать только один раз!', color=embedColor)
        embed2.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
        embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')  
        await interaction.edit_original_response(embed=embed2, view=None)

    @discord.ui.button(label="Активный тикет", emoji="🟢", style=discord.ButtonStyle.blurple)
    async def activeticket(self, interaction:discord.Interaction, button: discord.ui.button):
        tchannel = interaction.channel
        author = interaction.user
        guild = interaction.guild
        syslogc = get(guild.channels, id=ticketLogsChannelID)
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        ticketInfo = TicketData.find(cursor, tchannel.id)
        categoryn = activeTicketsCategoryID
        if tchannel.category_id != categoryn:
            embed4 = discord.Embed(description=f'Setting Ticket to `Active` status...', color=embedColor)
            embed4.set_author(name=f'{author}', icon_url=author.display_avatar)
            embed4.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                message3 = await interaction.response.edit_message(embed=embed4, view=None)
            except discord.HTTPException:
                message3 = await interaction.response.edit_message(f"Setting Ticket to `Active` status...", view=None)
            category = discord.utils.get(guild.categories, id=categoryn)
            await tchannel.edit(category=category)
            TicketData.edit(connection, cursor, ticketInfo, ticketInfo[2], "Active")
            embed1 = discord.Embed(title='__**Ticket Status Changed**__', description=f'This ticket has been set to `Active` ✅', color=embedColor)
            embed1.set_author(name=f'{author}', icon_url=author.display_avatar)
            embed1.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                message3 = await tchannel.send(embed=embed1)
            except discord.HTTPException:
                message3 = await tchannel.send(f"**This ticket has been set to `Active` ✅**")
            embed2 = discord.Embed(title='Ticket set to Active', description=f'Ticket {tchannel.mention} has been set to `Active` by {author.mention}', color=embedColor)
            embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                await syslogc.send(embed=embed2)
            except discord.HTTPException:
                await syslogc.send(f"Ticket {tchannel.mention} has been set to `Active` by {author.mention}")   
        elif tchannel.category_id == categoryn:
            embed1 = discord.Embed(description=f'Этот тикет уже настроен на `Active`!', color=embedColor)
            embed1.set_author(name=f'{author}', icon_url=author.display_avatar)
            embed1.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                await interaction.response.edit_message(embed=embed1, view=None)
            except discord.HTTPException:
                await tchannel.send(f"Этот тикет уже настроен наo `Active`!")
        TicketData.close(connection)

    @discord.ui.button(label="Отложить тикет", emoji="✋", style=discord.ButtonStyle.blurple)
    async def onholdticket(self, interaction:discord.Interaction, button: discord.ui.button):
        tchannel = interaction.channel
        author = interaction.user
        guild = interaction.guild
        syslogc = get(guild.channels, id=ticketLogsChannelID)
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        ticketInfo = TicketData.find(cursor, tchannel.id)
        categoryn = onHoldTicketsCategoryID
        if tchannel.category_id != categoryn:
            embed4 = discord.Embed(description=f'Setting Ticket to `Onhold` status...', color=embedColor)
            embed4.set_author(name=f'{author}', icon_url=author.display_avatar)
            embed4.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                message3 = await interaction.response.edit_message(embed=embed4, view=None)
            except discord.HTTPException:
                message3 = await interaction.response.edit_message(f"Setting Ticket to `Onhold` status...", view=None)
            category = discord.utils.get(guild.categories, id=categoryn)
            await tchannel.edit(category=category)
            TicketData.edit(connection, cursor, ticketInfo, ticketInfo[2], "Onhold")
            embed1 = discord.Embed(title='__**Ticket Status Changed**__', description=f'Этот тикет уже настроен на `Onhold` ✅', color=embedColor)
            embed1.set_author(name=f'{author}', icon_url=author.display_avatar)
            embed1.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                message3 = await tchannel.send(embed=embed1)
            except discord.HTTPException:
                message3 = await tchannel.send(f"**Этот тикет уже настроен на `Onhold` ✅**")
            embed2 = discord.Embed(title='Ticket set to Onhold', description=f'Ticket {tchannel.mention} has been set to `Onhold` by {author.mention}', color=embedColor)
            embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                await syslogc.send(embed=embed2)
            except discord.HTTPException:
                await syslogc.send(f"Ticket {tchannel.mention} has been set to `Onhold` by {author.mention}")   
        elif tchannel.category_id == categoryn:
            embed1 = discord.Embed(description=f'Этот тикет уже настроен на `Onhold`!', color=embedColor)
            embed1.set_author(name=f'{author}', icon_url=author.display_avatar)
            embed1.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                await interaction.response.edit_message(embed=embed1, view=None)
            except discord.HTTPException:
                await tchannel.send(f"Этот тикет уже настроен на `Onhold`!")
        TicketData.close(connection)

    @discord.ui.button(label="Переименовать тикет", emoji="✏️", style=discord.ButtonStyle.gray)
    async def rename(self, interaction:discord.Interaction, button: discord.ui.button):
        await interaction.response.send_modal(renameChannelModal())
        author = interaction.user
        embed2 = discord.Embed(description=f'You can only select a button once!', color=embedColor)
        embed2.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
        embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')  
        await interaction.edit_original_response(embed=embed2, view=None)
        
    @discord.ui.button(label="Архивировать тикет", emoji="🗄️", style=discord.ButtonStyle.blurple)
    async def archive(self, interaction:discord.Interaction, button: discord.ui.button):
        author = interaction.user
        embed6 = discord.Embed(description="Вы уверены, что хотите заархивировать этот тикет? Это приведет к перемещению тикета в архивную категорию, и тикет-бот больше не будет управлять им.", color=embedColor)
        embed6.set_author(name=f'{author}', icon_url=author.display_avatar)
        embed6.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            await interaction.response.edit_message(embed=embed6, view=ticketArchiveyesOrNoOption(timeout=None))
        except discord.HTTPException:
            await interaction.response.edit_message(content="Здесь произошло что-то странное, попробуйте еще раз.")

    @discord.ui.button(label="Расшифровать билет", emoji="📝", style=discord.ButtonStyle.red)
    async def transcribe(self, interaction:discord.Interaction, button: discord.ui.button):
        author = interaction.user
        embed6 = discord.Embed(description="Вы действительно хотите закрыть тикет? Это приведет к удалению тикета.", color=embedColor)
        embed6.set_author(name=f'{author}', icon_url=author.display_avatar)
        embed6.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            await interaction.response.edit_message(embed=embed6, view=yesOrNoOption(timeout=None))
        except discord.HTTPException:
            await interaction.response.edit_message("Здесь произошло что-то странное, попробуйте еще раз.")


class yesOrNoOption(discord.ui.View):
    @discord.ui.button(label="Да", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        open('messages.txt', 'w').close()
        tchannel = interaction.channel

        messages = []
        async for message in tchannel.history(limit=None):
            messages.append(message)

        for message in messages:
            with open('messages.txt', 'a', encoding='utf-8') as file:
                file.write(f'{message.author.name}: {message.content}\n')


        lchannel = bot.get_channel(ticketTranscriptChannelID)
        author = interaction.user
        guild = interaction.guild
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        ticketInfo = TicketData.find(cursor, tchannel.id)
        syslogc = get(guild.channels, id=ticketLogsChannelID)
        embed4 = discord.Embed(description=f'Архивирование тикета...', color=embedColor)
        embed4.set_author(name=f'{author}', icon_url=author.display_avatar)
        embed4.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            await interaction.response.edit_message(embed=embed4, view=None)
        except discord.HTTPException:
            await interaction.response.edit_message(f"Архивирование тикета...", )
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        embed3 = discord.Embed(title=f'Тикет закрыт', description=f'{author.mention} закрыл тикет, канал будет удалён через 5 секунд', color=embedColor)
        embed3.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            await tchannel.send(embed=embed3)
        except discord.HTTPException:
            await tchannel.send(f"{author.mention} закрыл тикет, канал будет удалён через 5 секунд")
        await asyncio.sleep(2)

        embed2 = discord.Embed(title=f'Транскрипция тикета', description=f'{author.mention} закрыл открытый тикет, он был сохранен, зарегистрирован и удален.', color=embedColor)
        embed2.set_thumbnail(url="https://static-00.iconduck.com/assets.00/memo-emoji-1948x2048-bgnk0vsq.png")
        embed2.set_author(name=author, icon_url=author.display_avatar)
        embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        embed2.add_field(name='**__Название канала:__**', value=f'#{tchannel.name}', inline=True)
        embed2.add_field(name="**__Автор:__**", value=f"{author.mention}", inline=True)
        embed2.add_field(name="**__Тип:__**", value=f"{ticketInfo[4]}", inline=True)
        if dmTicketCopies == True:
            try:
                embed3 = discord.Embed(title="Копия тикета", description=f"Привет {author.mention}!\n Спасибо за создание тикета у нас. Прикреплен к этому сообщению копия вашего тикета для ваших записей.\n\nПожалуйста, обратите внимание, что любые медиафайлы, отправленные в вашем тикете, через некоторое время не будут загружаться в копию.\n \n ", color=embedColor)
                embed3.add_field(name="**__Ссылка для перехода/скачивания:__**", value=f"Ссылка удалена", inline=True)
                embed3.add_field(name="**__Ссылка для просмотра:__**", value=f"[Ссылка удалена]()", inline=True)
                embed3.set_thumbnail(url="https://static-00.iconduck.com/assets.00/memo-emoji-1948x2048-bgnk0vsq.png")
                try:
                    await author.send(embed=embed3)
                except discord.HTTPException:
                    await author.send(f"Привет {author.mention}!\n Спасибо за создание тикета у нас. Прикреплен к этому сообщению копия вашего тикета для ваших записей.\nПожалуйста, обратите внимание, что любые медиафайлы, отправленные в вашем тикете, через некоторое время не будут загружаться в копию.\n**__Ссылка для перехода/скачивания:__ССЫЛКА_УДАЛЕНА\n**__Ссылка для просмотра:__**[ССЫЛКА УДАЛЕНА]()")
                embed2.add_field(name="**__Статус копии:__**", value="Копия тикета успешно доставлена создателю тикета. ✅")
            except Exception:
                print("2")
                embed2.add_field(name="**__Статус копии:__**", value="Не удалось доставить копию создателю тикета. Скорее всего, это связано с тем, что у него выключены личные сообщения. ❌")
        else:
            pass
        embed2.add_field(name="**__Время создания:__**", value=f"{ticketInfo[3]}", inline=False)
        embed2.add_field(name="**__Ссылка для перехода/скачивания:__**", value=f"\n Ссылка удалена", inline=True)
        embed2.add_field(name="**__Ссылка для просмотра:__**", value=f"\n[ССЫЛКА УДАЛЕНА]()", inline=True)
        try:
            message3 = await syslogc.send(embed=embed2, file=discord.File("messages.txt"))
        except discord.HTTPException:
            message3 = await syslogc.send(f"Канал тикета **{tchannel.mention}** был закрыт пользователем {author.mention}, он был сохранен, зарегистрирован и удален.")

        await tchannel.delete()
        TicketData.delete(connection, cursor, tchannel.id)
        TicketData.close(connection)


    @discord.ui.button(label="Нет", style=discord.ButtonStyle.red)
    async def no(self, interaction:discord.Interaction, button: discord.ui.button):
        author = interaction.user
        embed4 = discord.Embed(description="Отмена...", color=embedColor)
        embed4.set_author(name=f'{author}', icon_url=author.display_avatar)
        embed4.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            await interaction.response.edit_message(embed=embed4, view=None)
        except discord.HTTPException:
            await interaction.response.edit_message("Отмена...", view=None)
class ticketArchiveyesOrNoOption(discord.ui.View):
    @discord.ui.button(label="Да", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.button):
        tchannel = interaction.channel
        author = interaction.user
        guild = interaction.guild
        syslogc = get(guild.channels, id=ticketLogsChannelID)
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        ticketInfo = TicketData.find(cursor, tchannel.id)
        categoryn = archivedTicketsCategoryID
        embed4 = discord.Embed(description=f'Устанавливаю статус тикета на `Архивирован`...', color=embedColor)
        embed4.set_author(name=f'{author}', icon_url=author.display_avatar)
        embed4.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            message3 = await interaction.response.edit_message(embed=embed4, view=None)
        except discord.HTTPException:
            message3 = await interaction.response.edit_message(f"Устанавливаю статус тикета на `Архивирован`...", view=None)
        category = discord.utils.get(guild.categories, id=categoryn)
        await tchannel.edit(category=category)
        TicketData.edit(connection, cursor, ticketInfo, ticketInfo[2], "Архивирован")
        embed1 = discord.Embed(title='__**Изменение статуса тикета**__', description=f'Этот тикет был установлен в статус `Архивирован` ✅', color=embedColor)
        embed1.set_author(name=f'{author}', icon_url=author.display_avatar)
        embed1.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            message3 = await tchannel.send(embed=embed1)
        except discord.HTTPException:
            message3 = await tchannel.send(f"**Этот тикет был установлен в статус `Архивирован` ✅**")
        embed2 = discord.Embed(title='Тикет установлен в статус "Архивирован"', description=f'Тикет {tchannel.mention} был установлен в статус `Архивирован` пользователем {author.mention}', color=embedColor)
        embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            await syslogc.send(embed=embed2, file=discord.File("messages.txt"))
        except discord.HTTPException:
            await syslogc.send(f"Тикет {tchannel.mention} был установлен в статус `Архивирован` пользователем {author.mention}")
        TicketData.delete(connection, cursor, tchannel.id)
        TicketData.close(connection)

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction:discord.Interaction, button: discord.ui.button):
        author = interaction.user
        embed4 = discord.Embed(description="Отмена...", color=embedColor)
        embed4.set_author(name=f'{author}', icon_url=author.display_avatar)
        embed4.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            await interaction.response.edit_message(embed=embed4, view=None)
        except discord.HTTPException:
            await interaction.response.edit_message("Отмена...", view=None)