<?php
// 간단 인증 상태 (예시로 false 고정)
$isLoggedIn = false;

if (!$isLoggedIn) {
    header("Location: login.php");
    // exit();  // 주석 처리 → CWE-698 취약점 발생
}

// 이후에 HTML 출력됨 (리다이렉트 후에도 클라이언트로 노출)
?>
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8" />
    <title>Index Page</title>
    <link rel="stylesheet" href="/template/s.css" />
</head>
<body>
    <h1>보안 취약한 Index 페이지</h1>
    <p>로그인하지 않아도 이 내용이 노출됩니다.</p>
</body>
</html>
