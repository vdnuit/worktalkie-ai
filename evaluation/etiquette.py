from utils.gpt import generate_gpt_response

from .models import create_eval_etiq_list_model
from .constants import SCRIPTS_PATH, SCRIPTS_NAME, SYSTEM_PROMPT

def format_script(script: str, input_data: dict) -> str:

    return script.format(
        dialogue=input_data['dialogue']
    )

def count_user_dialogue(input_data):
    return sum(1 for item in input_data.get('dialogue', []) if 'User' in item)

def eval_etiquette(input_data):

    # 스크립트 파일 경로 설정
    script_path = f"{SCRIPTS_PATH}/{SCRIPTS_NAME}.txt"

    # 스크립트 파일 읽기
    with open(script_path, "r", encoding="utf-8") as file:
        script = file.read()

    # 스크립트 포맷
    formatted_script = format_script(script, input_data)
    print(formatted_script)
    
    dialogue_len = count_user_dialogue(input_data)
    print(dialogue_len)
    EvalEtiqList = create_eval_etiq_list_model(dialogue_len, dialogue_len)
    response_format = EvalEtiqList
    # GPT 모델 호출
    response = generate_gpt_response(
        formatted_script, response_format, SYSTEM_PROMPT
    )
    print(response)
    import json
    with open('results/etiq.json', 'w', encoding='utf-8') as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4)

    score = None
    feedback = None

    return score, feedback