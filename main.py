import discord, random, string
from captcha.image import ImageCaptcha
import os


def random_text(type):
    if type == 0:
        return ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
    else:
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))


image = ImageCaptcha(fonts=['font/arial.ttf'])

client = discord.Client()

role_id = #INSERT THE ROLE ID HERE for ex. 651482636438732801

token = {}
allow = []

captcha_numb = 0

@client.event
async def on_member_join(member):
    global captcha_numb
    await member.send(member.mention)
    embed = discord.Embed(title="DISCORD CAPTCHA - STOP ALL BOTS", color=discord.Color.purple())
    embed.set_thumbnail(url=member.avatar_url)

    captcha_text = random_text(1)

    image.generate(captcha_text)
    captcha_numb += 1
    image.write(captcha_text, f'captcha_{str(captcha_text)}.png')

    file = discord.File(f"captcha_{str(captcha_text)}.png", filename=f"captcha_{str(captcha_text)}.png")
    embed.add_field(name='INSERT CAPTCHA TO COMPLETE VERIFICATION (8 DIGITS)',
                    value='.............................................................................................................',
                    inline=False)
    embed.set_image(url=f"attachment://captcha_{str(captcha_text)}.png")

    token.update({member.id: [captcha_text, member.guild.id, member, True]})

    print(token)

    await member.send(content=None, file=file, embed=embed)

    os.remove(f'captcha_{str(captcha_text)}.png')

@client.event
async def on_message(message):

    if len(message.content) == 8 and token[message.author.id][3] and message.guild is None:
        if str(token[message.author.id][0]) == str(message.content).upper():
            await message.channel.send('```css\n+ SUCCESSFULLY AUTHENTICATED```')
            
            guild_id = token[message.author.id][1]
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
            role = discord.utils.find(lambda r: r.id == role_id, guild.roles)

            member = token[message.author.id][2]

            await member.add_roles(role)
            
            del token[message.author.id]
        else:
            await message.channel.send('```diff\n- VALUE INSERTED IS DIFFERENT FROM CAPTCHA\n```')

client.run('TOKEN')
