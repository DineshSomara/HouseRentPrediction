document.getElementById('priceForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData(document.getElementById('priceForm'));
    for (const [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
    }
    let floor1 = formData.get('floor1');
    let floor2 = formData.get('floor2');
    console.log(floor1);
    console.log(floor2);
    floor1 = parseFloat(floor1);
    floor2 = parseFloat(floor2);

    let floorRatio = parseFloat(floor1 / floor2).toFixed(6);
    console.log(floorRatio)

    let data = {
        'bhk': formData.get('bhk'),
        'size': formData.get('size'),
        'floor': floorRatio,
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
const locationList = document.getElementById("area_location");
fetch('./columns.json')
    .then((res)=>res.json())
    .then((json)=>{
        json.data_columns.forEach((element, index) => {
            if (index >= 10) {
              const option = document.createElement('option');
              option.textContent = element;
              locationList.appendChild(option);
            }
          });
    })

const tenantPreferred = ['Bachelors/Family', 'Bachelors', 'Family'];
const POC = ['Contact Owner', 'Contact Agent', 'Contact Builder'];
const areaType = ['Super Area','Carpet Area', 'Built Area'];
const city = ['Kolkata', 'Mumbai', 'Bangalore' ,'Delhi', 'Chennai', 'Hyderabad'];
const furnishedStatus = ['Unfurnished', 'Semi-Furnished', 'Furnished'];
function createDropdown(dropdownID, data) {
    const dropdownElement = document.getElementById(dropdownID);
    data.forEach(item => {
      const optionElement = document.createElement('option');
      optionElement.textContent = item;
      dropdownElement.appendChild(optionElement);   
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    createDropdown('tenant_preferred', tenantPreferred);
    createDropdown('point_of_contact', POC);
    createDropdown('area_type', areaType);
    createDropdown('city', city);
    createDropdown('furnishing_status', furnishedStatus);
});
