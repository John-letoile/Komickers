import httpx
from pathlib import Path

NEW_URL = "https://getcomics.org/dls/UuuIGuKucVJGvf2IzVkqKspX3tjmGQIloubBAVJ4xeLwVFbFU4Li5Ue6/wrjz64qbGu3LgAisEv6RZuGcYxZ/WoGf+ohOzN74mo/933SGWIYV41fnJokJzKGZuTgLuzzJxPMrVqvGNkgG56HC824N1o7j3daNeMsr2IOc/Zqei8oltVNQ+dtbkWgEqsYVlL7:MWqnGoh+7d65hkpryw8E+g=="

path = Path("test.txt")
with httpx.Client() as client:
    response: httpx.Response = client.get(
        "https://getcomics.org/dc/captain-america-13-2026/", follow_redirects=True
    )

    if response.status_code == 302:
        print("BYYY")

    else:
        print("HIIII")
