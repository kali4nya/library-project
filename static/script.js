function addUserIdToForm(form) {
    let userId = document.getElementById('borrowingUser').value;
    form.user_id.value = userId;  // Set the hidden input field
}