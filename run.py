import requests, sys, warnings, time
warnings.filterwarnings('ignore')

at_count = int(sys.argv[1]) if len(sys.argv) > 1 else 0
BASE = "Opanokebot"
at_str = "@" * at_count
target = f"https://t.me/{at_str}{BASE}"

U = 'https://core.smm.plus/api/free-service/order'
H = {
    'Content-Type': 'application/json',
    'Origin': 'https://smm.plus',
    'Referer': 'https://smm.plus/free-telegram-botstart',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
}

print(f"Trying @{at_count} -> {target}")

for attempt in range(3):
    try:
        r = requests.post(U,
            json={'service': 'telegram_bot_start', 'link': target, 'quantity': 100},
            headers=H, verify=False, timeout=12)
        
        txt = r.text.strip() if r.text else ""
        if not txt or txt.startswith('<!'):
            print(f"BLOCKED attempt {attempt+1}")
            time.sleep(5)
            continue
        
        d = r.json()
        if d.get('ok'):
            oid = d.get('data', {}).get('order', '?')
            print(f"SUCCESS order={oid} target={target}")
            sys.exit(0)
        else:
            err = d.get('error', '')
            print(f"LIMIT: {err[:60]}")
            # Limit matlab is @ pe nahi hoga, exit with code 1
            sys.exit(1)
    except Exception as e:
        print(f"ERR: {e}")
        time.sleep(3)

sys.exit(1)
