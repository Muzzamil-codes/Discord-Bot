import os
from Image_module import Image_maker
import requests
import json
import discord
from discord.ext import commands
import random 
from bot_token import token as tk


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix="DuDe ", intents=intents)


@client.event
async def on_ready():
    print(f"{client.user.name} is ready.")


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = "\"" + json_data[0]['q'] + "\"" + ' -' + json_data[0]["a"]
    return(quote)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        username = message.author
        await message.channel.send(f"{username.mention} My prefix is DuDe.")

    await client.process_commands(message)

"-------------------------------------------------------Normal commands--------------------------------------------------"

@client.command()
async def server(ctx, a: str):
    if a == "count":
        await ctx.send("yeah DuDe I'm in " + str(len(client.guilds)) + " servers!")

# Remove the existing help command
client.remove_command('help')

# Redefine the help command
@client.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        title="Help: Command List",
        description="Here's a list of commands you can use with this bot. Use them with the prefix `DuDe`.",
        color=0x8c75ff
    )
    
    embed.set_author(name="MKMisnotCOOL#2550")
    
    # Comedy Commands
    embed.add_field(
        name="Comedy Commands",
        value=(
            "`kill <user>`: Shoot a user (fictionally) with humor.\n"
            "`dumbest <user>`: Find out the 'dumbest' person.\n"
            "`shit <user>`: Generate a funny image with the user's name."
        ),
        inline=False
    )
    
    # Inspirational Quotes
    embed.add_field(
        name="Inspirational Quotes",
        value="`inspire`: Receive a random inspirational quote.",
        inline=False
    )
    
    # Tic-Tac-Toe Game
    embed.add_field(
        name="Tic-Tac-Toe Game",
        value=(
            "`tictactoe <user>`: Start a Tic-Tac-Toe game with another user.\n"
            "`place <position>`: Place your mark on the Tic-Tac-Toe board at a position (1-9)."
        ),
        inline=False
    )
    
    # Mathematical Operations
    embed.add_field(
        name="Mathematical Commands",
        value=(
            "`add <a> <b>`: Add two numbers.\n"
            "`multiply <a> <b>`: Multiply two numbers.\n"
            "`subtract <a> <b>`: Subtract one number from another.\n"
            "`divide <a> <b>`: Divide one number by another."
        ),
        inline=False
    )
    
    # General Fun Commands
    embed.add_field(
        name="Fun Commands",
        value=(
            "`hello`: Say hello to the bot.\n"
            "`creator`: Learn about the bot's creator.\n"
            "`server count`: Find out how many servers the bot is in."
        ),
        inline=False
    )

    embed.set_footer(text="Enjoy using the bot! More commands coming soon.")
    
    await ctx.send(embed=embed)


"-----------------------------------------------------------TicTacToe Game------------------------------------------------------"
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = ctx.author
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")


@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1
                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Bruh you trying to oversmart me!? You can only use numbers from 1 to 9!")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the DuDe tictactoe command.")



def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]  ] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")
        
"-----------------------------------------------------------Mathematic operation commands----------------------------------------------"

@client.command()
async def add(ctx, a: int, b: int):
    final_value = a + b
    await ctx.send(str(final_value))


@client.command()
async def multiply(ctx, a: int, b: int):
    final_value = a * b
    await ctx.send(str(final_value))


@client.command()
async def substract(ctx, a: int, b: int):
    final_value = a - b
    await ctx.send(str(final_value))


@client.command()
async def divide(ctx, a: int, b: int):
    final_value = a / b
    await ctx.send(str(final_value))

"-----------------------------------------------------------------Play around commands--------------------------------------------------------"

@client.command()
async def hello(ctx):
    await ctx.send("hello i am the ultimate bot")


@client.command()
async def creator(ctx):
    await ctx.send("Yah I have been created by an amazing superlavtive highly talented programmer known as Muzzamil lOl")


@client.command()
async def inspire(ctx):
    quote = get_quote()
    await ctx.send(quote)


@client.command()
async def dumbest(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send(f"Fine you are dumb.")
    elif random.randint(0, 100) <= 30:
        await ctx.send(f"Hey what do you mean you are the dumbest person! Yes you heard me right {ctx.author.mention} is the Dumbest person")
        with open('rickroll-dance.gif', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
        await ctx.send("GET RICKROOLED!!!!!!!!")
    else:
        dumb_person = f"{member.mention}"
        await ctx.send(f"{dumb_person} is the dumbest person on the planet earth")


@client.command()
async def kill(ctx, member: discord.Member):
    if member == client.user:
        await ctx.send(f"{ctx.author.mention} was shot by Narendra Modi")
    else:
        kill_sentence = f"{member.mention} was shot by Narendra Modi"
        await ctx.send(kill_sentence)
    with open('pm.jpg', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

@client.command()
async def shit(ctx, member: discord.Member):
    g_member = str(member)
    g_member = g_member
    Image_maker(g_member)
    with open("created_image.png", 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)
    os.remove("created_image.png")

client.run(tk)
