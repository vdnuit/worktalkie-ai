import json
import argparse
from utils.gpt import generate_gpt_response

def main():
    parser = argparse.ArgumentParser(description='Process a JSON file and send it to the GPT API.')
    parser.add_argument('json_file', type=str, help='The path to the JSON input file.')
    args = parser.parse_args()

    with open(args.json_file, 'r') as f:
        data = json.load(f)

    # user_message = data.get("user_message", "")

    # if not user_message:
    #     print("Error: 'user_message' field is missing in the JSON file.")
    #     return
    user_message = 'What is the capital of France? Respond in the same JSON format as: {"capital": your_answer}.'

    response = generate_gpt_response(user_message)
    print(response)

if __name__ == "__main__":
    main()
