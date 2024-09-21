from utils.gpt import generate_gpt_response
from .relevance import eval_relevance

def run_evaluation(input_data):
    print("RUN EVALUATION...")
    # eval_relevance
    relevance_score = eval_relevance(input_data)
    print(relevance_score)

    # eval_fluency
    # eval_etiquette

