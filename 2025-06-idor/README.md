# 1. IDOR 취약점 개요

IDOR (Insecure Direct Object Reference)는 인증이나 권한 검증 없이 직접적으로 시스템 자원에 접근할 수 있도록 허용하는 취약점으로 보안 검증이 미흡한 경우 공격자가 URL 파라미터나 요청 데이터를 조작해 다른 사용자의 민감한 정보를 열람하거나 조작할 수 있습니다.

# 2. PoC 개요

본 PoC는 IDOR(Insecure Direct Object Reference) 취약점 중 주문 결제 권한 검증 누락 사례를 재현합니다.

인증된 사용자가 다른 사용자의 주문 UUID를 조작해 결제 처리를 진행할 수 있는 문제를 실습용 환경에서 확인할 수 있습니다.

# 3. PoC 환경 구성

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

# 4. PoC 실행 방법

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
    
    
    | 경로 | 설명 | 메소드 | 비고 |
    | --- | --- | --- | --- |
    | /login | 로그인 페이지 | GET, POST |  |
    | /logout | 로그아웃 | GET |  |
    | /dashboard | 로그인 후 메인 대시보드 | GET |  |
    | /order/<uuid> | 주문 상세 및 결제 | GET, POST | IDOR 취약점 시연 대상 |
    
    공격자의 주문 UUID는 `c42ba5b5-c572-42fa-a9c6-ed8dc2ae842e` 입니다.
    
5. 기본 사용자 계정
    - attacker / 1234
    - victim / 1234

# 5. PoC 재현 방법

1. 피해자(victim) 계정으로 로그인을 합니다.
2. (가정) 외부에서 공격자(attacker)가 공유한 링크를 클릭 합니다.
3. 현재 로그인(인증)된 사용자는 피해자(victim)로 나와있는 것을 확인합니다.
4. 결제하기 버튼을 클릭합니다.
5. 결제 시 권한 검증이 미비하여 피해자(victim)은 공격자(attacker)의 주문을 결제하게 됩니다.
