from utils.gpt import generate_gpt_response

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
    
    response = generate_gpt_response(script, "너는 사회초년생의 비즈니스 매너를 위한 롤플레잉을 도와주는 AI 챗봇이야.")
    print(script)
    print(response)