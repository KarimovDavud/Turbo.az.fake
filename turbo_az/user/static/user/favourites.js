/*
{% for car in cars %}
        <div class="card">
            <img src="{{car.front_view_image.url}}" alt="Car Image">
            <div class="badge">{{car.brand}}</div>
            <div class="card-body">
                <h5>{{car.car_models}}</h5>
                <p>{{car.year}}, {{car.engine_capasity}} L, {{car.mileage}} km</p>
                <p>{{car.city}}, bugün 13:29</p>
            </div>
            <div class="card-footer">
                <span class="price">{{car.price}} AZN</span>
                <span class="details"><i class="fas fa-crown"></i></span>
            </div>
        </div>
        {% endfor %}
*/

const cardWrapper = document.querySelector(".card-wrapper")

document.addEventListener("DOMContentLoaded", () => {
    const favouriteCars = JSON.parse(localStorage.getItem("favourites")) ?? []
    renderCards(favouriteCars)
})

const removeFromLocalStorage = (id) => {
    let favouriteCars = JSON.parse(localStorage.getItem("favourites"))
    favouriteCars = favouriteCars.filter(car => +car.id !== id)
    localStorage.setItem("favourites", JSON.stringify(favouriteCars))
    renderCards(favouriteCars)
}

const renderCards = (favouriteCars) => {
    cardWrapper.innerHTML = ""

    favouriteCars.forEach(car => {
        cardWrapper.innerHTML += `
            <div class="card">
            <img src="${car.carImg}" alt="Car Image">
            <div class="badge">${car.carBrand}</div>
            <button class="icon active" onclick="removeFromLocalStorage(${car.id})" id="heart-icon" data-car-id="{{ car.id }}">
                <i class="fas fa-heart"></i>
            </button>
            <div class="card-body">
                <h5>${car.carModel}</h5>
                <p>${car.carInfo}</p>
                <p>${car.carLocation}</p>
            </div>
            <div class="card-footer">
                <span class="price">${car.carPrice}</span>
                <span class="details"><i class="fas fa-crown"></i></span>
            </div>
        </div>
        `
    })
}