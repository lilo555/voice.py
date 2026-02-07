import discord
from discord.ext import commands
import os

# السوارت اللي شعلتي فـ Discord Portal
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='.v ', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} is online (Temp Voice Bot)')

# --- نظام الـ Temp Voice ---
@bot.event
async def on_voice_state_update(member, before, after):
    # حط هنا الـ ID ديال الروم "Join to Create"
    LOBBY_ID = 1234567890  # بدلو بالـ ID ديالك

    if after.channel and after.channel.id == LOBBY_ID:
        guild = member.guild
        category = after.channel.category
        
        # إنشاء الروم الجديدة
        new_channel = await guild.create_voice_channel(
            name=f"🎙️ {member.display_name}",
            category=category
        )
        
        # نقل العضو
        await member.move_to(new_channel)
        
        # صلاحيات المالك
        await new_channel.set_permissions(member, manage_channels=True, connect=True)

# --- أوامر التحكم .v ---
@bot.command(name="lock")
async def lock(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.set_permissions(ctx.guild.default_role, connect=False)
        await ctx.send("🔒 الروم دابا مسدودة!")

@bot.command(name="name")
async def rename(ctx, *, name):
    if ctx.author.voice:
        await ctx.author.voice.channel.edit(name=name)
        await ctx.send(f"✅ تبدلت السمية لـ: {name}")

# تشغيل البوت بالتوكن الثاني من Railway Variables
bot.run(os.getenv('TOKEN_2'))
