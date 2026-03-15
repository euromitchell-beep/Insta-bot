from instagrapi import Client

USERNAME = "castingyounow9"
PASSWORD = "akki7860"

cl = Client()
cl.login(USERNAME, PASSWORD)

# Get recent 20 threads
threads = cl.direct_threads(amount=20)
for t in threads:
    print(t.id, t.thread_title)
