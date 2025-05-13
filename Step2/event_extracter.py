from keybert import KeyBERT
from eunjeon import Mecab
from sentence_transformers import SentenceTransformer

mecab = Mecab()
model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")
kw_model = KeyBERT(model)

def extract_keywords(text, top_n=3):
    stop_words = {
        "속보", "사진", "영상", "단독", "기준", "기록", "사실", "사건", "이슈", "상황",
        "추정", "수준", "선", "결과", "기준", "기대"
    }
    nouns = list(set([w for w in mecab.nouns(text) if w not in stop_words]))
    if not nouns:
        return []
    return [kw[0] for kw in kw_model.extract_keywords(" ".join(nouns), candidates=nouns, top_n=top_n)]

title = "부동산R114 'AI 시세' 서비스 론칭"
print("📌 키워드:", extract_keywords(title))
