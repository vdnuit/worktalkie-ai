from .spm import get_speech_speed
from .pause import get_pause_ratio

def eval_proficiency(input_conv_data, input_audio_list, input_stt_list):
    
    speed_score, speed_spm, speed_feedback = get_speech_speed(input_stt_list)

    pause_score, pause_ratio, pause_feedback = get_pause_ratio(input_stt_list)
    # cal_pronunciation_score(input_stt_list)

    proficiency_score = speed_score
    proficiency_feedback = {
        'speed_spm': speed_spm,
        'speed_feedback': speed_feedback
    }
    return proficiency_score, proficiency_feedback