(function() { // IIFE
    'use strict';
  
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
        lastMouseX = e.clientX;
        lastMouseY = e.clientY;
    });
  
    document.addEventListener("keydown", function(e) {
        sensorData += `key-${e.key};`;
    });
  
    document.addEventListener("scroll", function() {
        if (!isScrolling) {
            scrollStartX = window.scrollX;
            scrollStartY = window.scrollY;
            sensorData += `scroll-start-${scrollStartX}-${scrollStartY};`;
        }
  
        window.clearTimeout(isScrolling);
  
        isScrolling = setTimeout(function() {
            sensorData += `scroll-end-${window.scrollX}-${window.scrollY};`;
        }, 100);
    });
  
    document.addEventListener("click", function(e) {
        sensorData += `click-${e.clientX}-${e.clientY};`;
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
        asdfingerprintinterval = setInterval(leEngine, 10);
    }
  
    function protectionDisarm(){
        clearInterval(asdfingerprintinterval);
    }
  
    function getFingerprint(){
        console.log(asdfingerprint);
        return asdfingerprint;
    }
  
    // Expose the functions that need to be accessible globally.
    window.protectionArm = protectionArm;
    window.protectionDisarm = protectionDisarm;
    window.getFingerprint = getFingerprint;
  
})(); 