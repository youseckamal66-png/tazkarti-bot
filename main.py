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

        elements = await page.query_selector_all(".one-block
