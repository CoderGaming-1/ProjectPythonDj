let navMonth = 0;
let navDay = 0;
let first_load_month_view = 0;
let clicked = new Date();
let selectedMonthDay = new Date();
let selectedDayNumber = 0;

let clickedTime = null;
let events = localStorage.getItem('events') ? JSON.parse(localStorage.getItem('events')) : [];

const calendar = document.getElementById('calendar');
const newEventModal = document.getElementById('newEventModal');
const deleteEventModal = document.getElementById('deleteEventModal');
const backDrop = document.getElementById('modalBackDrop');
// const eventTitleInput = document.getElementById('eventTitleInput');
const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];


function openModal(timeClicked) {
  clickedTime = timeClicked;

  const eventForDay = events.find(e => e.date === clicked);

  if (eventForDay) {
    document.getElementById('eventText').innerText = eventForDay.title;
    deleteEventModal.style.display = 'block';
  } else {
    newEventModal.style.display = 'block';
  }

  backDrop.style.display = 'block';
}
function closeModal() {
  // eventTitleInput.classList.remove('error');
  newEventModal.style.display = 'none';
  deleteEventModal.style.display = 'none';
  backDrop.style.display = 'none';
  // eventTitleInput.value = '';
  clicked = null;
  load();
}

function saveEvent() {
  // if (eventTitleInput.value) {
  //   eventTitleInput.classList.remove('error');

  //   events.push({
  //     date: clicked,
  //     title: eventTitleInput.value,
  //   });

  //   localStorage.setItem('events', JSON.stringify(events));
    closeModal();
  // } else {
  //   eventTitleInput.classList.add('error');
  // }
}

function deleteEvent() {
  events = events.filter(e => e.date !== clicked);
  localStorage.setItem('events', JSON.stringify(events));
  closeModal();
}
function loadDayView(date) {
  const calendar = document.getElementById('calendar');
  calendar.innerHTML = '';
  calendar.style.display = 'flex';
  calendar.style.flexDirection = 'column';

  if (date) {

    const year = date.getFullYear();
    const newDate = new Date(date);
    newDate.setDate(newDate.getDate());
    
    selectedMonthDay = newDate;
    selectedDayNumber = newDate.getDate();
    document.getElementById('monthDisplay').innerText =
      `${newDate.toLocaleDateString('en-us', { month: 'long', day: 'numeric' })}, ${year}`;

    for (let i = 7; i <= 19; i++) {
      for (let j = 0; j < 2; j++) {
        const timeSlot = document.createElement('div');
        timeSlot.classList.add('time-slot');
        let timeString = '';
        if (i < 12) {
          timeString = `${i}:${j === 0 ? '00' : '30'} AM`;
        } else if (i === 12) {
          timeString = `${i}:${j === 0 ? '00' : '30'} PM`;
        } else {
          timeString = `${i - 12}:${j === 0 ? '00' : '30'} PM`;
        }
        timeSlot.innerText = timeString;
        const timeSlotDate = new Date(year, date.getMonth(), selectedDayNumber, i + (j === 0 ? 0 : 0.5));
        if (timeSlotDate < new Date()) {
          timeSlot.classList.add('past-time');
        }
        timeSlot.addEventListener('click', () => {
          console.log(`Bạn đã nhấn vào khung giờ ${timeString} ngày ${selectedMonthDay}`);
          openModal(timeString);
        });
        calendar.appendChild(timeSlot);
      }
    }
  }
}


function loadMonthView(isToday=false) {
  document.getElementById('weekdays').style.display = 'grid';
  const calendar = document.getElementById('calendar');
  calendar.innerHTML = '';
  calendar.style.display = 'grid';
  const dt = new Date();
  const today = new Date(dt.getFullYear(), dt.getMonth(), dt.getDate());

  if ((first_load_month_view !== 0) && isToday !== true) {
    dt.setDate(selectedDayNumber)
    dt.setMonth(dt.getMonth() + navMonth);
  }
  if (isToday) {
    const dt = new Date();
    selectedMonthDay = new Date(dt.getFullYear(), dt.getMonth(), dt.getDate());
  }
  // console.log('Month viewwwwwwwwww: ' + dt);
  clicked = dt

  const day = dt.getDate();
  const month = dt.getMonth();
  const year = dt.getFullYear();

  const firstDayOfMonth = new Date(year, month, 1);
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const dateString = firstDayOfMonth.toLocaleDateString('en-us', {
    weekday: 'long',
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
  });
  const paddingDays = weekdays.indexOf(dateString.split(', ')[0]);

  document.getElementById('monthDisplay').innerText =
    `${dt.toLocaleDateString('en-us', { month: 'long', day: 'numeric' })}, ${year}`;

  calendar.innerHTML = '';
  selectedDayNumber = day;
  selectedMonthDay = clicked || day;
  
  if (clicked && clicked.getMonth() === month) {
    selectedMonthDay = new Date(clicked);
  } 
  else {
    selectedMonthDay = new Date(year, month, selectedDayNumber);
  }
  // console.log('heaaarrrrrrrrr: '+ selectedMonthDay);
  for (let i = 1; i <= paddingDays + daysInMonth; i++) {
    const daySquare = document.createElement('div');
    daySquare.classList.add('day');

    const dayString = `${month + 1}/${i - paddingDays}/${year}`;

    if (i > paddingDays) {
      daySquare.innerText = i - paddingDays;
      const currentDate = new Date(year, month, i - paddingDays);
      if (currentDate < today) {
        daySquare.classList.add('past-time');
      }
      if (i - paddingDays === selectedMonthDay.getDate()) {
        daySquare.classList.add('selected');
      }
      daySquare.addEventListener('click', () => {
        const selectedDate = new Date(year, month, i - paddingDays);
        selectedMonthDay = new Date(selectedDate);
        document.getElementById('monthDisplay').innerText =
          `${selectedDate.toLocaleDateString('en-us', { month: 'long', day: 'numeric' })}, ${year}`;
        document.getElementById('weekdays').style.display = 'none';
        document.getElementById('monthSelect').value = 'Day';
        loadDayView(selectedDate);
      });
    } else {
      daySquare.classList.add('padding');
    }
    calendar.appendChild(daySquare);
    first_load_month_view = 1
    
  }
}

function initButtons() {
  document.getElementById('nextButton').addEventListener('click', () => {
    const currentView = document.getElementById('monthSelect').value;
    if (currentView === 'Month') {
      navMonth++
      loadMonthView(false);
    } else if (currentView === 'Day') {
      navDay=1
      let newDate = new Date(selectedMonthDay);
      newDate.setDate(newDate.getDate() + navDay);
      loadDayView(newDate);
    }
  });
  document.getElementById('backButton').addEventListener('click', () => {
    const currentView = document.getElementById('monthSelect').value;
    if (currentView === 'Month') {
      navMonth--
      loadMonthView(false);
    } else if (currentView === 'Day') {
      navDay=1
      let newDate = new Date(selectedMonthDay);
      newDate.setDate(newDate.getDate() - navDay);
      loadDayView(newDate);
    }
  });
  document.getElementById('todayButton').addEventListener('click', () => {
    const currentView = document.getElementById('monthSelect').value;
    const dt = new Date();
    const today = new Date(dt.getFullYear(), dt.getMonth(), dt.getDate());
    selectedMonthDay = today;
    selectedDayNumber = today.getDate();
    navMonth = 0
    if (currentView === 'Month') {  
      loadMonthView(true);
    } else if (currentView === 'Day') {
      loadDayView(today);
    }
  });
  document.getElementById('saveButton').addEventListener('click', saveEvent);
  document.getElementById('cancelButton').addEventListener('click', closeModal);
  document.getElementById('deleteButton').addEventListener('click', deleteEvent);
  document.getElementById('closeButton').addEventListener('click', closeModal);

}
function load() {
  const monthSelect = document.getElementById('monthSelect');
  monthSelect.addEventListener('change', function () {
    const selectedOption = this.value;
    if (selectedOption === 'Month') {
      loadMonthView(false);
    } else if (selectedOption === 'Day') {
      loadDayView(selectedMonthDay);
    }           
  });
  loadMonthView(false);
}
initButtons();
document.addEventListener('DOMContentLoaded', function () {
  const monthSelect = document.getElementById('monthSelect');
  monthSelect.value = 'Month';
  load();
});
