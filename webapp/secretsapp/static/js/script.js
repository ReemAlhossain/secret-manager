// Wacht tot de DOM volledig is geladen
document.addEventListener('DOMContentLoaded', function() {

    // Elementen selecteren
    const loginWrapper = document.querySelector('#loginWrapper');
    const registerWrapper = document.querySelector('#registerWrapper');
    const loginLink = document.querySelector('.loginlink');
    // const registerLink = document.querySelector('.register-link');
    const btnPopup = document.querySelector('.btnLogin-popup');
    const iconClose = document.querySelector('.icon-close');
    const registerButton = document.querySelector("#registerButton");
    const backToHomeButton = document.querySelector("#backToHomeButton");

    // Debug log voor de btnPopup
    console.log(btnPopup)

    // Event listener voor inlogknop
    btnPopup.addEventListener('click', ()=> {
        loginWrapper.classList.add('active-popup');
    });

    // Event listener voor sluit-icoon
    iconClose.addEventListener('click', ()=> {
        loginWrapper.classList.remove('active-popup');
    }); 

    // Event listener voor registratieknop
    registerButton.addEventListener('click', () => {
        loginWrapper.classList.add('active-popup');
        registerWrapper.classList.remove('active-popup');
    });

    // Event listener voor "Terug naar Home" knop
    backToHomeButton.addEventListener('click', () => {
        loginWrapper.classList.remove('active-popup');
        registerWrapper.classList.add('active-popup');
    });

    // ... Voeg hier eventueel nog meer functionaliteit toe

});
