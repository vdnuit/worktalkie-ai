from statistics import mean
import re

from ..constants import SpeechSpeedFeedback

def count_syllables(text):
    # 문장 부호와 공백 제거
    clean_text = re.sub(r'[^\w\s]', '', text)  # 문장 부호 제거
    clean_text = re.sub(r'\s+', ' ', clean_text)  # 다중 공백을 하나로 변경

    syllable_count = 0
    for word in clean_text.split():
        # 한국어면 한 글자당 하나의 음절로 간주
        if re.search(r'[가-힣]', word):
            syllable_count += len(word)
        # 영어면 한 단어당 두 음절로 간주
        elif re.search(r'[a-zA-Z]', word):
            syllable_count += 2
    
    return syllable_count

def cal_speech_speed(input_stt_list):
    spm_list = []

    for turn in input_stt_list:
        data = turn['data']['segments'][0]
        if len(turn['data']['segments']) !=1:
            print("data.segment 확인 요망")
            exit()
        start_time = data['start']
        end_time = data['end']
        syllables = count_syllables(data['text'])
        spm = (syllables/end_time-start_time)*1000*60
        spm_list.append(spm)
    print(spm_list)
    return mean(spm_list)

def speech_speed_rating(spm):
    if spm <= 99:
        return 50, SpeechSpeedFeedback.VERY_SLOW
    elif 99 < spm <= 198:
        return 70, SpeechSpeedFeedback.SLOW
    elif 198 < spm <= 264:
        return 90, SpeechSpeedFeedback.SLIGHTLY_SLOW
    elif 264 < spm <= 400:
        return 100, SpeechSpeedFeedback.NORMAL
    elif 400 < spm <= 520:
        return 90, SpeechSpeedFeedback.SLIGHTLY_FAST
    elif 520 < spm <= 600:
        return 70, SpeechSpeedFeedback.FAST
    else:
        return 50, SpeechSpeedFeedback.VERY_FAST

def get_speech_speed(input_stt_list):
    spm_score = cal_speech_speed(input_stt_list)
    speed_score, speed_feedback = speech_speed_rating(spm_score)
    return speed_score, spm_score, speed_feedback

def eval_proficiency(input_conv_data, input_audio_list, input_stt_list):
    
    speed_score, spm_score, speed_feedback = get_speech_speed(input_stt_list)


    # cal_pause_ratio(input_stt_list)
    # cal_pronunciation_score(input_stt_list)

    proficiency_score = speed_score
    proficiency_feedback = {
        'spm_score': spm_score,
        'speed_feedback': speed_feedback
    }
    return proficiency_score, proficiency_feedback