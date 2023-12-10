from konlpy.tag import Okt
import re

okt = Okt()
# 감탄사, 조사들은 제거할 수 있도록 정의
stop_words = set(['은', '는', '이', '가', '하', '아', '것', '들', '의', '있', '되', '수', '보', '주', '등', '한'])

# 데이터 정제
def refine_data(train_data, data):
    clean_train_data = []

    for review in train_data['document']:
        if type(data) == str:
            clean_train_data.append(preprocessing(data, okt, True, stop_words))
        else:
            clean_train_data.append([])

# 전처리 함수 정의
def preprocessing(review, okt, remove_stopwords=False, stop_words=None):
    if stop_words is None:
        stop_words = set()

    try:
        # 문장에서 한글만 뽑아냄
        review_text = re.sub("[^가-힣ㄱ-하-ㅣ\s]", "", review)

        # okt 라이브러리로 단어의 어간별로 분리
        word_review = okt.morphs(review_text, stem=True)

        # 불용어 제거
        if remove_stopwords:
            word_review = [token for token in word_review if token not in stop_words]

        return word_review

    except Exception as e:
        print(f"An error occurred during preprocessing: {e}")
        return None

