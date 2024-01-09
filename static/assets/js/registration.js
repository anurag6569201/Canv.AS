let signup=document.querySelector('#signup');
let login=document.querySelector('#login');

function toggleTab(tab) {
    if (tab === 'login') {
        login.style.display = 'block';
        signup.style.display = 'none';
    } else if (tab === 'signup') {
        login.style.display = 'none';
        signup.style.display = 'block';
    }
}