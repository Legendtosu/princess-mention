import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID", "9181844"))
api_hash = os.environ.get("API_HASH", "996a3e7194a4f07576fda5c20bb1138b")
bot_token = os.environ.get("TOKEN", "5853405036:AAHay06CtbbUmRhCguwgflpMLxiLWgp5vts")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "__**ι'м   мєηтιση вσт** ¢αη мєηтιση αℓмσѕт αℓℓ мємвєяѕ ιη gяσυρ σя ¢нαηηєℓ 👻\nClick **/help** for more information__\n\n Owner [@Alone_programmare]",
    link_preview=False,
    buttons=(
      [
        Button.url('♛ σωηєя', 'https://t.me/your_godfather_xd'),
        Button.url('✪ ɠɾσυρ', 'https://t.me/incricible')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**нєℓρ мєηυ σƒ мєηтισηαℓℓвσт**\n\nCommand: @all \n__уσυ ¢αη υѕє тнιѕ ¢σммαη∂ ωιтн тєχт ωнαт уσυ ωαηт тσ мєηтιση σтнєяѕ.__\n`єχαмρℓє: @all gσσ∂ мσяηιηg!`\n__уσυ ¢αη уσυ тнιѕ ¢σммαη∂ αѕ α яєρℓу тσ αηу мєѕѕαgє. . вσт ωιℓℓ тαg υѕєяѕ тσ тнαт яєρℓιє∂ мєѕѕѕαgє__.\n\n σωηєя [@Alone_programmare]"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('♛ σωηєя', 'https://t.me/your_godfather_xd'),
        Button.url('✪ ɠɾσυρ', 'https://t.me/incricoble')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^@all ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__This command can be use in groups and channels!__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__σηℓу α∂мιηѕ ¢αη мєηтιση αℓℓ мємвєяѕ!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Give me one argument!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__I can't mention members for older messages! (messages which are sent before I'm added to group)__")
  else:
    return await event.respond("__Reply to a message or give me some text to mention others!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 1:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__тнєяє ιѕ ησ ρяσ¢¢єѕѕ ση gσιηg...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Stopped.__')

print(">> вσтѕ ѕтαятє∂ <<")
client.run_until_disconnected()
