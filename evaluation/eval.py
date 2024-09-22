from utils.gpt import generate_gpt_response
from .relevance import eval_relevance
from .etiquette import eval_etiquette
from .proficiency import eval_proficiency

def run_evaluation(input_data, input_audio):
    print("RUN EVALUATION...")
    # eval_relevance
    relevance_score = eval_relevance(input_data)
    print(relevance_score)

    # eval_proficiency
    proficiency_score, proficiency_feedback = eval_proficiency(input_data, input_audio)
    
    # eval_etiquette
    etiquette_score, etiquette_feedback = eval_etiquette(input_data)

    return {
        'relevance_score': relevance_score,
        'etiquette_score': etiquette_score,
        'etiquette_feedback': etiquette_feedback
    }
