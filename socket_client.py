import socket

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'  # 서버의 호스트 주소
    port = 8000         # 서버의 포트 번호

    # 서버에 연결 시도
    client_socket.connect((host, port))
    print("서버에 연결되었습니다.")

    # 서버에 메시지 전송
    message = input("분석할 텍스트를 입력하세요 (2~100자): ")
    client_socket.send(message.encode('utf-8'))

    # 서버로부터 응답 수신
    response = client_socket.recv(1024).decode('utf-8')
    print(f"서버로부터 수신된 응답: {response}")

    # 연결 종료
    client_socket.close()

if __name__ == '__main__':
    run_client()
