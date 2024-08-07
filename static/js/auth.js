const ACCESS_TOKEN_KEY = 'access_token';

const setAccessToken = (token) => {
    sessionStorage.setItem(ACCESS_TOKEN_KEY, token);
    return;
};

const getAccesssToken = () => {
    const token = sessionStorage.getItem(ACCESS_TOKEN_KEY);
    return token;
};

const checkAuthorizedAccessAndRedirect = () => {
    const token = getAccesssToken();

    if (!token) {
        alert('로그인이 필요합니다.');

        // fyi. 로그인 성공 이후 redirect 시킬 곳
        const curUrl = window.location.href;
        window.location.href =
            PAGE_URLS['SIGN_IN'] + '?redirect=' + encodeURIComponent(curUrl);

        return;
    }

    return true;
};

const getUserObjFromAccessToken = () => {
    const token = getAccesssToken();

    if (checkAuthorizedAccessAndRedirect()) {
        const base64Payload = token.split('.')[1];
        const base64 = base64Payload.replace(/-/g, '+').replace(/_/g, '/');
        const decodedJWT = JSON.parse(
            decodeURIComponent(
                window
                    .atob(base64)
                    .split('')
                    .map(function (c) {
                        return (
                            '%' +
                            ('00' + c.charCodeAt(0).toString(16)).slice(-2)
                        );
                    })
                    .join('')
            )
        );

        return {
            nickname: decodedJWT.nickname,
            user_id: decodedJWT.user_id,
        };
    } else {
        return {
            // TODO: null 이 좋을지 고민 필요
            nickname: '비로그인',
            user_id: '-1',
        };
    }
};
