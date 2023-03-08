import asyncio, json, os, random, warnings, aiohttp, sys
from datetime import datetime
from bs4 import BeautifulSoup

file = open("data.json")
searchData = json.load(file)

path = os.path.dirname(__file__)
warnings.filterwarnings("ignore")

useragents = open("useragents.txt").read().splitlines()  # list of strings (useragents)


async def find_username(username: str):
    timeout = aiohttp.ClientTimeout(total=20)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []  # list of dictionaries
        for u in searchData["sites"]:
            task = asyncio.ensure_future(make_request(session, u, username))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        userJson = {
            "search-params": {
                "username": username,
                "sites-number": len(searchData["sites"]),
                "date": now,
            },
            "sites": [],
        }
        for x in results:
            userJson["sites"].append(x)

        pathSave = os.path.join(
            path, "results", username + ".json"
        )  # $path/results/$username.json
        userFile = open(pathSave, "w")
        json.dump(userJson, userFile, indent=4, sort_keys=True)

        # print(f"[!] Results saved to {username}.json")
        print("\n🔥 DONE 🔥")
        return userJson


async def make_request(session, u, username):
    url = u["url"].format(username=username)
    metadata = []

    useragent = random.choice(useragents)
    headers = {"User-Agent": useragent}

    if "headers" in u:
        headers.update(eval(u["headers"]))  # add more defined header

    jsonBody = None
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
                if "metadata" in u:
                    print("[-] ", end="")
                else:
                    print("[+] ", end="")
                print(
                    f'{u["app"]} account found - {url} [{response.status} {response.reason}]'
                )
                if "metadata" in u:
                    metadata = []
                    for d in u["metadata"]:
                        try:
                            value = eval(d["value"]).strip("\t\r\n").strip()
                            print(f"   ┣━ {d['key']}: {value}")

                            metadata.append(
                                {"type": d["type"], "key": d["key"], "value": value}
                            )
                        except Exception as e:
                            pass
                # Found
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
                # !Found
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
        # Error
        return {
            "id": u["id"],
            "app": u["app"],
            "url": url,
            "response-status": None,
            "status": "ERROR",
            "error-message": repr(e),
            "metadata": metadata,
        }


if __name__ == "__main__":
    asyncio.run(find_username(sys.argv[1]))
