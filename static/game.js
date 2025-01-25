const target = document.getElementById('target');
const wordDisplay = document.getElementById('word-display');
const wordInput = document.getElementById('word-input');
const scoreElement = document.getElementById('score');
const timeLeftElement = document.getElementById('time-left');
const endMessage = document.getElementById('end-message');
const successList = document.getElementById('success-list');
const gameBox = document.getElementById('game-box');
let score = 0;
let timeLeft = 20; // Game duration in seconds
let currentWord = '';
const words = ['hello', 'world', 'javascript', 'matrix', 'python', 'coding']; // Word list

// Function to randomly choose between button or word game with a 2:1 ratio
function randomChallenge() {
    const randomChoice = Math.random(); // Generate a random number between 0 and 1
    if (randomChoice < 0.67) {
        startButtonChallenge();
    } else {
        startWordChallenge();
    }
}

// Button Challenge Logic
function startButtonChallenge() {
    wordDisplay.style.display = 'none';
    wordInput.style.display = 'none';
    successList.style.display = 'none';
    target.style.display = 'block';

    const boxWidth = gameBox.offsetWidth;
    const boxHeight = gameBox.offsetHeight;
    const x = Math.random() * (boxWidth - 60);
    const y = Math.random() * (boxHeight - 60);

    target.style.left = `${x}px`;
    target.style.top = `${y}px`;

    target.onclick = () => {
        score++;
        scoreElement.textContent = score;
        randomChallenge(); // Switch to another challenge
    };
}

// Word Challenge Logic
function startWordChallenge() {
    target.style.display = 'none';
    wordInput.style.display = 'block';
    wordDisplay.style.display = 'block';
    successList.style.display = 'none';

    currentWord = words[Math.floor(Math.random() * words.length)];
    wordDisplay.textContent = currentWord;
    wordInput.value = '';

    wordInput.oninput = () => {
        if (wordInput.value.toLowerCase() === currentWord.toLowerCase()) {
            score++;
            scoreElement.textContent = score;
            displaySuccessWord(currentWord); // Show the word with a tick
            timeLeft += 5; // Add 5 seconds to the timer
            randomChallenge(); // Switch to another challenge
        }
    };
}

// Display Successful Word with Tick
function displaySuccessWord(word) {
    successList.style.display = 'block';
    const successItem = document.createElement('div');
    successItem.className = 'success-item';
    successItem.innerHTML = `${word} <span class="tick">✔</span>`;
    successList.appendChild(successItem);

    // Remove the success list after 1.5 seconds
    setTimeout(() => {
        successList.style.display = 'none';
        successList.innerHTML = ''; // Clear the list
    }, 1500);
}

// Timer Logic
const timerInterval = setInterval(() => {
    timeLeft--;
    timeLeftElement.textContent = timeLeft;

    if (timeLeft <= 0) {
        clearInterval(timerInterval); // Stop the timer
        target.style.display = 'none';
        wordDisplay.style.display = 'none';
        wordInput.style.display = 'none';
        successList.style.display = 'none';
        showRestartButton();
    }
}, 1000);

// Function to display the restart button
function showRestartButton() {
    const restartButton = document.createElement('button'); // Create button
    restartButton.textContent = 'Test Again'; // Button label
    restartButton.id = 'restart-button'; // Assign an ID for styling
    restartButton.addEventListener('click', () => {
        window.location.reload(); // Reload the page to restart the game
    });
    endMessage.appendChild(restartButton); // Add button below the message
    endMessage.style.display = 'block';
}

// Start the game
randomChallenge();
