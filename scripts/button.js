
document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('theme-toggle');
    const body = document.body;
    const icon = toggleBtn.querySelector('i');

    // 1. Check Local Storage on Page Load
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        body.classList.add('light-mode');
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon'); // Show Moon if currently Light
    } else {
        // Default is Dark
        icon.classList.add('fa-sun'); // Show Sun if currently Dark
    }

    // 2. Handle Click
    toggleBtn.addEventListener('click', () => {
        body.classList.toggle('light-mode');
        
        if (body.classList.contains('light-mode')) {
            localStorage.setItem('theme', 'light');
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        } else {
            localStorage.setItem('theme', 'dark');
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    });

    // Функция для обновления темы Giscus
    function updateGiscusTheme(theme) {
        const iframe = document.querySelector('iframe.giscus-frame');
        if (!iframe) return;
        
        // Выбираем тему Giscus в зависимости от вашей темы
        // Если theme === 'light-mode', ставим светлую тему Giscus, иначе темную
        const giscusTheme = theme === 'light-mode' ? 'light' : 'transparent_dark';

        iframe.contentWindow.postMessage(
            { giscus: { setConfig: { theme: giscusTheme } } },
            'https://giscus.app'
        );
    }

    // ВАЖНО: Вызовите эту функцию там, где вы переключаете класс body
    // Например, внутри вашего обработчика клика:
    themeToggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('light-mode');
        
        // ... ваш код сохранения в localStorage ...

        // Проверяем, какая тема сейчас активна
        const currentTheme = document.body.classList.contains('light-mode') ? 'light-mode' : 'dark-mode';
        updateGiscusTheme(currentTheme);
});
});