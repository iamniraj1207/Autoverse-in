let currentQuestionIndex = 0;
let score = 0;
let totalXpEarned = 0;

async function submitAnswer(btn, answer, questionId) {
    const card = btn.closest('.question-card');
    const options = card.querySelectorAll('.option-btn');

    // Disable all options
    options.forEach(b => b.disabled = true);

    const res = await fetch('/api/academy/answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question_id: questionId, answer: answer })
    });

    const data = await res.json();

    const explanationBox = document.getElementById(`explanation-${questionId}`);
    const explanationText = explanationBox.querySelector('.explanation-text');

    if (data.correct) {
        btn.classList.add('correct');
        score++;
        totalXpEarned += data.xp_earned;
        showXpPopup(data.xp_earned);
        explanationText.innerHTML = `<strong style="color: #2ecc71">CORRECT!</strong><br>${data.explanation}`;
    } else {
        btn.classList.add('wrong');
        // Highlight correct answer
        options.forEach(b => {
            if (b.innerText === data.correct_answer) b.classList.add('correct');
        });
        explanationText.innerHTML = `<strong style="color: #e74c3c">INCORRECT</strong><br>${data.explanation}`;
    }

    explanationBox.style.display = 'block';

    // Update progress
    const total = parseInt(card.dataset.total);
    const progressFill = document.getElementById('quiz-progress-fill');
    progressFill.style.width = `${((currentQuestionIndex + 1) / total) * 100}%`;
}

function showXpPopup(xp) {
    const popup = document.getElementById('global-xp-popup');
    popup.innerText = `+${xp} XP`;
    popup.classList.add('visible');
    setTimeout(() => {
        popup.classList.remove('visible');
    }, 1500);
}

async function nextQuestion() {
    const cards = document.querySelectorAll('.question-card');
    cards[currentQuestionIndex].classList.remove('active');

    currentQuestionIndex++;

    if (currentQuestionIndex < cards.length) {
        cards[currentQuestionIndex].classList.add('active');
    } else {
        showResults();
    }
}

async function showResults() {
    document.getElementById('quiz-results').style.display = 'block';
    document.getElementById('res-score').innerText = `${score}/${currentQuestionIndex}`;
    document.getElementById('res-xp').innerText = totalXpEarned;

    // Mark lesson complete
    await fetch('/api/academy/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lesson_id: LESSON_ID, score: score })
    });
}
