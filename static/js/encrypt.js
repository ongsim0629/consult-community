async function hashPassword(password) {
    // 인코딩된 비밀번호를 가져옴
    const encoder = new TextEncoder();
    const data = encoder.encode(password);

    // SHA-256 해시 생성
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);

    // 해시를 문자열로 변환
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray
        .map((byte) => byte.toString(16).padStart(2, '0'))
        .join('');

    console.log(hashHex);
    return hashHex;
}
