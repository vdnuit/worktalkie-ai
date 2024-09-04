from utils.gpt import generate_gpt_response

user_message = 'What is the capital of France? Respond in the same JSON format as: {"capital": your_answer}.'

response = generate_gpt_response(user_message)
print(response)
