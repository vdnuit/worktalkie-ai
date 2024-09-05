import json
import argparse
from utils.gpt import generate_gpt_response
from conversation.main import run_conversation

def main():
    parser = argparse.ArgumentParser(description='Process a JSON file and send it to the GPT API.')
    parser.add_argument('json_file', type=str, help='The path to the JSON input file.')
    args = parser.parse_args()

    with open(args.json_file, 'r') as f:
        input_data = json.load(f)

    turn_num= len(input_data['dialogue'])

    if turn_num == 0:
        run_conversation(input_data, "start_conversation")
    elif turn_num >=20:
        run_conversation(input_data)
    else:
        run_conversation(input_data)

if __name__ == "__main__":
    main()
