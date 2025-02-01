var lastMouseX = 0;
var lastMouseY = 0;
var prevMouseX = 0;
var prevMouseY = 0;
var sensorData = ``;
var asdfingerprint = {};
var asdfingerprintinterval = null;
var startTimeCT = Date.now();
var isScrolling;
var scrollStartX, scrollStartY;

document.addEventListener("mousemove", function(e) {
    var event = e;
    lastMouseX = event.clientX;
    lastMouseY = event.clientY;
});

document.addEventListener("keydown", function(e) {
    var keyPressed = e.key;
    sensorData += `key-${keyPressed};`;
});

document.addEventListener("scroll", function() {
    if (!isScrolling) {
        scrollStartX = window.scrollX;
        scrollStartY = window.scrollY;
        sensorData += `scroll-start-${scrollStartX}-${scrollStartY};`;
    }

    window.clearTimeout(isScrolling);

    isScrolling = setTimeout(function() {
        var scrollEndX = window.scrollX;
        var scrollEndY = window.scrollY;
        sensorData += `scroll-end-${scrollEndX}-${scrollEndY};`;
    }, 100);
});

document.addEventListener("click", function(e) {
    var clickX = e.clientX;
    var clickY = e.clientY;
    sensorData += `click-${clickX}-${clickY};`;
});

function leEngine(){
    var viewportWidth = window.innerWidth;
    var viewportHeight = window.innerHeight;
    if (lastMouseX !== prevMouseX || lastMouseY !== prevMouseY) {
        var mousePath = `${lastMouseX}-${lastMouseY}`;
        sensorData += `${mousePath};`;
        prevMouseX = lastMouseX;
        prevMouseY = lastMouseY;
    }
    
    if (sensorData.length > 3000) {
        sensorData = sensorData.substring(sensorData.length - 3000);
    }

    asdfingerprint = {
        sensorData: sensorData,
        viewportWidth: viewportWidth,
        viewportHeight: viewportHeight,
        userAgent: navigator.userAgent,
        language: navigator.language,
        platform: navigator.platform,
        webdriver: navigator.webdriver,
        screenResolution: screen.width + "x" + screen.height,
        colorDepth: screen.colorDepth,
        plugins: navigator.plugins.length,
        mimeTypes: navigator.mimeTypes.length,
        timezoneOffset: new Date().getTimezoneOffset(),
        touchSupport: 'ontouchstart' in window || navigator.maxTouchPoints > 0,
        deviceMemory: navigator.deviceMemory || 'unknown',
        hardwareConcurrency: navigator.hardwareConcurrency || 'unknown',
        doNotTrack: navigator.doNotTrack
    };
}

function protectionArm(){
    asdfingerprint = {};
    sensorData = ``;
    asdfingerprintinterval = setInterval(leEngine, 150);
}

function protectionDisarm(){
    clearInterval(asdfingerprintinterval);
}

function getFingerprint(){
    console.log(asdfingerprint);
    return asdfingerprint;
}