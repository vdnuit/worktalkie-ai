from utils.gpt import generate_gpt_response
from .models import StartConv, ContinueConv

def update_missions(input_data, response):
    # 미션 완료 여부 업데이트
    input_data['is_missions_completed'][0] = response['is_mission1'] or input_data['is_missions_completed'][0]
    input_data['is_missions_completed'][1] = response['is_mission2'] or input_data['is_missions_completed'][1]
    input_data['is_missions_completed'][2] = response['is_mission3'] or input_data['is_missions_completed'][2]

    # 대화 종료 여부 업데이트
    input_data['is_end'] = response['is_end'] or input_data['is_end']

    return input_data

def run_conversation(input_data, status):
    
    with open(f"scripts/{status}.txt", "r", encoding="utf-8") as file:
        script = file.read()

    script = script.format(
        senario = input_data['senario'],
        background = input_data['background'],
        role_of_ai = input_data['role_of_ai'],
        missions = input_data['missions'],
        dialogue = input_data['dialogue']
    )
    
    print(script)
    if status == "start_conversation":
        response_format = StartConv
    elif status == "continue_conversation":
        response_format = ContinueConv

    response = generate_gpt_response(script, response_format, "너는 사회초년생의 비즈니스 매너를 위한 롤플레잉을 도와주는 AI 챗봇이야.")
    print(response)

    input_data['dialogue'].append({"AI": response['answer']})

    if status == "continue_conversation":
        input_data = update_missions(input_data, response)

    return input_data