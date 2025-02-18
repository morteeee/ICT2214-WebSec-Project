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
const words = ['hello', 'world', 'java$cript', 'm@trix', 'pyth0n', 'c0d1ng', 'th1si$c0mpl3x']; // Word list


function validate(callback){
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
        // document.getElementById('resultBoard').innerHTML = document.getElementById('resultBoard').innerHTML += `<p>${data['result']}</p>`;

        var tr = `<tr>`;
        tr += `<td style="color: ${parseFloat(data['result']['avg_speed']) < 50 ? 'red' : '#00ff00'}">${parseFloat(data['result']['avg_speed']).toFixed(3)}</td>`;
        tr += `<td style="color: ${parseFloat(data['result']['acceleration']) < 50 ? 'red' : '#00ff00'}">${parseFloat(data['result']['acceleration']).toFixed(3)}</td>`;
        tr += `<td style="color: ${parseFloat(data['result']['jerk']) < 50 ? 'red' : '#00ff00'}">${parseFloat(data['result']['jerk']).toFixed(3)}</td>`;
        tr += `<td style="color: ${parseFloat(data['result']['curvature']) < 50 ? 'red' : '#00ff00'}">${parseFloat(data['result']['curvature']).toFixed(3)}</td>`;
        tr += `<td style="color: ${parseFloat(data['result']['straightness']) < 50 ? 'red' : '#00ff00'}">${parseFloat(data['result']['straightness']).toFixed(3)}</td>`;
        tr += `<td style="color: ${parseFloat(data['result']['jitter']) < 50 ? 'red' : '#00ff00'}">${parseFloat(data['result']['jitter']).toFixed(3)}</td>`;
        tr += `<td style="color: ${parseFloat(data['result']['direction_changes']) < 50 ? 'red' : '#00ff00'}">${parseFloat(data['result']['direction_changes']).toFixed(3)}</td>`;

        document.getElementById('resultBoard').innerHTML += tr;
        

        if(data['success'] == true){
            score++;
            scoreElement.textContent = score;
            callback();
            protectionArm();
        }
        else{
            alert('Fingerprint validation failed. Please try again.');
            protectionArm();
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


// Function to randomly choose between button or word game with a 2:1 ratio
function randomChallenge() {
    const randomChoice = Math.random(); // Generate a random number between 0 and 1
    if (randomChoice < 0.67) {
        startButtonChallenge();
    } else {
        // startWordChallenge();
        startButtonChallenge();
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
        validate(randomChallenge);
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
            validate(function(){
                timeLeft += 5; // Add 5 seconds to the timer
                randomChallenge(); // Switch to another challenge
            })
        }
    };
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
protectionArm();
