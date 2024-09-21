from utils.gpt import generate_gpt_response

from .models import EvalEtiqList
from .constants import SCRIPTS_PATH, SCRIPTS_NAME, SYSTEM_PROMPT

def format_script(script: str, input_data: dict) -> str:

    return script.format(
        dialogue=input_data['dialogue']
    )
def count_user_dialogue(input_data):
    return sum(1 for item in input_data.get('dialogue', []) if 'User' in item)

def generate_gpt_response_with_retry(formatted_script, response_format, system_prompt, valid_len, max_retries=3):
    retries = 0
    while retries < max_retries:
        # GPT 모델 호출
        response = generate_gpt_response(formatted_script, response_format, system_prompt)
        print(response)

        res_len = len(response['dialogue'])
        # response 길이가 valid_len과 같은지 확인
        if res_len == valid_len:
            return response  # 성공하면 반환

        # 길이가 맞지 않으면 재시도
        retries += 1
        print(f"Response 길이가 맞지 않습니다. 재시도 중... ({retries}/{max_retries})")

    # 최대 재시도에 도달한 경우 오류 메시지 출력
    raise ValueError(f"Response 길이가 {valid_len}과 맞지 않습니다. 최대 {max_retries}번 재시도했으나 실패했습니다.")

def eval_etiquette(input_data):

    # 스크립트 파일 경로 설정
    script_path = f"{SCRIPTS_PATH}/{SCRIPTS_NAME}.txt"

    # 스크립트 파일 읽기
    with open(script_path, "r", encoding="utf-8") as file:
        script = file.read()

    # 스크립트 포맷
    formatted_script = format_script(script, input_data)
    print(formatted_script)
    
    response_format = EvalEtiqList
    valid_len = count_user_dialogue(input_data)

    # GPT 모델 호출
    try:
        response = generate_gpt_response_with_retry(
            formatted_script, response_format, SYSTEM_PROMPT, valid_len
            )
    except ValueError as e:
        print(f"오류 발생: {e}")

    import json
    with open('results/etiq.json', 'w', encoding='utf-8') as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4)

    score = None
    feedback = None

    return score, feedback