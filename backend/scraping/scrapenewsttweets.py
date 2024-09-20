import asyncio
from playwright.async_api import async_playwright

async def login_to_twitter(page, username, password):
    # Navega a la página de inicio de sesión de Twitter
    await page.goto('https://twitter.com/login')

    # Espera a que los campos de inicio de sesión se carguen y rellénalos
    await page.fill('input[type="text"]', username)

    botones = await page.query_selector_all('button')

    await botones[-2].click()

    await page.fill('input[type="text"]', password)

    botones = await page.query_selector_all('button')

    await botones[-1].click()

    # Espera a que se complete la navegación y se cargue la página principal de Twitter
    # await page.wait_for_navigation()

async def fetch_recent_tweets(username, twitter_username, twitter_password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state="auth.json")
        page = await context.new_page()

        await page.goto("https://x.com/MetroCDMX")

        # # Inicia sesión en Twitter
        # await login_to_twitter(page, twitter_username, twitter_password)

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

        latest_tweet = await page.query_selector('article')
        print(latest_tweet)
        replies = []
        if latest_tweet:
            await latest_tweet.click()
            replies = await page.query_selector_all('article')


        await browser.close()
        # return replies
        return (tweets, replies)

# Reemplaza 'usuario_de_twitter' con el nombre de usuario de Twitter que deseas consultar
target_username = 'MetroCDMX'

# Credenciales de tu cuenta de Twitter
twitter_username = 'TepalYael79389'
twitter_password = 'Hans66306713333'

tweets = asyncio.run(fetch_recent_tweets(target_username, twitter_username, twitter_password))
print(tweets)
