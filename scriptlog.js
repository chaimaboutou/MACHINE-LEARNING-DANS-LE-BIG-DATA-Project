let logTimeout;  // Store timeout ID to prevent multiple log requests

// Function to get the current date and time in the format YYYY-MM-DD HH:MM:SS
function getCurrentDateTime() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0'); // Add seconds
    return `${year}/${month}/${day} ${hours}:${minutes}:${seconds}`;
}


function logMessage(message) {
    clearTimeout(logTimeout);
    logTimeout = setTimeout(() => {
        const dateTime = getCurrentDateTime();
        console.log(`${dateTime} | ${message}`);
        fetch('http://localhost:3000/save-log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                timestamp: dateTime,
                message: message,
            }),
        }).catch((error) => console.error('Error logging message:', error));
    }, 1000);
}



// Log click events on specific links
document.addEventListener('click', function (event) {
    if (event.target.innerText === 'About') {
        logMessage('Clicked About link');
    }
    if (event.target.innerText === 'Products') {
        logMessage('Clicked Products link');
    }
    if (event.target.innerText === 'Contact') {
        logMessage('Clicked Contact link');
    }
});


function logHover(event) {
    const productName = event.target.getAttribute('data-name');
    logMessage(`Hovered over | ${productName} | 1`);
}


function logHoverSection(event) {
    logMessage(`Hovered over | ${event.target.id} | 1`);
}


const sections = ["women-section", "men-section", "boys-section", "girls-section"];
sections.forEach(sectionId => {
    const sectionElement = document.getElementById(sectionId);
    if (sectionElement) {
        sectionElement.addEventListener("mouseenter", logHoverSection);
    }
});


const products = [
    "women_product_1", "women_product_2", "women_product_3",
    "men_product_1", "men_product_2", "men_product_3",
    "boy_product_1", "boy_product_2", "boy_product_3",
    "girls_product_1", "girls_product_2", "girls_product_3"
];

products.forEach(productId => {
    const productElement = document.getElementById(productId);
    if (productElement) {
        productElement.addEventListener("mouseenter", logHover);
    }
});


function logPurchase(productName, price) {
    logMessage(`Product purchased | ${productName} | 1 | ${price}`);
}
