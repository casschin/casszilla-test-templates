var dropdown_selector = document.getElementById('dropdown');
dropdown_selector.addEventListener('change', function(e) {
    document.getElementById('dropdown-selected-value').innerHTML = this.value;
});

var clicked_value = document.getElementById('click');
clicked_value.addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('clicked').innerHTML = 'Yes.';
});

var form = document.getElementById('form');
form.addEventListener('submit', function(e) {
    e.preventDefault();
    document.getElementById('input-value').innerHTML = document.getElementById('input-field').value;
});