from typing import Literal

import requests
from bs4 import BeautifulSoup


def google_translate(
    text: str, # 번역 대상
    source: Literal["auto", "en", "ko"],
    target: Literal["en", "ko"],
):
    text = text.strip()
    if not text: # 빈 문자열
        return ""

    endpoint_url = "https://translate.google.com/m"  # 크롤링 주소 지정

    params = { # QueryString 인자를 사전(dict)로 지정
        "hl": source,
        "sl": source,
        "tl": target,
        "q": text,
        "ie": "UTF-8",
        "prev": "_m",
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"
        ),
    }
    # 위 크롤링한 거 get 요청
    res = requests.get(
        endpoint_url,
        params=params,
        headers=headers,
        timeout=5,
    )
    res.raise_for_status()  # 응답 200 아니면 예외 발생

    soup = BeautifulSoup(res.text, "html.parser") # 응답 HTML 문자열 파싱
    translated_text = soup.select_one(".result-container").text.strip() # 번역 된 문자열

    return translated_text