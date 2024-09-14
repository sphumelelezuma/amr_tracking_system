document.addEventListener('DOMContentLoaded', function() {
    const editProfileBtn = document.getElementById('editProfileBtn');
    const profileBio = document.getElementById('profileBio');
    const bioEdit = document.getElementById('bioEdit');
    const choosePicBtn = document.getElementById('choosePicBtn');
    const profilePicForm = document.getElementById('profilePicForm');
    const profilePicInput = document.getElementById('profilePicInput');

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

            // Send an AJAX request to update the bio on the server
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '{% url "update_profile" %}', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');

            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    // Optionally handle success
                    console.log('Bio updated successfully');
                }
            };

            const formData = new FormData();
            formData.append('bio', bioEdit.value.trim());

            xhr.send(new URLSearchParams(formData).toString());
        }
    });

    // Handle profile picture update
    choosePicBtn.addEventListener('click', function() {
        profilePicInput.click();
    });

    profilePicInput.addEventListener('change', function() {
        if (profilePicInput.files.length > 0) {
            const file = profilePicInput.files[0];
            const reader = new FileReader();

            // Update the profile image preview
            reader.onload = function(e) {
                document.getElementById('profileImage').src = e.target.result;
            };

            reader.readAsDataURL(file);

            // Automatically submit the form on file selection
            profilePicForm.submit();
        }
    });
});
