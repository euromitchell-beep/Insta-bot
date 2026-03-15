---

## 5️⃣ bot.py (Final Version: Bold + Flashy Welcome Text)

```python
from instagrapi import Client
import time, json, random
from datetime import datetime

# ====== Instagram Login ======
USERNAME = "YOUR_INSTAGRAM_USERNAME"
PASSWORD = "YOUR_INSTAGRAM_PASSWORD"
THREAD_ID = "YOUR_GROUP_THREAD_ID"

cl = Client()
cl.login(USERNAME, PASSWORD)

# ====== Config ======
try:
    with open("config.json","r") as f:
        config = json.load(f)
except:
    config = {
        "admins": [USERNAME],
        "welcomed_users": [],
        "daily_report": {},
        "welcome_messages": [
            "✨🔥 𝗛𝗬𝗬 @{name}! 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗧𝗛𝗜𝗦 𝗚𝗥𝗢𝗨𝗣 🔥✨\n💎 𝗕𝗢𝗧 𝗠𝗔𝗗𝗘 𝗕𝗬 𝗔𝗡𝗜𝗞 @b4n.nobita 💎\n⚡ 𝗟𝗘𝗧'𝗦 𝗥𝗢𝗖𝗞 𝗔𝗡𝗗 𝗛𝗔𝗩𝗘 𝗙𝗨𝗡! ⚡"
        ]
    }

def save_config():
    with open("config.json","w") as f:
        json.dump(config,f)

def send_msg(text):
    cl.direct_send(text, thread_ids=[THREAD_ID])

# Bold Unicode
def bold_text(text):
    bold_map = { 
        'A':'𝗔','B':'𝗕','C':'𝗖','D':'𝗗','E':'𝗘','F':'𝗙','G':'𝗚','H':'𝗛','I':'𝗜','J':'𝗝','K':'𝗞','L':'𝗟','M':'𝗠',
        'N':'𝗡','O':'𝗢','P':'𝗣','Q':'𝗤','R':'𝗥','S':'𝗦','T':'𝗧','U':'𝗨','V':'𝗩','W':'𝗪','X':'𝗫','Y':'𝗬','Z':'𝗭',
        'a':'𝗮','b':'𝗯','c':'𝗰','d':'𝗱','e':'𝗲','f':'𝗳','g':'𝗴','h':'𝗵','i':'𝗶','j':'𝗷','k':'𝗸','l':'𝗹','m':'𝗺',
        'n':'𝗻','o':'𝗼','p':'𝗽','q':'𝗾','r':'𝗿','s':'𝘀','t':'𝘁','u':'𝘂','v':'𝘃','w':'𝘄','x':'𝘅','y':'𝘆','z':'𝘇',
        '0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'
    }
    return ''.join(bold_map.get(c, c) for c in text)

# ====== Main Loop ======
while True:
    thread = cl.direct_thread(THREAD_ID)

    # Admin commands
    messages = cl.direct_messages(thread_id=THREAD_ID, amount=5)
    for msg in messages:
        if msg.user.username in config["admins"] and msg.text:
            text = msg.text
            if text.startswith("!setwelcome "):
                new_msg = text.replace("!setwelcome ","")
                if new_msg not in config["welcome_messages"]:
                    config["welcome_messages"].append(new_msg)
                    save_config()
                    send_msg("✅ New welcome message added!")
            elif text.startswith("!removewelcome "):
                rem_msg = text.replace("!removewelcome ","")
                if rem_msg in config["welcome_messages"]:
                    config["welcome_messages"].remove(rem_msg)
                    save_config()
                    send_msg("❌ Welcome message removed!")
            elif text.startswith("!addadmin "):
                new_admin = text.replace("!addadmin ","")
                if new_admin not in config["admins"]:
                    config["admins"].append(new_admin)
                    save_config()
                    send_msg(f"👑 {new_admin} added as admin!")
            elif text.startswith("!removeadmin "):
                rem_admin = text.replace("!removeadmin ","")
                if rem_admin in config["admins"] and rem_admin != USERNAME:
                    config["admins"].remove(rem_admin)
                    save_config()
                    send_msg(f"❌ {rem_admin} removed from admin!")

    # Welcome new members
    for user in thread.users:
        if user.pk not in config["welcomed_users"]:
            welcome_text = random.choice(config["welcome_messages"]).format(name=user.username)
            send_msg(bold_text(welcome_text))
            config["welcomed_users"].append(user.pk)
            today = datetime.now().strftime("%Y-%m-%d")
            config["daily_report"][today] = config["daily_report"].get(today,0)+1
            save_config()

    # Anti-leave alert
    current_user_ids = [u.pk for u in thread.users]
    left_users = [uid for uid in config["welcomed_users"] if uid not in current_user_ids]
    for uid in left_users:
        send_msg(f"⚠️ A member left the group!")
        config["welcomed_users"].remove(uid)
        save_config()

    time.sleep(15)
