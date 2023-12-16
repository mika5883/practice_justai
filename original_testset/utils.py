from requests import post
def swagger_prompt(text:str=None):
    if text == None:
        raise Exception('Provide a query in str format')
    
    url = 'http://109.248.175.148:9000/predict'

    headers = {'accept': 'application/json',
            'Content-Type': 'application/json'}
    body = \
        {
        "data": {
            "texts": [
            f"{text}"
            ]
        },
        "config": {
            "caila_config": {
            "num_candidates": 10,
            "candidate_radius": 0,
            "vectorizer_batch_size": 10,
            "rescale_method": "none",
            "prompt": "You are a Russian-speaking question answering system. You help users look for information in the Documentation. Try to answer their Question or find documents related to the Question according to the Documentation provided below. Each document starts from New document. Follow the rules: (1) Firstly, find relevant documents related to the Question. It is possible that there are no related documents in the Documentation. (2) Answer strictly according to the documents. Don't make things up. (3) Question can be formulated as either an ordinary question with a question mark or words (когда работает банк?) or a search query (режим работы банка). You must deal with all types. (4) If there is more than one answer to the Question, list all possible solutions separately. (5) If there is not a direct Answer, but just information on the related topic, answer with it. (6) If you can't find relevant documents, ask a user to reformulate the Question in your answer. (7) Answer the Question in Russian. Documentation: {}; Question: {}; Answer:",
            "batch_size": 200
            }
        }
        }
    return post(url, headers=headers, json=body)