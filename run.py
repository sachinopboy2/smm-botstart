import requests, time, warnings
warnings.filterwarnings('ignore')

BASE = "Opanokebot"
U = 'https://core.smm.plus/api/free-service/order'
H = {
    'Content-Type': 'application/json',
    'Origin': 'https://smm.plus',
    'Referer': 'https://smm.plus/free-telegram-botstart',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
}

total_ok = 0
at_count = 0  # current @ prefix count
MAX_AT = 50   # max @ to try

import time as _t
end_time = _t.time() + 200  # run for ~3.5 minutes (GitHub timeout is 4 min)

print(f"Starting @ escalation loop for {BASE}")

while _t.time() < end_time:
    target = "https://t.me/" + ("@" * at_count) + BASE
    try:
        r = requests.post(U,
            json={'service': 'telegram_bot_start', 'link': target, 'quantity': 100},
            headers=H, verify=False, timeout=15)
        d = r.json()

        if d.get('ok'):
            total_ok += 1
            order_id = d.get('data', {}).get('order', '?')
            print(f"[OK] +100 | total={total_ok*100} | target={target} | order={order_id}")
            # Success! Reset @ count back to 0 and try fresh
            at_count = 0
            time.sleep(1)

        else:
            err = d.get('error', '')
            print(f"[LIMIT] at={at_count} @ | {err[:60]} -> escalating @")
            # Limit hit -> badhaao @, wait bilkul nahi
            at_count += 1
            if at_count > MAX_AT:
                print(f"[RESET] Reached max {MAX_AT}@, resetting to 0")
                at_count = 0
                time.sleep(2)

    except Exception as e:
        print(f"[ERR] {e}")
        time.sleep(2)

print(f"\n[DONE] Total placed: {total_ok * 100} botstart for {BASE}")
