document.addEventListener('DOMContentLoaded', function( ) {
    document.querySelector('index').addEventListener('click', () => add_transactions());
});


function add_transactions(event) {
    event.preventDefault();

    // Get form data
    let category = document.getSelection('#category').value;
    let amount = document.querySelector('#amount').value;
    let desciption = document.querySelector('#description').value;

    // Fect a POST request
    fetch('/', {
        method: 'POST ',
        headers: {
            'content-Type': 'applications/json'
        },
        body: JSON.stringify({
            category: category,
            amount: amount,
            desciption: desciption
        })
    })
    .then(response => response.json())
    .then(result => {
        
    })
}