document.addEventListener('DOMContentLoaded', () => {
    const hiddenBtns = document.querySelectorAll('.toggle-hidden-btn');

    hiddenBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const flashcardId = btn.getAttribute('data-id');
            fetch(`/flashcard/${flashcardId}/toggle-hidden/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'hidden') {
                        btn.textContent = 'Show';
                    } else {
                        btn.textContent = 'Hide';
                    }
                })
                .catch(err => console.error(err));
        });
    });
});

// Helper para obtener CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



document.addEventListener('DOMContentLoaded', () => {
    // Individual Hide/Unhide
    document.querySelectorAll('.toggle-visibility').forEach(button => {
        button.addEventListener('click', function () {
            const flashcardId = this.dataset.id; // Obtener el ID del flashcard
            const flashcardWrapper = document.getElementById(`flashcard-${flashcardId}`); // Seleccionar el contenedor
            if (flashcardWrapper) {
                if (flashcardWrapper.classList.contains('hidden')) {
                    flashcardWrapper.classList.remove('hidden');
                    this.textContent = 'Hide'; // Cambiar texto del botón a "Hide"
                } else {
                    flashcardWrapper.classList.add('hidden');
                    this.textContent = 'Unhide'; // Cambiar texto del botón a "Unhide"
                }
            }
        });
    });

    // Unhide All
    const unhideAllButton = document.getElementById('unhide-all');
    if (unhideAllButton) {
        unhideAllButton.addEventListener('click', () => {
            document.querySelectorAll('.flashcard-wrapper.hidden').forEach(wrapper => {
                wrapper.classList.remove('hidden'); // Quitar la clase "hidden"
                const toggleButton = wrapper.querySelector('.toggle-visibility');
                if (toggleButton) toggleButton.textContent = 'Hide'; // Cambiar texto del botón a "Hide"
            });
        });
    }
});
