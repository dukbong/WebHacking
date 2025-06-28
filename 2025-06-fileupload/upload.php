<?php
if (isset($_FILES['file'])) {
    $uploadDir = "uploads/";
    
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0777, true);
    }
    
    # 👇 인가 검증이 없습니다. (취약점 포인트!)
    $uploadFile = $uploadDir . basename($_FILES['file']['name']);

    if (move_uploaded_file($_FILES['file']['tmp_name'], $uploadFile)) {
        echo "✅ 업로드 성공: <a href='$uploadFile'>$uploadFile</a>";
    } else {
        echo "❌ 업로드 실패";
    }
}
?>

<h2>파일 업로드</h2>
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="file">
    <button type="submit">업로드</button>
</form>
