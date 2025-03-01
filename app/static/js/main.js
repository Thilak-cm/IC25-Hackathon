async function checkParking() {
    const licensePlate = document.getElementById('license-plate').value;
    const lotName = document.getElementById('lot-name').value;
    const userType = document.getElementById('user-type').value;
    
    const response = await fetch('/check_parking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            license_plate: licensePlate,
            lot_name: lotName,
            user_type: userType,
            time: new Date().toISOString()
        })
    });
    
    const result = await response.json();
    displayResult(result);
}

function displayResult(result) {
    const resultDiv = document.getElementById('result');
    resultDiv.classList.remove('hidden');
    
    if (result.status === 'allowed') {
        resultDiv.innerHTML = `
            <div class="success">
                <h2>✅ Parking Allowed</h2>
                <p>${result.message}</p>
            </div>
        `;
    } else {
        resultDiv.innerHTML = `
            <div class="error">
                <h2>❌ Parking Not Allowed</h2>
                <p>${result.message}</p>
                <div class="alternatives">
                    <h3>Alternative Options:</h3>
                    <ul>
                        ${result.alternatives.map(alt => `<li>${alt}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }
}
