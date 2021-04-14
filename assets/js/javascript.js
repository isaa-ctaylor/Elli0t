function darkMode(button) {
    var element = document.body;
    element.classList.toggle("dark-mode");
    button.classList.toggle("fa-sun");
    button.classList.toggle("fa-moon");
}