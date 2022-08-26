let userInfoCard = document.querySelector('.user-info');
let userDescription = document.querySelector('.user-description-container');
let certificateContainer = document.querySelector('.certificate-container');
let editProfileBtn = document.querySelector('.edit-profile-btn');
let profileForm = document.querySelector('.profile-edit-form');
let isEditing = false;

console.log(editProfileBtn.innerHTML);

function hide(elements) { 
    elements.forEach(ele => {
        ele.classList.add('hidden');
    });
}

function open(elements) {
    elements.forEach(ele => {
        ele.classList.remove('hidden')
    });
}

editProfileBtn.addEventListener('click', () => {
    console.log('Hi there')
    if(!isEditing) {
        isEditing = !isEditing;
        editProfileBtn.innerHTML = 'Go back';
        hide([ userInfoCard, userDescription, certificateContainer ]);
        open([profileForm]);
    } else {
        isEditing = !isEditing;
        editProfileBtn.innerHTML = 'Edit Profile';
        open([ userInfoCard, userDescription, certificateContainer ])
        hide([profileForm]);
    }
})

followingBtn.addEventListener('click', () => {
    if(!isEditing) {
        isEditing = !isEditing;
        hide([ profileForm ]);
        open([followers]);
    } else {
        isEditing = !isEditing;
        // open([ userInfoCard, userDescription, certificateContainer ])
        hide([followers]);
    }
})