<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8" />
    <title>Login Page</title>
    <link rel="stylesheet" href="/template/s.css" />
</head>
<body>
    <h1>로그인 페이지</h1>
    <p><strong>안내:</strong> <br />
        <ul>
            <li><code>index.php</code> 페이지는 <em>리다이렉트 후 exit 누락</em>으로 취약합니다.</li>
            <li><code>dashboard.php</code> 페이지는 <em>적절한 exit 처리</em>로 취약하지 않습니다.</li>
        </ul>
    </p>
    <form method="post" action="login.php">
        <label>아이디: <input type="text" name="userid" /></label><br />
        <label>비밀번호: <input type="password" name="password" /></label><br />
        <button type="submit">로그인</button>
    </form>
</body>
</html>
