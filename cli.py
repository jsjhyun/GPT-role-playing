import os
import openai

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 상황극 설정
language = "English"
gpt_name = "Steve"
level_string = f"a beginner in {language}"
level_word = "simple"
situation_en = "make new friends"
my_role_en = "me"
gpt_role_en = "new friend"

SYSTEM_PROMPT = (
    f"You are helpful assistant supporting people learning {language}. "
    f"Your name is {gpt_name}. Please assume that the user you are assisting "
    f"is {level_string}. And please write only the sentence without "
    f"the character role."
)
USER_PROMPT = (
    f"Let's have a conversation in {language}. Please answer in {language} only "
    f"without providing a translation. And please don't write down the "
    f"pronunciation either. Let us assume that the situation in '{situation_en}'. "
    f"I am {my_role_en}. The character I want you to act as is {gpt_role_en}. "
    f"Please make sure that "
    f"I'm {level_string}, so please use {level_word} words as much as possible. "
    f"Now, start a conversation with the first sentence!"
)
# 대화 내역을 누적할 리스트
messages = [{"role": "system", "content": SYSTEM_PROMPT}]


def gpt_query(user_query: str) -> str:
    global messages # 코드를 간결하게 쓰기 위해 전역변수를 사용했을 뿐, 전역변수 사용은 안티패턴입니다.

    messages.append({
        "role": "user",
        "content": user_query,
    })

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=1
    )
    assistant_message = response["choices"][0]["message"]["content"]
    messages.append({
        "role": "assistant",
        "content": assistant_message,
    })

    return assistant_message


def main():
    # 초기 응답 출력
    assistant_message = gpt_query(USER_PROMPT)
    print(f"[assistant] {assistant_message}")
    # 유저 입력을 받아서 전달하고, 그에 대한 응답을 출력
    # 빈 문자열을 입력받거나, Ctrl-C 입력을 받으면 대화 루프를 끝냅니다.
    try:
        while line := input("[user] ").strip():
            response = gpt_query(line)
            print("[assistant] {}".format(response))
    except (EOFError, KeyboardInterrupt):
        print("terminated by user.")


if __name__ == "__main__":
    main()