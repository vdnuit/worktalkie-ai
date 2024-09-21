from utils.gpt import generate_gpt_response
from .relevance import eval_relevance
from .etiquette import eval_etiquette

def run_evaluation(input_data):
    print("RUN EVALUATION...")
    # eval_relevance
    relevance_score = eval_relevance(input_data)
    print(relevance_score)

    # eval_fluency
    # eval_etiquette
    etiquette_score, etiquette_feedback = eval_etiquette(input_data)
