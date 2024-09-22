import json
import argparse
from .eval import run_evaluation
from pydub import AudioSegment

def load_input_data(input_file):
    with open(input_file, 'r') as f:
        return json.load(f)

def load_mp3_audio(audio_path):
    audio = AudioSegment.from_mp3(audio_path)
    return audio
    
def save_output_data(output_file, output_data):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Process a JSON file and send it to the GPT API.')
    parser.add_argument('input_file', type=str, help='The path to the JSON input file.')
    parser.add_argument('input_audio_path', type=str, help='The path to the MP3 input file.')
    parser.add_argument('output_file', type=str, help='The path to the JSON output file.')

    args = parser.parse_args()

    input_data = load_input_data(args.input_file)
    input_audio = load_mp3_audio(args.input_audio_path)
    output_data = run_evaluation(input_data, input_audio)
    save_output_data(args.output_file, output_data)

if __name__ == "__main__":
    main()
