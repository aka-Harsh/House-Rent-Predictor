document.addEventListener('DOMContentLoaded', function() {
    const citySelect = document.getElementById('city');
    const areaSelect = document.getElementById('area');
    const predictButton = document.getElementById('predict');
    const resultsDiv = document.getElementById('results');
    const predictedRentP = document.getElementById('predicted-rent');
    const recommendationsList = document.getElementById('recommendations');
    const themeSwitch = document.getElementById('theme-switch');

    citySelect.addEventListener('change', function() {
        fetch('/get_areas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({city: this.value}),
        })
        .then(response => response.json())
        .then(areas => {
            areaSelect.innerHTML = '<option value="">Select an area</option>';
            areas.forEach(area => {
                const option = document.createElement('option');
                option.value = area;
                option.textContent = area;
                areaSelect.appendChild(option);
            });
        });
    });

    predictButton.addEventListener('click', function() {
        const city = citySelect.value;
        const area = areaSelect.value;
        const rooms = document.getElementById('rooms').value;
        const bathrooms = document.getElementById('bathrooms').value;
        const budget = document.getElementById('budget').value;

        if (!city || !area || !rooms || !bathrooms || !budget) {
            alert('Please fill in all fields');
            return;
        }

        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({city, area, rooms, bathrooms, budget}),
        })
        .then(response => response.json())
        .then(data => {
            predictedRentP.textContent = `Estimated Rent: ₹${data.predicted_rent.toFixed(2)}`;
            recommendationsList.innerHTML = '';
            data.recommendations.forEach(rec => {
                const li = document.createElement('li');
                li.textContent = `Area: ${rec.area}, Rooms: ${rec.rooms}, Bathrooms: ${rec.bathroom}, Rent: ₹${rec.total_rent}`;
                recommendationsList.appendChild(li);
            });
            resultsDiv.classList.remove('hidden');
        });
    });

    themeSwitch.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        const icon = this.querySelector('i');
        if (icon.classList.contains('fa-sun')) {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        } else {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    });
});