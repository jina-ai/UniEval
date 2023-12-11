from prettytable import PrettyTable

def convert_to_json(output_list, src_list=None, ref_list=None, context_list=None, \
            scores=None, doc_id=None, system_id=None):
    """
        Convert the data into the json format.

        output_list: a list of model output
        src_list: source input for different NLG tasks. For example, source document for summarization 
                  and dialogue history for dialogue response generation
        ref_list: human-annotated groundtruth
        context_list: the context needed to evaluate several specific dimension. For example,
                      additional factual information when evaluating engagingness and groundedness in dialogues
        scores: human scores for evaluating the model output. They can be used to calculate the correlation
                between evaluators and human judgements. The scores should be stored in a dictionary. For example,
                {'fluency': 2.0, 'coherence': 3.0} could be the human score for a sample.
        doc_id: the index of the input source. It can be used to calculate summary-level correlation for summarzation
        system_id: the index of the generation system. It can be used to calculate system-level correlation.
    """
    json_data = []
    for i in range(len(output_list)):
        cur = {}
        cur['system_output'] = output_list[i]
        if src_list is not None:
            cur['source'] = src_list[i]
        if ref_list is not None:
            cur['reference'] = ref_list[i]
        if context_list is not None:
            cur['context'] = context_list[i]
        if scores is not None:
            cur['scores'] = scores[i]
        if doc_id is not None:
            cur['doc_id'] = doc_id[i]
        if system_id is not None:
            cur['system_id'] = system_id[i]
        json_data.append(cur)
    return json_data


def add_question(dimension, output, src=None, ref=None, context=None, task=None):
    """
        Add questions to generate input in Bool-QA format for UniEval.
        
        dimension: specific dimension to be evaluated
        src: source input for different NLG tasks. For example, source document for summarization 
             and dialogue history for dialogue response generation.
        output: output text generated by the models
        ref: human-annotataed groundtruth
        context: the context needed to evaluate several specific dimension. For example,
                 additional factual information when evaluating engagingness and groundedness in dialogues.
    """
    
    input_with_question = []
    for i in range(len(output)):
        # For summarization
        if task == 'summarization':
            if dimension == 'fluency':
                cur_input = 'question: Is this a fluent paragraph? </s> paragraph: ' + output[i]
            elif dimension == 'coherence':
                cur_input = 'question: Is this a coherent summary to the document? </s> summary: ' + output[i] + ' </s> document: ' + src[i]
            elif dimension == 'consistency':
                cur_input = 'question: Is this claim consistent with the document? </s> claim: ' + output[i] + ' </s> document: ' + src[i]
            elif dimension == 'relevance':
                cur_input = 'question: Is this summary relevant to the reference? </s> summary: ' + output[i] + ' </s> reference: ' + ref[i]
            else:
                raise NotImplementedError('The input format for this dimension is still undefined. Please customize it first.')
        # For translation
        elif task == 'translation':
            if dimension == 'fluency':
                cur_input = 'question: Is this a fluent translation? </s> translation: ' + output[i]
            elif dimension == 'coherence':
                cur_input = 'question: Is this a coherent translation of the original? </s> translation: ' + output[i] + ' </s> original: ' + src[i]
            elif dimension == 'consistency':
                cur_input = 'question: Is this translation consistent with the original? </s> translation: ' + output[i] + ' </s> original: ' + src[i]
            elif dimension == 'relevance':
                cur_input = 'question: Is this translation relevant to the reference? </s> translation: ' + output[i] + ' </s> reference: ' + ref[i]
            else:
                raise NotImplementedError('The input format for this dimension is still undefined. Please customize it first.')
        elif task == 'qa':
            if dimension == 'naturalness':
                cur_input = 'question: Is this a natural response? </s> response: ' + output[i]
            elif dimension == 'fluency':
                cur_input = 'question: Is this a fluent response? </s> translation: ' + output[i]
            elif dimension == 'coherence':
                cur_input = 'question: Is this a coherent response given the question? </s> response: ' \
                            + output[i] + ' </s> question: ' + src[i]
            elif dimension == 'engagingness':
                cur_input = 'question: Is this an engaging and informative response given the question? </s> response: ' \
                            + output[i] + ' </s> question: ' + src[i]
            elif dimension == 'groundedness':
                cur_input = 'question: Is this response consistent with knowledge in the question? </s> response: ' \
                            + output[i] + ' </s> question: ' + src[i]
            elif dimension == 'understandability':
                cur_input = 'question: Is this an understandable response? </s> response: ' + output[i]
            else:
                raise NotImplementedError(
                    'The input format for this dimension is still undefined. Please customize it first.')
        # For dialogues
        elif task == 'dialogue':
            if dimension == 'naturalness':
                cur_input = 'question: Is this a natural response in the dialogue? </s> response: ' + output[i]
            elif dimension == 'coherence':
                cur_input = 'question: Is this a coherent response given the dialogue history? </s> response: '\
                            + output[i] + ' </s> dialogue history: ' + src[i]
            elif dimension == 'engagingness':
                cur_input = 'question: Is this an engaging and informative response according to the dialogue history and fact? </s> response: '\
                            + output[i] + ' </s> dialogue history: ' + src[i] + ' </s> fact: ' + context[i]
            elif dimension == 'groundedness':
                cur_input = 'question: Is this response consistent with knowledge in the fact? </s> response: '\
                            + output[i] + ' </s> fact: ' + context[i]
            elif dimension == 'understandability':
                cur_input = 'question: Is this an understandable response in the dialogue? </s> response: ' + output[i]
            else:
                raise NotImplementedError('The input format for this dimension is still undefined. Please customize it first.')
        # For data-to-text
        elif task == 'data2text':
            if dimension == 'naturalness':
                cur_input = 'question: Is this a fluent utterance? </s> utterance: ' + output[i]
            elif dimension == 'informativeness':
                cur_input = 'question: Is this sentence informative according to the reference? </s> sentence: '\
                            + output[i] + ' </s> reference: ' + ref[i]
            else:
                raise NotImplementedError('The input format for this dimension is still undefined. Please customize it first.')
        # For factual consistency detection
        elif task == 'fact':
            if dimension == 'consistency':
                cur_input = 'question: Is this claim consistent with the document? </s> claim: ' + output[i] + ' </s> document: ' + src[i]
            else:
                raise NotImplementedError('No other dimensions for the factual consistency detection task.')
        # For new customized tasks
        else:
            raise NotImplementedError('Other tasks are not implemented, please customize specific tasks here.')
        input_with_question.append(cur_input)
    return input_with_question


def print_scores(scores):
    table = PrettyTable(['Dimensions','Score'])
    print('\nEvaluation scores are shown below:')
    dims = list(scores[0].keys())
    for dim in dims:
        cur_score = 0
        for i in range(len(scores)):
            cur_score += scores[i][dim]
        table.add_row([dim, round(cur_score / len(scores), 6)])
    print(table)
