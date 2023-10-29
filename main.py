import tls_client, random, time, os, sys
from itertools import cycle
from concurrent.futures import ThreadPoolExecutor
import aiohttp, asyncio, requests
from dhooks import Webhook
os.system("clear")

vanity = cycle(["vanity1", "vanity2", "vanity3"´])
threads = 50
delay = 0.5
tkn = ""
guild = ""
hook_url = ""
hook = Webhook(hook_url)
claimed = False

def get_origin():
  return random.choice(["discord", "canary.discord", "ptb.discord", "discordapp"])

api_ = cycle([6,7,8,9,10])
def get_api():
  return next(api_)

def get_headers(token, origin):
  return {"Authorization": token}

attempt = 0 
async def fetch(headers, url):
  if claimed: 
    return 
  async with aiohttp.ClientSession(headers=headers) as session:
   async with session.get(url) as r:
     return r.status, await r.json() 

def notify(text):
  hook.send(text)
  #session = tls_client.Session(client_identifier="chrome_110")
  #r = session.post(hook_url, json={"content": text})
  #print(r.status_code)
  #print(r.text)
  
async def claim(code):
  global claimed
  if claimed: 
    return
  claimed = True
  print(code)
  time1 = time.time()
  #session = aiosonic.HTTPClient()
  headers = {"Authorization": tkn, "X-Audit-Log-Reason": "slapped by exploit | sniper v6"}   
  url = "https://canary.discord.com/api/v9/guilds/%s/vanity-url" % (guild)
  data = {"code": code}
  async with aiohttp.ClientSession(headers=headers) as session:
   async with session.patch(url, json=data) as r:
      print(r.text)
      time2 = time.time()
      time_taken = time2 - time1
      print(time_taken, r.status)
      claimed = True
      if r.status in (200, 201, 204):
        
        notify("@everyone claimed %s" % code)
        sys.exit()
      else:
        print(await r.json())
        notify("ok")
        notify(f"@everyone failed to claim; {code}, status; {r.status}, text; {await r.json()}")

def request_handler():
    if claimed:
      return
    global attempt
    vanity_code = next(vanity)
    origin = get_origin()
    headers = get_headers(tkn, origin)
    # session = tls_client.Session(client_identifier="chrome_110")
    # session.headers.update(headers)
    # r = session.get(url) 
    url = "https://%s.com/api/v%s/invites/%s?with_counts=true&with_expiration=true" % (origin, get_api(), vanity_code)
    status, text = asyncio.run(fetch(headers, url))
    if status in (200, 201, 204):
        attempt += 1
        sys.stdout.write('\r~ Request Count: %d | Vanity: %s' % (attempt, vanity_code))
          # sys.stdout.write('\n\033[F')
        sys.stdout.flush()
    else:
      # print(status, str(text))
      if status == 429:
        if 'retry_after' in str(text):
          print("rate limited, sleeping for :", text['retry_after'])
          time.sleep(int(text['retry_after']))
        else:
          os.system("kill 1")
      elif status == 404:
        asyncio.run(claim(vanity_code))
        sys.exit()

def main():
  origin = get_origin()
  headers = get_headers(tkn, origin)
  session = tls_client.Session(client_identifier="chrome_110")
  session.headers.update(headers)
  r = session.get("https://discord.com/api/v9/users/@me")
  if r.status_code in (200, 201, 204):
    print("logged in as: %s" % (r.json()['username']))
    notify("connected; %s" % (r.json()['username']))
  elif r.status_code == 429:
    print("[-] Rate Limited")
    os.system("kill 1")
  else:
    print("invalid token")
    hook.send("@everyone failed to connect to discord websocket")
    sys.exit()
  with ThreadPoolExecutor(max_workers=threads) as executer:
    for x in range(999991):
      time.sleep(delay)
      executer.submit(request_handler)

if __name__ == "__main__":
  main()

