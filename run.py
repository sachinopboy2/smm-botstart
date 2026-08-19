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
end_time = _t.time() + 340  # 5.5 min

total_ok = 0
print(f"START {BASE}")

while _t.time() < end_time:
    # Inner loop: @ 0 se 30 tak try karo, jab tak success na ho
    success = False
    for at_count in range(31):  # 0 to 30
        if _t.time() >= end_time:
            break
        at_str = "@" * at_count
        target = f"https://t.me/{at_str}{BASE}"
        try:
            r = requests.post(U,
                json={'service': 'telegram_bot_start', 'link': target, 'quantity': 100},
                headers=H, verify=False, timeout=12)
            txt = r.text.strip() if r.text else ""

            # HTML/empty = IP blocked
            if not txt or txt.startswith('<!') or txt.startswith('<h'):
                print(f"BLOCK @{at_count} -> skip")
                continue

            try:
                d = r.json()
            except:
                print(f"PARSE @{at_count}: {txt[:30]}")
                continue

            if d.get('ok'):
                total_ok += 1
                oid = d.get('data', {}).get('order', '?')
                print(f"SUCCESS +100 total={total_ok*100} @{at_count} order={oid}")
                success = True
                break  # success mila, inner loop se bahar
            else:
                err = d.get('error', '')
                print(f"LIMIT @{at_count}: {err[:50]} -> next @")
                # No wait, turant next @

        except Exception as e:
            print(f"ERR @{at_count}: {str(e)[:40]}")

    if success:
        # Success ke baad 3 min wait, phir dobara try
        print(f"Waiting 180s...")
        time.sleep(180)
    else:
        # Sab 30 @ try kar liye, koi success nahi -> 30s wait phir fir se
        print(f"All 30@ failed, wait 30s retry")
        time.sleep(30)

print(f"DONE total={total_ok*100}")
