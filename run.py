import requests, time, warnings
warnings.filterwarnings('ignore')

BASE = "Opanokebot"
U = 'https://core.smm.plus/api/free-service/order'

import time as _t
end_time = _t.time() + 200

total_ok = 0
at_count = 0

print(f"FINAL start {BASE}")

while _t.time() < end_time:
    at_str = "@" * at_count
    target = f"https://t.me/{at_str}{BASE}"
    H = {
        'Content-Type': 'application/json',
        'Origin': 'https://smm.plus',
        'Referer': 'https://smm.plus/free-telegram-botstart',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    }
    try:
        r = requests.post(U,
            json={'service': 'telegram_bot_start', 'link': target, 'quantity': 100},
            headers=H, verify=False, timeout=12)

        txt = r.text.strip() if r.text else ""

        # HTML response = IP blocked -> wait and retry same @
        if txt.startswith('<!') or txt.startswith('<h') or not txt:
            print(f"IP_BLOCK @{at_count} -> wait 15s")
            time.sleep(15)
            continue  # retry same at_count after wait

        try:
            d = r.json()
        except:
            print(f"PARSE @{at_count}: {txt[:30]} -> wait 5s")
            time.sleep(5)
            continue

        if d.get('ok'):
            total_ok += 1
            oid = d.get('data', {}).get('order', '?')
            print(f"SUCCESS +100 total={total_ok*100} @{at_count} order={oid}")
            at_count = 0  # reset after success, try from scratch
            time.sleep(1)
        else:
            err = d.get('error', '')
            # Rate limit on this target -> try next @
            print(f"LIMIT @{at_count}: {err[:50]} -> next @")
            at_count += 1
            if at_count > 50:
                at_count = 0
                time.sleep(5)

    except Exception as e:
        print(f"ERR @{at_count}: {str(e)[:40]}")
        time.sleep(3)

print(f"DONE total={total_ok*100}")
