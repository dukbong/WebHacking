# 1. PoC 환경 구성

- 언어 및 프레임워크 : Python 3.11, Flask
- 데이터베이스: SQLite3 (내장형, 경량 DB)
- PoC 구성
    - `app.py`: 인증 및 주문 조회/결제 기능 포함
    - `models.py`: DB 테이블 생성 및 초기 데이터 삽입
    - `db.py`: DB 초기화 실행 스크립트
    - `Dockerfile`: 도커 이미지 생성용 설정
- Docker 환경
    - Docker 이미지 빌드 후 컨테이너 실행 시 `db.py`를 통해 DB 자동 생성 및 초기화
    - `flask run` 명령으로 0.0.0.0 주소에서 5000 포트로 실행

# 2. PoC 실행 방법

1. Docker 이미지 가져오기
    
    ```bash
    $ docker pull dukbong/poc:2025-06-idor
    ```
    
2. Docker 컨테이너 실행
    
    ```bash
    docker run --name idor-poc -p 5000:5000 dukbong/poc:2025-06-idor
    ```
    
3. 웹 애플리케이션 접속
    
    ```bash
    http://localhost:5000
    ```
    
4. 경로 및 설명
    
    
    | 경로 | 설명 | 메소드 | 비 |
    | --- | --- | --- | --- |
    | /login | 로그인 페이지 | GET, POST |  |
    | /logout | 로그아웃 | GET |  |
    | /dashboard | 로그인 후 메인 대시보드 | GET |  |
    | /order/<uuid> | 주문 상세 및 결 | GET, POST | IDOR 취약점 대상 |
    
    공격자의 주문 UUID는 `c42ba5b5-c572-42fa-a9c6-ed8dc2ae842e` 입니다.
    
5. 기본 사용자 계정
    - attacker / 1234
    - victim / 1234
