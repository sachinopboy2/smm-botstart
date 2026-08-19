import requests, time, warnings
warnings.filterwarnings('ignore')

BASE = "Opanokebot"
U = 'https://core.smm.plus/api/free-service/order'

import time as _t
end_time = _t.time() + 200  # 3.5 min

total_ok = 0
at_count = 0

print(f"v3 start: {BASE}")

while _t.time() < end_time:
    at_str = "@" * at_count
    target = f"https://t.me/{at_str}{BASE}"

    H = {
        'Content-Type': 'application/json',
        'Origin': 'https://smm.plus',
        'Referer': 'https://smm.plus/free-telegram-botstart',
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{110+at_count}.0.0.0 Safari/537.36',
    }

    try:
        r = requests.post(U,
            json={'service': 'telegram_bot_start', 'link': target, 'quantity': 100},
            headers=H, verify=False, timeout=12)

        txt = r.text.strip() if r.text else ""

        if not txt:
            # Empty = IP rate limited, try next @ immediately
            print(f"EMPTY @{at_count} -> next @")
            at_count += 1
            if at_count > 80:
                at_count = 0
                time.sleep(3)
            continue

        try:
            d = r.json()
        except:
            print(f"PARSE_ERR @{at_count}: {txt[:50]} -> next @")
            at_count += 1
            if at_count > 80:
                at_count = 0
            time.sleep(0.3)
            continue

        if d.get('ok'):
            total_ok += 1
            oid = d.get('data', {}).get('order', '?')
            print(f"SUCCESS +100 total={total_ok*100} @{at_count} order={oid}")
            # After success, keep @ same first, then reset after cycle
            time.sleep(1)
        else:
            err = d.get('error', '')
            # ANY error/limit -> @ badhaao, koi wait nahi
            print(f"LIMIT @{at_count}: {err[:55]} -> next @")
            at_count += 1
            if at_count > 80:
                at_count = 0
                time.sleep(2)

    except Exception as e:
        print(f"ERR @{at_count}: {str(e)[:40]} -> next @")
        at_count += 1
        if at_count > 80:
            at_count = 0
        time.sleep(0.3)

print(f"DONE total={total_ok*100}")
