window.onload = function() {
    setTimeout(showDisclaimer, 1000); // Show disclaimer after 1 second delay
};

function showDisclaimer() {
    var disclaimer = document.getElementById('disclaimer');
    disclaimer.style.opacity = 1; // Set opacity to 1 to make it visible
}

function hideDisclaimer() {
    var disclaimer = document.getElementById('disclaimer');
    document.getElementById('disclaimer').style.display = 'none';
}
