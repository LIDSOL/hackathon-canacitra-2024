import asyncio
from playwright.async_api import async_playwright

async def fetch_recent_tweets(username):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Navega a la página de Twitter del usuario
        await page.goto(f'https://twitter.com/{username}')
        
        # Espera que los tweets se carguen
        await page.wait_for_selector('article')
        
        # Extrae el contenido de los tweets
        tweets = await page.evaluate('''
            () => {
                const tweet_elements = document.querySelectorAll('article div[lang]');
                const tweets = [];
                tweet_elements.forEach(tweet => tweets.push(tweet.innerText));
                return tweets;
            }
        ''')
        
        await browser.close()
        return tweets

# Reemplaza 'usuario_de_twitter' con el nombre de usuario de Twitter que deseas consultar
username = 'usuario_de_twitter'
tweets = asyncio.run(fetch_recent_tweets(username))
print(tweets)
