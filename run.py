import requests,time,warnings,sys
warnings.filterwarnings('ignore')
T = sys.argv[1]
U = 'https://core.smm.plus/api/free-service/order'
H = {'Content-Type':'application/json','Origin':'https://smm.plus','Referer':'https://smm.plus/free-telegram-botstart'}
ok = 0
for i in range(5):
    try:
        r = requests.post(U, json={'service':'telegram_bot_start','link':T,'quantity':100}, headers=H, verify=False, timeout=15)
        d = r.json()
        if d.get('ok'):
            ok += 1
            print(f'OK {ok*100} botstart for {T}')
        else:
            rt = int(d.get('retry_after_seconds', 120))
            print(f'Wait {rt}s | {d.get("error","")[:40]}')
            time.sleep(min(rt, 120))
    except Exception as e:
        print(f'ERR: {e}')
    time.sleep(3)
print(f'Done: +{ok*100} for {T}')
