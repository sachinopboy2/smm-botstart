import requests,time,warnings,sys
warnings.filterwarnings('ignore')

BASE = "Opanokebot"
U = 'https://core.smm.plus/api/free-service/order'
H = {
    'Content-Type':'application/json',
    'Origin':'https://smm.plus',
    'Referer':'https://smm.plus/free-telegram-botstart',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
}

total_ok = 0
# Try with increasing @ prefix: Opanokebot, @Opanokebot, @@Opanokebot, ... up to @@@@@@Opanokebot
variants = [
    f"https://t.me/{('@'*i)+BASE}" for i in range(0, 8)
]

print(f"Starting smart @ retry loop. {len(variants)} variants to try.")

for attempt in range(20):  # run for ~20 attempts total
    for variant in variants:
        try:
            r = requests.post(U,
                json={'service':'telegram_bot_start','link':variant,'quantity':100},
                headers=H, verify=False, timeout=15)
            d = r.json()
            if d.get('ok'):
                total_ok += 1
                print(f"SUCCESS [{total_ok*100} total] target={variant} order={d.get('data',{}).get('order','?')}")
                time.sleep(2)
            else:
                err = d.get('error','')
                retry_after = int(d.get('retry_after_seconds', 120))
                print(f"LIMIT [{variant}] wait={retry_after}s err={err[:50]}")
                # Don't wait, try next variant immediately
                time.sleep(1)
        except Exception as e:
            print(f"ERR [{variant}]: {e}")
            time.sleep(2)
    
    print(f"--- Round {attempt+1} done. Total placed: {total_ok*100} ---")
    time.sleep(5)

print(f"FINAL: +{total_ok*100} botstart placed for {BASE}")
