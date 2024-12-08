// Function to toggle the visibility of the answer in flashcards
function toggleAnswer(button) {
    const answer = button.previousElementSibling.querySelector('.flashcard-answer');
    if (answer) {
        answer.classList.toggle('show');
        button.textContent = answer.classList.contains('show') ? 'Hide Answer' : 'Show Answer';
    }
}

// Add event listener to all flashcards for toggling the answer
document.addEventListener('DOMContentLoaded', () => {
    const flipButtons = document.querySelectorAll('.flip-btn');
    flipButtons.forEach(button => {
        button.addEventListener('click', () => toggleAnswer(button));
    });
});
