import os
from openai import OpenAI

import time

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def call_gpt_api(messages, model="gpt-3.5-turbo", temperature=0.7, max_tokens=100, retries=3):
    """
    GPT API를 호출하는 함수, 실패 시 최대 3번까지 재시도

    Args:
    - messages (list): GPT에게 보낼 메시지 리스트 (시스템, 사용자, GPT의 메시지 포함)
    - model (str): 사용할 GPT 모델 (기본값: gpt-3.5-turbo)
    - temperature (float): 답변의 창의성 (0.0 ~ 1.0)
    - max_tokens (int): 생성할 최대 토큰 수
    - retries (int): 실패 시 재시도할 횟수 (기본값: 3)

    Returns:
    - response_text (str): GPT의 응답 텍스트 또는 None (실패 시)
    """
    
    attempt = 0
    while attempt < retries:
        try:
            response = client.chat.completions.create(  # 최신 인터페이스
                model=model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=temperature,
                max_tokens=max_tokens
            )
            response_text = response.choices[0].message.content
            return response_text
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(2)
            if attempt == retries:
                print("Max retries reached. No response.")
                return None

def generate_gpt_response(user_message, system_message="You are a helpful assistant."):
    """
    사용자와 시스템 메시지를 받아 GPT API를 호출하는 함수

    Args:
    - user_message (str): 사용자로부터의 입력 메시지
    - system_message (str): 시스템 메시지 (기본값: "You are a helpful assistant.")

    Returns:
    - response_text (str): GPT의 응답 텍스트
    """
    
    # messages 리스트 구성
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    # GPT API 호출
    return call_gpt_api(messages)

# Code for Test
user_message = 'What is the capital of France? Respond in the same JSON format as: {"capital": your_answer}.'
response = generate_gpt_response(user_message)
print(response)