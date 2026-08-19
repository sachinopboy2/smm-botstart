import requests, time, warnings
warnings.filterwarnings('ignore')

BASE = "Opanokebot"
U = 'https://core.smm.plus/api/free-service/order'
H = {
    'Content-Type': 'application/json',
    'Origin': 'https://smm.plus',
    'Referer': 'https://smm.plus/free-telegram-botstart',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
}

import time as _t
end_time = _t.time() + 340  # 5.5 min (GitHub timeout = 6min)

total_ok = 0
at_count = 0

print(f"START {BASE}")

while _t.time() < end_time:
    at_str = "@" * at_count
    target = f"https://t.me/{at_str}{BASE}"

    try:
        r = requests.post(U,
            json={'service': 'telegram_bot_start', 'link': target, 'quantity': 100},
            headers=H, verify=False, timeout=12)

        txt = r.text.strip() if r.text else ""

        # HTML / empty = IP blocked -> wait 3 min then retry
        if not txt or txt.startswith('<!') or txt.startswith('<h'):
            print(f"BLOCK @{at_count} -> wait 180s")
            time.sleep(180)
            at_count = 0  # reset after block wait
            continue

        try:
            d = r.json()
        except:
            print(f"PARSE @{at_count}: {txt[:30]} -> wait 3min")
            time.sleep(180)
            at_count = 0
            continue

        if d.get('ok'):
            total_ok += 1
            oid = d.get('data', {}).get('order', '?')
            print(f"SUCCESS +100 total={total_ok*100} @{at_count} order={oid}")
            # Success hone pe 3 min wait, phir fir try
            print(f"Waiting 180s before next order...")
            time.sleep(180)
            at_count = 0  # reset @ after success

        else:
            err = d.get('error', '')
            # ANY limit/error -> @ badhaao, NO WAIT, turant retry
            print(f"LIMIT @{at_count}: {err[:55]} -> next @")
            at_count += 1
            if at_count > 50:
                at_count = 0
                time.sleep(5)

    except Exception as e:
        print(f"ERR @{at_count}: {str(e)[:40]}")
        time.sleep(3)

print(f"DONE total={total_ok*100}")
