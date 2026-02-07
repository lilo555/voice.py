intents = discord.Intents.default()
intents.members = True          # هادي هي اللي شعلتي دابا
intents.message_content = True  # وهادي حتى هي
intents.voice_states = True     # هادي هي الساروت ديال الـ Temp Voice

bot = commands.Bot(command_prefix='.', intents=intents)

class TempVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_data = {} # هنا كيتخزن شكون مول الروم

    # --- Setup Commands (Slash) ---
    @app_commands.command(name="set-lobby", description="حدد الروم اللي غاتصاوب الفويس")
    async def set_lobby(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        # هنا خاصك تحفظ الـ ID فـ Database (للمثال غانديرو متغير)
        await interaction.response.send_message(f"✅ تم تحديد {channel.mention} كلوبي.")

    # --- Voice Management (Prefix .v) ---
    @commands.group(name="v")
    async def v_group(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("❓ استعمل `.v help` باش تشوف الأوامر.")

    @v_group.command(name="lock")
    async def lock(self, ctx):
        """🔒 سد الروم"""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.set_permissions(ctx.guild.default_role, connect=False)
            await ctx.send("🔒 الروم دابا مسدودة!")

    @v_group.command(name="unlock")
    async def unlock(self, ctx):
        """🔓 حل الروم"""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.set_permissions(ctx.guild.default_role, connect=True)
            await ctx.send("🔓 الروم دابا محلولة!")

    @v_group.command(name="name")
    async def name(self, ctx, *, new_name: str):
        """📝 تبديل سمية الروم"""
        if ctx.author.voice:
            await ctx.author.voice.channel.edit(name=new_name)
            await ctx.send(f"✅ تبدلت السمية لـ: {new_name}")

    @v_group.command(name="limit")
    async def limit(self, ctx, count: int):
        """👥 تحديد عدد الداخلين"""
        if ctx.author.voice:
            await ctx.author.voice.channel.edit(user_limit=count)
            await ctx.send(f"👥 تم تحديد العدد فـ {count}")

    # --- Events: صاوب الروم فاش يدخل بنادم ---
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        lobby_id = 123456789 # الـ ID ديال Lobby اللي حددتي
        
        if after.channel and after.channel.id == lobby_id:
            guild = member.guild
            category = after.channel.category
            new_channel = await guild.create_voice_channel(
                name=f"🎙️ {member.display_name}'s Room",
                category=category
            )
            await member.move_to(new_channel)
            # صاوب الأزرار هنا (المرحلة الجاية)
            await self.send_control_panel(new_channel, member)

    async def send_control_panel(self, channel, owner):
        # هادي هي اللي غاتصاوب الـ Embed اللي فالتصويرة
        embed = discord.Embed(title="🎙️ Voice Control Panel", color=discord.Color.blue())
        embed.description = f"مرحبا بك {owner.mention} فالفويس ديالك!"
        # إضافة الأزرار (Buttons)
        view = VoiceButtons()
        await channel.send(embed=embed, view=view)

# كلاس الأزرار (Buttons)
class VoiceButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Lock", emoji="🔒", style=discord.ButtonStyle.grey)
    async def lock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # الكود ديال السدان هنا
        await interaction.response.send_message("🔒 سديتي الروم!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TempVoice(bot))
import os
bot.run(os.getenv('TOKEN_2'))
