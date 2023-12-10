import socket
from konlpy.tag import Okt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import pandas as pd
import sentimentAnalysis

# 모델 및 토큰화, 패딩 설정
model = load_model('textSA_ver1.h5')
tokenizer = Tokenizer()
okt = Okt()
MAX_SEQUENCE_LENGTH = 8

# 감탄사, 조사들은 제거할 수 있도록 정의
stop_words = set(['은', '는', '이', '가', '하', '아', '것', '들', '의', '있', '되', '수', '보', '주', '등', '한'])

# 데이터 정제
train_data = pd.read_csv('ratingsTrain.txt', header=0, delimiter='\t', quoting=3)
clean_train_data = []
for review in train_data['document']:
    if type(review) == str:
        clean_train_data.append(sentimentAnalysis.preprocessing(review, okt, True, stop_words))
    else:
        clean_train_data.append([])

# Text to Number
tokenizer.fit_on_texts(clean_train_data)
train_sequence = tokenizer.texts_to_sequences(clean_train_data)
train_inputs = pad_sequences(train_sequence, maxlen=MAX_SEQUENCE_LENGTH, padding='post')

def analyze_sentiment(data):
    preprocessed_data = sentimentAnalysis.preprocessing(data, okt, True, stop_words)
    test_data = [preprocessed_data]
    test_token = tokenizer.texts_to_sequences(test_data)
    test_seq = pad_sequences(test_token, maxlen=MAX_SEQUENCE_LENGTH, padding='post')
    ret = model.predict(test_seq)
    if ret > 0.5:
        return "긍정"
    elif ret < 0.5:
        return "부정"
    else:
        return "중립"

def run_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8000
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"소켓 서버가 {port}번 포트에서 대기중입니다.")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"{addr}에서 연결되었습니다.")

        # 클라이언트로부터 데이터 수신
        data = client_socket.recv(1024).decode('utf-8')
        print(f"수신된 데이터: {data}")

        # 텍스트 길이 검증
        if 2 <= len(data) <= 100:
            # 감정 분석 수행
            sentiment = analyze_sentiment(data)
        else:
            sentiment = "텍스트 길이가 유효하지 않습니다."

        # 클라이언트에게 결과 전송
        client_socket.send(sentiment.encode('utf-8'))

        # 연결 종료
        client_socket.close()

    server_socket.close()

if __name__ == '__main__':
    run_socket_server()
