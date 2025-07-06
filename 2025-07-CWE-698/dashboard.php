<?php
// dashboard.php - 안전한 페이지 예시

// 인증 여부 체크 (예시)
$isLoggedIn = false;

if (!$isLoggedIn) {
    header("Location: login.php");
    exit();  // 반드시 exit() 호출로 실행 종료
}

// 인증된 사용자에게 보여줄 페이지 내용
?>
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8" />
    <title>Dashboard - 안전한 페이지</title>
    <link rel="stylesheet" href="/template/s.css" />
</head>
<body>
    <h1>안전하게 보호된 대시보드 페이지입니다.</h1>
    <p>로그인된 사용자만 이 페이지를 볼 수 있습니다.</p>
</body>
</html>
