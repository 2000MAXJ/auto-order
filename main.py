import time
import config
import tools
import url
import dominator

import asyncio
from pyppeteer import launch


async def test():
    browser = await launch(headless=bool(1 - config.debug),
                           userDataDir=config.userDataDir,
                           args=['--disable-infobars'])
    page = await browser.newPage()
    await page.setViewport({'width': config.width, 'height': config.height})
    await page.goto(url.login)
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await asyncio.sleep(100)
    await browser.close()


async def main():
    await dominator.init()

    await dominator.goto(url.login, timeout=5000)
    await dominator.login()

    await dominator.goto(config.sku)
    await dominator.wait_putaway()

    has_remain = await dominator.has_remain()
    if not has_remain:
        print('抢购失败')
        await dominator.close()
        return

    # await dominator.choose()
    await dominator.amount()

    await dominator.order()
    await dominator.buy()

    await asyncio.sleep(3)
    await dominator.close()


if __name__ == '__main__':
    wait_time = tools.get_wait()
    if wait_time > 60:
        print('等待抢购开始 ---- 剩余{0}秒'.format(wait_time - 60))
        time.sleep(wait_time - 60)
    asyncio.get_event_loop().run_until_complete(main())
    # asyncio.get_event_loop().run_until_complete(test())