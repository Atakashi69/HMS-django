const minPriceSlider = document.getElementById("id_min_price");
const maxPriceSlider = document.getElementById("id_max_price");
const minPriceValue = document.getElementById("min-price-value");
minPriceValue.textContent = minPriceSlider.value;
const maxPriceValue = document.getElementById("max-price-value");
maxPriceValue.textContent = maxPriceSlider.value;

minPriceSlider.addEventListener("input", function() {
    minPriceValue.textContent = minPriceSlider.value;
});

maxPriceSlider.addEventListener("input", function() {
    maxPriceValue.textContent = maxPriceSlider.value;
});