import json
import argparse
from utils.gpt import generate_gpt_response
from conversation.main import run_conversation

def main():
    parser = argparse.ArgumentParser(description='Process a JSON file and send it to the GPT API.')
    parser.add_argument('input_file', type=str, help='The path to the JSON input file.')
    parser.add_argument('output_file', type=str, help='The path to the JSON output file.')

    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    turn_num= len(input_data['dialogue'])

    if turn_num == 0:
        output_data = run_conversation(input_data, "start_conversation")
    elif turn_num >=20:
        output_data = run_conversation(input_data, "terminate_conversation")
    else:
        output_data = run_conversation(input_data, "continue_conversation")

    with open(args.output_file, 'w', encoding='utf-8') as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    main()
