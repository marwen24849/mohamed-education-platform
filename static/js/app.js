document.addEventListener('DOMContentLoaded', function () {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    }

    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        const icon = themeToggle.querySelector('i');
        const applyIcon = () => {
            const mode = document.documentElement.getAttribute('data-theme');
            if (mode === 'dark') {
                icon.className = 'bi bi-moon-stars-fill';
            } else {
                icon.className = 'bi bi-sun-fill';
            }
        };
        applyIcon();

        themeToggle.addEventListener('click', function () {
            const currentTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', currentTheme);
            localStorage.setItem('theme', currentTheme);
            applyIcon();
        });
    }

    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    favoriteButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const id = button.dataset.documentId;
            const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
            if (favorites.includes(id)) {
                const filtered = favorites.filter(item => item !== id);
                localStorage.setItem('favorites', JSON.stringify(filtered));
                button.innerHTML = '<i class="bi bi-heart"></i> Ajouter aux favoris';
                return;
            }
            favorites.push(id);
            localStorage.setItem('favorites', JSON.stringify(favorites));
            button.innerHTML = '<i class="bi bi-heart-fill"></i> En favori';
        });
    });

    const docId = document.querySelector('.favorite-btn')?.dataset.documentId;
    if (docId) {
        const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        const button = document.querySelector('.favorite-btn');
        if (button && favorites.includes(docId)) {
            button.innerHTML = '<i class="bi bi-heart-fill"></i> En favori';
        }
    }

    const recentlyViewed = JSON.parse(localStorage.getItem('recentlyViewed') || '[]');
    const currentPage = window.location.pathname;
    if (currentPage.includes('/document/')) {
        const match = currentPage.match(/\/document\/(\d+)/);
        if (match) {
            const currentDocId = match[1];
            const updated = [currentDocId, ...recentlyViewed.filter(item => item !== currentDocId)].slice(0, 6);
            localStorage.setItem('recentlyViewed', JSON.stringify(updated));
        }
    }
});
