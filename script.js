document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM is fully loaded");
    document.getElementById("recipe-form").addEventListener("submit", function (event) {
        event.preventDefault();  // Prevent the form from submitting in the traditional way

        const ingredients = document.getElementById("ingredients").value.trim();

        // Check if ingredients are empty
        if (!ingredients) {
            alert("Please enter some ingredients");
            return;
        }

        const fetchUrl = `http://127.0.0.1:5000/search_recipes?ingredients=${ingredients}`;
        console.log("Fetching from URL:", fetchUrl);  // Log the URL for debugging

        fetch(fetchUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Data received:", data);  // Log the received data
                let resultsDiv = document.getElementById("recipe-results");
                resultsDiv.innerHTML = "";  // Clear previous results

                if (data.length === 0) {
                    resultsDiv.innerHTML = "<p>No recipes found</p>";
                } else {
                    data.forEach(recipe => {
                        resultsDiv.innerHTML += `
                            <div class="recipe">
                                <h3>${recipe.title}</h3>
                                <img src="${recipe.image}" alt="${recipe.title}">
                                <p><strong>Missed Ingredients:</strong> ${recipe.missedIngredientCount}</p>
                                <a href="https://spoonacular.com/recipes/${recipe.title}-${recipe.id}" target="_blank">View Recipe</a>
                            </div>
                            <hr>`;
                    });
                }
            })
            .catch(error => {
                console.error("Error:", error);
                let resultsDiv = document.getElementById("recipe-results");
                resultsDiv.innerHTML = "<p>Failed to fetch recipes. Please try again later.</p>";
            });
    });
});
