(function() { //IIFE
'use strict';

const target = document.getElementById('target');
const scoreElement = document.getElementById('score');
const timeLeftElement = document.getElementById('time-left');
const gameBox = document.getElementById('game-box');
const finalResultDiv = document.getElementById('final-result');
const scoreDisplay = document.getElementById('score-display');
const categoryDisplay = document.getElementById('category-display');

let score = 0;
let timeLeft = 20;
let dataInstances = [];



function buf2hex(buffer) {
    return Array.from(new Uint8Array(buffer))
           .map(b => b.toString(16).padStart(2, '0'))
           .join('');
}
  
function hex2buf(hex) {
    const bytes = new Uint8Array(hex.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));
    return bytes.buffer;
}
  
async function importRsaPublicKey(pem, algoName = "RSA-OAEP") {
    const pemHeader = "-----BEGIN PUBLIC KEY-----";
    const pemFooter = "-----END PUBLIC KEY-----";
    const pemContents = pem
        .replace(pemHeader, "")
        .replace(pemFooter, "")
        .replace(/\n/g, '')
        .trim();
    const binaryDerString = window.atob(pemContents);
    const binaryDer = new Uint8Array([...binaryDerString].map(char => char.charCodeAt(0)));
    return window.crypto.subtle.importKey(
        "spki",
        binaryDer.buffer,
        {
            name: algoName,
            hash: "SHA-256"
        },
        true,
        ["encrypt"]
    );
}
  
async function encryptPayload(payload) {
    const response = await fetch('/getPublicKey');
    const jsonData = await response.json();
    const pemKey = jsonData.public_key;
    const publicKey = await importRsaPublicKey(pemKey);
    
    const aesKey = await window.crypto.subtle.generateKey(
        { name: "AES-GCM", length: 256 },
        true,
        ["encrypt", "decrypt"]
    );
    
    const encoder = new TextEncoder();
    const encodedPayload = encoder.encode(JSON.stringify(payload));
    
    const nonce = window.crypto.getRandomValues(new Uint8Array(12));
    
    const encryptedBuffer = await window.crypto.subtle.encrypt(
        { name: "AES-GCM", iv: nonce },
        aesKey,
        encodedPayload
    );
    const encryptedBytes = new Uint8Array(encryptedBuffer);
    const tagLength = 16;
    const ciphertextBytes = encryptedBytes.slice(0, encryptedBytes.length - tagLength);
    const tagBytes = encryptedBytes.slice(encryptedBytes.length - tagLength);
  
    const rawAesKey = await window.crypto.subtle.exportKey("raw", aesKey);
    
    const encryptedAesKeyBuffer = await window.crypto.subtle.encrypt(
        { name: "RSA-OAEP" },
        publicKey,
        rawAesKey
    );
    
    return {
        encrypted_key: buf2hex(encryptedAesKeyBuffer),
        ciphertext: buf2hex(ciphertextBytes.buffer),
        nonce: buf2hex(nonce.buffer),
        tag: buf2hex(tagBytes.buffer)
    };
}



async function validate() {
    protectionDisarm();
    var fingerprint = getFingerprint();
    const payload = { fingerprint: fingerprint };

    try {
        const encryptedData = await encryptPayload(payload);
        fetch('/validateFingerprint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(encryptedData)
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

            let tr = document.createElement('tr');
            Object.keys(instance).forEach(key => {
                let td = document.createElement('td');
                td.textContent = instance[key].toFixed(3);
                td.style.color = instance[key] < 50 ? 'red' : '#00ff00';
                tr.appendChild(td);
            });

            let resultTable = document.getElementById('resultBoard');
            resultTable.appendChild(tr);

            if (timeLeft <= 0) {
                sendDataToBackend();
            }

            if (data['success'] == true) {
                score++;
                scoreElement.textContent = score;
                startButtonChallenge();
                protectionArm();
            } else {
                alert('Fingerprint validation failed. Please try again.');
                protectionArm();
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    } catch (error) {
        console.error("Encryption error:", error);
        protectionArm();
    }
}

// Function to display final weighted score and category in the middle of the game box
function displayFinalResult(weightedScore, category) {
    // Hide all game elements
    target.style.display = 'none';

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

// Button Challenge Logic
function startButtonChallenge() {
    target.style.display = 'block';

    const boxWidth = gameBox.offsetWidth;
    const boxHeight = gameBox.offsetHeight;
    const x = Math.random() * (boxWidth - 60);
    const y = Math.random() * (boxHeight - 60);

    target.style.left = `${x}px`;
    target.style.top = `${y}px`;

    target.onclick = () => {
        validate();
    };
}

// Timer Logic
const timerInterval = setInterval(() => {
    timeLeft--;
    timeLeftElement.textContent = timeLeft;

    if (timeLeft <= 0) {
        clearInterval(timerInterval);
        target.style.display = 'none';
        sendDataToBackend();
    }
}, 1000);

// Start the game
startButtonChallenge();
protectionArm();

})();