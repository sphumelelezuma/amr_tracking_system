document.addEventListener('DOMContentLoaded', function() {
    const editProfileBtn = document.getElementById('editProfileBtn');
    const profileBio = document.getElementById('profileBio');
    const bioEdit = document.getElementById('bioEdit');
    const updatePicBtn = document.getElementById('updatePicBtn');
    const profilePicForm = document.getElementById('profilePicForm');
    const profilePicInput = document.getElementById('profilePicInput');
    const choosePicBtn = document.getElementById('choosePicBtn');

    // Toggle bio edit mode
    editProfileBtn.addEventListener('click', function() {
        if (bioEdit.classList.contains('d-none')) {
            // Enter edit mode
            bioEdit.classList.remove('d-none');
            profileBio.classList.add('d-none');
            bioEdit.value = profileBio.textContent.trim();
            editProfileBtn.textContent = 'Save Changes';
        } else {
            // Save changes
            profileBio.textContent = bioEdit.value.trim();
            bioEdit.classList.add('d-none');
            profileBio.classList.remove('d-none');
            editProfileBtn.textContent = 'Edit Profile';
            // Add logic to save changes to the server here
        }
    });

    // Handle profile picture update
    choosePicBtn.addEventListener('click', function() {
        profilePicInput.click();
    });

    profilePicInput.addEventListener('change', function() {
        profilePicForm.submit(); // Automatically submit the form on file selection
    });
});
