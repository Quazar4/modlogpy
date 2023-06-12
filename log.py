import discord
from discord.ext import commands
import psycopg2

bot = commands.Bot(command_prefix="%")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

    conn = psycopg2.connect(
        database="modlog_db",
        user="your_username",
        password="your_password",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS modlogs (
            id SERIAL PRIMARY KEY,
            guild_id BIGINT NOT NULL,
            user_id BIGINT NOT NULL,
            moderator_id BIGINT NOT NULL,
            action TEXT NOT NULL,
            reason TEXT,
            timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
        """
    )
    conn.commit()
    cursor.close()

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    # Perform the kick action
    await member.kick(reason=reason)
    
    conn = psycopg2.connect(
        database="modlog_db",
        user="your_username",
        password="your_password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO modlogs (guild_id, user_id, moderator_id, action, reason) VALUES (%s, %s, %s, %s, %s)",
        (ctx.guild.id, member.id, ctx.author.id, "kick", reason)
    )
    conn.commit()
    cursor.close()

    await ctx.send(f"{member.mention} has been kicked.")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    
    await member.ban(reason=reason)
    
    conn = psycopg2.connect(
        database="modlog_db",
        user="name",
        password="your_password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO modlogs (guild_id, user_id, moderator_id, action, reason) VALUES (%s, %s, %s, %s, %s)",
        (ctx.guild.id, member.id, ctx.author.id, "ban", reason)
    )
    conn.commit()
    cursor.close()

    await ctx.send(f"{member.mention} has been banned.")

bot.run("token")
