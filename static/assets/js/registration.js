function showContent(contentId) {
    document.querySelectorAll('.login-signup-form-content').forEach(function (content) {
        content.classList.remove('active-login-signup-content');
    });

    document.getElementById(contentId).classList.add('active-login-signup-content');

    document.querySelectorAll('.login-signup-tab').forEach(function (tab) {
        tab.classList.remove('active-login-signup-tab');
    });

    document.querySelector('.login-signup-tab[data-content="' + contentId + '"]').classList.add('active-login-signup-tab');
}