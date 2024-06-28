document.addEventListener('DOMContentLoaded', function() {
        let valoracionS = document.querySelectorAll('.valoracionS');
        let valoracionI = document.querySelectorAll('.valoracionI');
        let s = document.querySelectorAll('.s');
        let a = document.querySelector('#admin');
        let navbar = document.querySelector('nav');
        let exitButton = document.querySelectorAll('.icon-button')
        let ignoreBackground = document.querySelector('#ignoreBackground');
        let subtitle = document.querySelectorAll('.subtitulo');
        let footer = document.querySelector('footer');
        let td = document.querySelectorAll('td.text-start + td.text-start')
        for (let i = 0; i < valoracionS.length; i++) {
            valoracionS[i].addEventListener('click', function() {
                s[i].style.visibility = 'visible';
                ignoreBackground.style.visibility = 'visible';
                navbar.style.visibility = 'hidden';
                footer.style.visibility = 'hidden';
            });
            valoracionI[i].addEventListener('click', function() {
                s[i].style.visibility = 'visible';
                ignoreBackground.style.visibility = 'visible';
                navbar.style.visibility = 'hidden';
                footer.style.visibility = 'hidden';
            });
            exitButton[i].addEventListener('click', function() {
                s[i].style.visibility = 'hidden';
                ignoreBackground.style.visibility = 'hidden';
                navbar.style.visibility = 'visible';
                footer.style.visibility = 'visible';
            });
            ignoreBackground.addEventListener('click', function(){
                s[i].style.visibility = 'hidden';
                ignoreBackground.style.visibility = 'hidden';
                navbar.style.visibility = 'visible';
                footer.style.visibility = 'visible';
            });
        }
    });
