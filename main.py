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

progress = False

token = {}
allow = []

captcha_numb = 0

@client.event
async def on_member_join(member):
    global captcha_numb
    await member.send(member.mention)
    embed = discord.Embed(title="🔰 𝙂𝙐𝘼𝙍𝘿𝙄𝘼𝙉 𝘾𝙄𝙏𝙔 𝙍𝙋  [𝙍𝙅]", color=discord.Color.purple())
    embed.set_thumbnail(url=member.avatar_url)

    captcha_text = random_text(1)

    image.generate(captcha_text)
    captcha_numb += 1
    image.write(captcha_text, f'captcha_{str(captcha_text)}.png')

    file = discord.File(f"captcha_{str(captcha_text)}.png", filename=f"captcha_{str(captcha_text)}.png")
    embed.add_field(name='INSIRA O CAPTCHA PARA CONCLUIR A VERIFICAÇÃO (8 DIGITOS)',
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
            await message.channel.send('```css\n+ AUTENTICADO COM SUCESSO```')

            token[message.author.id][3] = False
            guild_id = token[message.author.id][1]
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
            if guild_id == 579156532617543691:
                role = discord.utils.find(lambda r: r.id == 579166180418519040, guild.roles)
            else:
                role = discord.utils.find(lambda r: r.id == 651482636438732801, guild.roles)

            member = token[message.author.id][2]

            del token[message.author.id]

            await member.add_roles(role)
        else:
            await message.channel.send('```diff\n- VALOR INSERIDO É DIFERENTE DO CAPTCHA\n```')

client.run('NzU1ODQ2NTc3MDYyNTQzMzkw.X2JO-g.7VdQn5_2_6tKcz_cuUp1h9f98Gc')
