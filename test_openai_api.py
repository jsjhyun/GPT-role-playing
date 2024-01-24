import os
import openai
# 각자 OPENAI API KEY 지정 : 이 파일은 버전 관리에는 절대 넣지 마세요.
openai.api_key = os.getenv("OPENAI.API_KEY")

# 텍스트 생성 혹은 문서 요약
response = openai.Completion.create(
    engine="gpt-3.5-turbo",
    prompt="""
Fix grammar errors:
- I is a boy
- You is a girl""".strip(),
)
print(response)
print(response.choices[0].text.strip())

# 챗봇 응답 생성
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "당신은 지식이 풍부한 도우미입니다."},
        {"role": "user", "content": "세계에서 가장 큰 도시는 어디인가요?"},
    ],
)
print(response)
print(response["choices"][0]["message"]["content"])