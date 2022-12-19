import argparse, asyncio, json, os, random, subprocess, sys, time, warnings, aiohttp
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import Fore, init

file = open("data.json")
searchData = json.load(file)
currentOs = sys.platform
path = os.path.dirname(__file__)
warnings.filterwarnings("ignore")

useragents = open("useragents.txt").read().splitlines()
interfaceType = "CLI"


async def find_username(username, interfaceType):
    startTime = time.time()
    timeout = aiohttp.ClientTimeout(total=20)

    print(
        f"{Fore.LIGHTYELLOW_EX}[!] Searching '{username}' across {len(searchData['sites'])} social networks\033[0m"
    )

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []
        for u in searchData["sites"]:
            task = asyncio.ensure_future(
                make_request(session, u, username, interfaceType)
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        executionTime = round(time.time() - startTime, 1)
        userJson = {
            "search-params": {
                "username": username,
                "sites-number": len(searchData["sites"]),
                "date": now,
                "execution-time": executionTime,
            },
            "sites": [],
        }
        for x in results:
            userJson["sites"].append(x)
        pathSave = os.path.join(path, "results", username + ".json")
        userFile = open(pathSave, "w")
        json.dump(userJson, userFile, indent=4, sort_keys=True)

        print(
            f"{Fore.LIGHTYELLOW_EX}[!] Search complete in {executionTime} seconds\033[0m"
        )
        print(f"{Fore.LIGHTYELLOW_EX}[!] Results saved to {username}.json\033[0m")
        return userJson


async def make_request(session, u, username, interfaceType):
    url = u["url"].format(username=username)
    jsonBody = None
    useragent = random.choice(useragents)
    headers = {"User-Agent": useragent}
    metadata = []
    if "headers" in u:
        headers.update(eval(u["headers"]))
    if "json" in u:
        jsonBody = u["json"].format(username=username)
        jsonBody = json.loads(jsonBody)
    try:
        async with session.request(
            u["method"], url, json=jsonBody, headers=headers, ssl=False
        ) as response:
            responseContent = await response.text()
            if (
                "content-type" in response.headers
                and "application/json" in response.headers["Content-Type"]
            ):
                jsonData = await response.json()
            else:
                soup = BeautifulSoup(responseContent, "html.parser")

            if eval(u["valid"]):
                print(
                    f'{Fore.LIGHTGREEN_EX}[+]\033[0m - #{u["id"]} {Fore.BLUE}{u["app"]}\033[0m {Fore.LIGHTGREEN_EX}account found\033[0m - {Fore.YELLOW}{url}\033[0m [{response.status} {response.reason}]\033[0m'
                )
                if "metadata" in u:
                    metadata = []
                    for d in u["metadata"]:
                        try:
                            value = eval(d["value"]).strip("\t\r\n")
                            print(f"   |--{d['key']}: {value}")
                            metadata.append(
                                {"type": d["type"], "key": d["key"], "value": value}
                            )
                        except Exception as e:
                            pass
                return {
                    "id": u["id"],
                    "app": u["app"],
                    "url": url,
                    "response-status": f"{response.status} {response.reason}",
                    "status": "FOUND",
                    "error-message": None,
                    "metadata": metadata,
                }
            else:
                return {
                    "id": u["id"],
                    "app": u["app"],
                    "url": url,
                    "response-status": f"{response.status} {response.reason}",
                    "status": "NOT FOUND",
                    "error-message": None,
                    "metadata": metadata,
                }
    except Exception as e:
        return {
            "id": u["id"],
            "app": u["app"],
            "url": url,
            "response-status": None,
            "status": "ERROR",
            "error-message": repr(e),
            "metadata": metadata,
        }


def list_sites():
    for i, u in enumerate(searchData["sites"], 1):
        print(f'{i}. {u["app"]}')


def read_results(file):
    try:
        pathRead = os.path.join(path, "results", file)
        f = open(pathRead, "r")
        jsonD = json.load(f)
        print(f"Loaded results file: {file}")
        print(f"Username: {jsonD['search-params']['username']}")
        print(f"Number of sites: {jsonD['search-params']['sites-number']}")
        print(f"Date: {jsonD['search-params']['date']}")
        print("-------------------------------------------------")
        for u in jsonD["sites"]:
            if u["status"] == "FOUND":
                print(
                    f'{Fore.LIGHTGREEN_EX}[+]\033[0m - {Fore.BLUE}{u["app"]}\033[0m {Fore.LIGHTGREEN_EX}account found\033[0m - {Fore.YELLOW}{u["url"]}\033[0m [{u["response-status"]}]\033[0m'
                )
                if u["metadata"]:
                    for d in u["metadata"]:
                        print(f"   |--{d['key']}: {d['value']}")
            elif u["status"] == "ERROR":
                print(
                    f'{Fore.RED}[X]\033[0m - {Fore.BLUE}{u["app"]}\033[0m error on request ({u["error-message"]}) - {Fore.YELLOW}{u["url"]}\033[0m'
                )
            elif u["status"] == "NOT FOUND":
                print(
                    f'{Fore.WHITE}[-]\033[0m - {Fore.BLUE}{u["app"]}\033[0m account not found - {Fore.YELLOW}{u["url"]}\033[0m [{u["response-status"]}]\033[0m'
                )

    except Exception as e:
        print(f"{Fore.RED}[X] Error reading file [{repr(e)}]")


if __name__ == "__main__":
    init()

    parser = argparse.ArgumentParser(
        description="An OSINT tool to search for accounts by username in social networks."
    )
    parser.add_argument(
        "-u",
        action="store",
        dest="username",
        required=False,
        help="The target username.",
    )
    parser.add_argument(
        "--list-sites",
        action="store_true",
        dest="list",
        required=False,
        help="List all sites currently supported.",
    )
    parser.add_argument(
        "-f", action="store", dest="file", required=False, help="Read results file."
    )
    arguments = parser.parse_args()

    if arguments.username:
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except:
            pass

        asyncio.run(find_username(arguments.username, interfaceType))
    elif arguments.list:
        list_sites()
    elif arguments.file:
        read_results(arguments.file)
