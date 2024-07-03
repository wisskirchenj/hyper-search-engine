import nltk

def rouge2(candidate, reference):
    candidate_bigrams = set(nltk.bigrams(candidate.split()))
    reference_bigrams = set(nltk.bigrams(reference.split()))

    intersection = candidate_bigrams.intersection(reference_bigrams)
    precision = len(intersection) / len(candidate_bigrams)
    recall = len(intersection) / len(reference_bigrams)

    if precision + recall == 0:
        f1_score = 0
    else:
        f1_score = 2 * (precision * recall) / (precision + recall)

    return round(f1_score, 3)