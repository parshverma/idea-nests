window.onload = function() {
    setTimeout(showDisclaimer, 1000); // Show disclaimer after 1 second delay
};

function showDisclaimer() {
    var disclaimer = document.getElementById('disclaimer');
    disclaimer.style.opacity = 1; // Set opacity to 1 to make it visible
}

function hideDisclaimer() {
    document.getElementById("disclaimer").style.display = "none";
    // Set session variable to indicate that the disclaimer has been seen
    fetch("{% url 'disclaimer_seen' %}", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    });
}

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}