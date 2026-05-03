import asyncio
import requests
from playwright.async_api import async_playwright

BOT_TOKEN = "8754403140:AAGQZRdpdQfHHQBKYVJ79S70xU3wfFt4b-8"
CHAT_ID = "1235955153"
URL = "https://tazkarti.com/#/matches"
CHECK_INTERVAL = 60

previous_matches = set()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    })

async def check_matches():
    global previous_matches
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL, wait_until="networkidle")
        await page.wait_for_timeout(5000)

        elements = await page.query_selector_all(".one-block")

        current_matches = set()

        for el in elements:
            text = await el.inner_text()
            current_matches.add(text.strip())

        print(f"عدد المباريات: {len(current_matches)}")

        if not previous_matches:
            previous_matches = current_matches
            send_telegram(f"✅ البوت شغال\nعدد المباريات الحالي: {len(current_matches)}")
        else:
            new_matches = current_matches - previous_matches
            for match in new_matches:
                send_telegram(
                    f"🔥 <b>ماتش جديد نزل!</b>\n\n{match}\n\n"
                    f"احجز: https://tazkarti.com/#/matches"
                )
            previous_matches = current_matches

        await browser.close()

async def main():
    while True:
        try:
            await check_matches()
        except Exception as e:
            print("Error:", e)
        await asyncio.sleep(CHECK_INTERVAL)

asyncio.run(main())
