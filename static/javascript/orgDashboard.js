let prevEventsCards = document.querySelectorAll('.p-event-card-el');
let popUpContainer = document.querySelector('.pop-up-container');
let downloadReportBtn = document.querySelectorAll('.download-report-btn');
let userContainer = document.querySelectorAll('.single-user-container');
let eventInfoPopup = document.querySelector('.event-info-container');
let userInfoClose = document.querySelector('.userPuClose');
let userInfoPopup = document.querySelector('.user-info-popup-container');
let backToEventInfo = document.querySelector('.backToEventInfo');
let reportPuClose = document.querySelector('.reportPuClose');
let reportPopup = document.querySelector('.report-popup-container');

function close(ele) {
    ele.style.display = 'none';
}

function open(ele) {
    ele.style.display = 'flex';
}

close(popUpContainer);

popUpContainer.addEventListener('click', (e) => {
    if(e.path.length == 5) {
        close(popUpContainer);
    }
})

prevEventsCards.forEach(card => {
    card.addEventListener('click', (e) => {
        open(popUpContainer);
        open(eventInfoPopup);
        close(userInfoPopup);
        close(reportPopup);
        var eventId = card.getAttribute('value');
        
    })
});

userContainer.forEach(user => {
    user.addEventListener('click', () => {
        close(eventInfoPopup);
        userInfoPopup.style.display = 'flex';
    })
})

window.addEventListener('keydown', (e) => {

    if(e.key == 'Escape') { 
        close(popUpContainer);
    };
})

downloadReportBtn.forEach(btn => {
    btn.addEventListener('click', (e) => {
        close(popUpContainer)
        open(popUpContainer);
        reportPopup.style.display = 'flex';
        close(userInfoPopup);
        e.stopPropagation();
        document.getElementById("download_report").value =btn.value
    })
});

userInfoClose.addEventListener('click', () => {
    close(popUpContainer);
});

backToEventInfo.addEventListener('click', () => {
    close(userInfoPopup);
    eventInfoPopup.style.display = 'flex';
});

reportPuClose.addEventListener('click', () => {
    close(popUpContainer);
});