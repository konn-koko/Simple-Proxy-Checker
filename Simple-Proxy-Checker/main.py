import asyncio
import aiofiles
import aiohttp
import datetime
import questionary
from colorama import Fore


async def check(check_data: str, timeout: int, output_file_name: str) -> None:
    try:
        async with aiohttp.ClientSession() as client:
            response = await client.get("https://api.ipify.org?format=json", timeout=timeout, proxy=f"http://{check_data}")
            if response.status == 200 and check_data is not None:
                print(f"[{Fore.GREEN}+{Fore.RESET}] Checked: Available {check_data}")
                async with aiofiles.open(f'{output_file_name}-live-proxies.txt', mode='a', encoding='utf-8') as f:
                    await f.write(f"{check_data}\n")
                return None
            else:
                print(f"[{Fore.RED}!{Fore.RESET}] Checked: Usage prohibited {check_data}")
                return None
    except aiohttp.ClientError or AttributeError:
        print(f"[{Fore.RED}!{Fore.RESET}] Checked: Usage prohibited {check_data}")
        return None


async def main(path: str):
    tasks = []
    execution_date = str(datetime.date.today())
    print(f"[{Fore.GREEN}#{Fore.RESET}] INFO: Start")
    async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
        async for line in f:
            tasks.append(asyncio.ensure_future(check(check_data=str(line).strip('\n'), timeout=5, output_file_name=execution_date)))
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"[{Fore.GREEN}#{Fore.RESET}] INFO: Completion")


if __name__ == '__main__':
    asyncio.run(main(path=questionary.path(
        "Enter the path of the proxy file to be checked."
    ).ask()))
