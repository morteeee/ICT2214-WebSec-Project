const target = document.getElementById('target');
const wordDisplay = document.getElementById('word-display');
const wordInput = document.getElementById('word-input');
const scoreElement = document.getElementById('score');
const timeLeftElement = document.getElementById('time-left');
const gameBox = document.getElementById('game-box');
const finalResultDiv = document.getElementById('final-result');
const scoreDisplay = document.getElementById('score-display');
const categoryDisplay = document.getElementById('category-display');

let score = 0;
let timeLeft = 10;
let dataInstances = [];

function validate(callback) {
    protectionDisarm();
    var fingerprint = getFingerprint();

    fetch('/validateFingerprint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ fingerprint: fingerprint })
    })
    .then(response => response.json())
    .then(data => {
        let instance = {
            avg_speed: parseFloat(data['result']['avg_speed']),
            acceleration: parseFloat(data['result']['acceleration']),
            jerk: parseFloat(data['result']['jerk']),
            curvature: parseFloat(data['result']['curvature']),
            straightness: parseFloat(data['result']['straightness']),
            jitter: parseFloat(data['result']['jitter']),
            direction_changes: parseFloat(data['result']['direction_changes'])
        };

        dataInstances.push(instance);

        let tr = `<tr>`;
        Object.values(instance).forEach(value => {
            tr += `<td style="color: ${value < 50 ? 'red' : '#00ff00'}">${value.toFixed(3)}</td>`;
        });
        tr += `</tr>`;
        document.getElementById('resultBoard').innerHTML += tr;

        if (timeLeft <= 0) {
            sendDataToBackend();
        }

        if (data['success'] == true) {
            score++;
            scoreElement.textContent = score;
            callback();
            protectionArm();
        } else {
            alert('Fingerprint validation failed. Please try again.');
            protectionArm();
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Function to display final weighted score and category in the middle of the game box
function displayFinalResult(weightedScore, category) {
    // Hide all game elements
    target.style.display = 'none';
    wordDisplay.style.display = 'none';
    wordInput.style.display = 'none';

    // Show final result
    scoreDisplay.innerHTML = `Weighted Score: <strong>${weightedScore}</strong>`;
    categoryDisplay.innerHTML = `Category: <strong>${category}</strong>`;
    finalResultDiv.classList.remove('hidden');
}

// Function to send collected data to Python for weighted scoring
function sendDataToBackend() {
    fetch('/calculateWeightedScore', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instances: dataInstances })
    })
    .then(response => response.json())
    .then(data => {
        //alert(`Weighted Score: ${data.weighted_score} | Category: ${data.category}`);
        displayFinalResult(data.weighted_score, data.category);
    })
    .catch(error => {
        console.error('Error sending data:', error);
    });
}

// Random challenge selection
function randomChallenge() {
    const randomChoice = Math.random();
    if (randomChoice < 0.67) {
        startButtonChallenge();
    } else {
        startButtonChallenge();
    }
}

// Button Challenge Logic
function startButtonChallenge() {
    wordDisplay.style.display = 'none';
    wordInput.style.display = 'none';
    target.style.display = 'block';

    const boxWidth = gameBox.offsetWidth;
    const boxHeight = gameBox.offsetHeight;
    const x = Math.random() * (boxWidth - 60);
    const y = Math.random() * (boxHeight - 60);

    target.style.left = `${x}px`;
    target.style.top = `${y}px`;

    target.onclick = () => {
        validate(randomChallenge);
    };
}

// Timer Logic
const timerInterval = setInterval(() => {
    timeLeft--;
    timeLeftElement.textContent = timeLeft;

    if (timeLeft <= 0) {
        clearInterval(timerInterval);
        target.style.display = 'none';
        wordDisplay.style.display = 'none';
        wordInput.style.display = 'none';
        showRestartButton();
        sendDataToBackend();
    }
}, 1000);

// Function to display the restart button
function showRestartButton() {
    document.getElementById('restart-button').style.display = 'block';
}

// Start the game
randomChallenge();
protectionArm();
