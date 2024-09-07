document.getElementById('priceForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData(document.getElementById('priceForm'));
    for (const [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
    }
    let data = {
        'bhk': formData.get('bhk'),
        'size': formData.get('size'),
        'floor': formData.get('floor'),
        'area_type': formData.get('area_type'),
        'area_location': formData.get('area_location'),
        'city': formData.get('city'),
        'furnishing_status': formData.get('furnishing_status'),
        'tenant_preferred': formData.get('tenant_preferred'),
        'bathroom': formData.get('bathroom'),
        'point_of_contact': formData.get('point_of_contact')
    };

    fetch('http://127.0.0.1:5000/predict_home_price', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams(data)
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById('result').textContent = 'Estimated Price: ₹' + result.estimated_price.toFixed(2);
    })
    .catch(error => console.error('Error:', error));
});
