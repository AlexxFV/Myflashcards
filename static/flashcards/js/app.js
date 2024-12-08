document.addEventListener('DOMContentLoaded', () => {
    const flashcards = document.querySelectorAll('.flashcard');

    flashcards.forEach(flashcard => {
        const inner = flashcard.querySelector('.flashcard-inner');
        const showAnswerBtn = flashcard.querySelector('.flashcard-front .flip-btn');
        const hideAnswerBtn = flashcard.querySelector('.flashcard-back .flip-btn');

        showAnswerBtn.addEventListener('click', () => {
            inner.classList.add('flipped');
        });

        hideAnswerBtn.addEventListener('click', () => {
            inner.classList.remove('flipped');
        });
    });
});



