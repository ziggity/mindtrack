document.addEventListener("DOMContentLoaded", function () {
    const transactionTypeField = document.getElementById("transaction_type");
    const categoryField = document.getElementById("category");

    // Function to load categories
    function loadCategories(transactionType) {
        fetch(`/FinanceManager/get_categories/${transactionType}/`)
            .then(response => response.json())
            .then(data => {
                categoryField.innerHTML = ""; // Clear the current options
                categoryField.appendChild(new Option("Select a category", "", true, true)); // Default placeholder

                // Populate categories dropdown with options
                data.categories.forEach(category => {
                    const option = new Option(category.name, category.id);
                    categoryField.appendChild(option);
                });
            })
            .catch(error => console.error("Error loading categories:", error));
    }

    // Trigger category loading when transaction type changes
    transactionTypeField.addEventListener("change", function () {
        const selectedType = transactionTypeField.value;
        loadCategories(selectedType);
    });

    // Load categories on page load (default transaction type)
    loadCategories(transactionTypeField.value);
    

});
