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
const backDrop = document.getElementById('modalBackDrop');
const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];



function openModal(timeClicked, dayClicked) {
  clickedTime = timeClicked;
  newEventModal.style.display = 'block';
  backDrop.style.display = 'block';

  const clickedDate = new Date(dayClicked);

  const [hours, minutes] = timeClicked.split(':');

  clickedDate.setHours(parseInt(hours));
  clickedDate.setMinutes(parseInt(minutes));

  const year = clickedDate.getFullYear();
  const month = ('0' + (clickedDate.getMonth() + 1)).slice(-2);
  const day = ('0' + clickedDate.getDate()).slice(-2);
  const hours24 = ('0' + clickedDate.getHours()).slice(-2);
  const minute = ('0' + clickedDate.getMinutes()).slice(-2);

  const formattedStartDate = `${year}-${month}-${day}T${hours24}:${minute}`;
  const formattedEndDate = `${year}-${month}-${day}T18:30`;
  document.getElementById('startPicker').value = formattedStartDate;
  document.getElementById('endPicker').value = formattedEndDate;
}

function closeModal() {
  newEventModal.style.display = 'none';
  backDrop.style.display = 'none';
  load();
}

function saveEvent() {
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

    const now = new Date();
    now.setSeconds(0, 0);

    for (let i = 7; i < 19; i++) {
      for (let j = 0; j < 2; j++) {
        const timeSlot = document.createElement('div');
        timeSlot.classList.add('time-slot');

        const hours = (i < 10 ? '0' : '') + i;
        const minutes = (j === 0 ? '00' : '30');
        const timeString = `${hours}:${minutes}`;
        timeSlot.innerText = timeString;

        const timeSlotDate = new Date(year, date.getMonth(), selectedDayNumber, i, j === 0 ? 0 : 30);

        if (timeSlotDate <= now) {
          timeSlot.classList.add('past-time');
        } else {
          for (const schedule of schedules) {
            const startShift = new Date(schedule.startshift).toISOString().slice(0, -1);
            const newStartShift = new Date(startShift)
            if (timeSlotDate.getTime() === newStartShift.getTime()) {
              if (schedule.status === 1) {
                timeSlot.classList.add('active');
              }
              else if (schedule.status === 2) {
                timeSlot.classList.add('booked');
              }
            }
          }
        }
        if (!timeSlot.classList.contains('past-time') && !timeSlot.classList.contains('active') && !timeSlot.classList.contains('booked')) {
          timeSlot.addEventListener('click', () => {
            openModal(timeString, selectedMonthDay);
          });
        }
        calendar.appendChild(timeSlot);
      }
    }
  }
}


function loadMonthView(isToday = false) {
  document.getElementById('weekdays').style.display = 'grid';
  const calendar = document.getElementById('calendar');
  calendar.innerHTML = '';
  calendar.style.display = 'grid';
  const dt = new Date();
  const today = new Date(dt.getFullYear(), dt.getMonth(), dt.getDate());

  if ((navDay !== 0 || first_load_month_view !== 0) && isToday !== true) {
    dt.setDate(selectedDayNumber)
    dt.setMonth(dt.getMonth() + navMonth);
  }
  if (isToday) {
    const dt = new Date();
    selectedMonthDay = new Date(dt.getFullYear(), dt.getMonth(), dt.getDate());
  }
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

  // if(dt.getHours() >= 19 || (dt.getHours() = 18 && dt.getMinutes() >= 30))
  // {
    
  // }
  const isPastTime = (dt.getHours() >= 19 || (dt.getHours() === 18 && dt.getMinutes() >= 30)) ;

  for (let i = 1; i <= paddingDays + daysInMonth; i++) {
    const daySquare = document.createElement('div');
    daySquare.classList.add('day');

    const dayString = `${month + 1}/${i - paddingDays}/${year}`;

    if (i > paddingDays) {
      daySquare.innerText = i - paddingDays;
      const currentDate = new Date(year, month, i - paddingDays);
      if (currentDate < today || (isPastTime && currentDate.getDate() === today.getDate())) {
        daySquare.classList.add('past-time');
      }
      else {
        for (const schedule of schedules) {
          const startShift = new Date(schedule.startshift).toISOString().slice(0, -1);
          const newStartShift = new Date(startShift)
          if (currentDate.getFullYear() === newStartShift.getFullYear() && currentDate.getMonth() === newStartShift.getMonth() && currentDate.getDate() === newStartShift.getDate()) {
            if (schedule.status === 1) {
              daySquare.classList.add('active');
            }
            else if (schedule.status === 2) {
              daySquare.classList.add('booked');
            }
          }
        }
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
      navDay = 1
      let newDate = new Date(selectedMonthDay);
      newDate.setDate(newDate.getDate() + navDay);
      const isFirstDayOfMonth = newDate.getDate() === 1;
      const isLastDayOfMonth = newDate.getDate() === new Date(newDate.getFullYear(), newDate.getMonth() + 1, 0).getDate();
      if (isFirstDayOfMonth) {
        navMonth++
      } else if (isLastDayOfMonth) {
        navMonth--
      }
      loadDayView(newDate);
    }
  });
  document.getElementById('backButton').addEventListener('click', () => {
    const currentView = document.getElementById('monthSelect').value;
    if (currentView === 'Month') {
      navMonth--
      loadMonthView(false);
    } else if (currentView === 'Day') {
      navDay = 1
      let newDate = new Date(selectedMonthDay);
      newDate.setDate(newDate.getDate() - navDay);
      const isFirstDayOfMonth = newDate.getDate() === 1;
      const isLastDayOfMonth = newDate.getDate() === new Date(newDate.getFullYear(), newDate.getMonth() + 1, 0).getDate();
      if (isFirstDayOfMonth) {
        navMonth++
      } else if (isLastDayOfMonth) {
        navMonth--
      }
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
}
function load() {
  const monthSelect = document.getElementById('monthSelect');
  const selectedOption = monthSelect.value;
  if (selectedOption === 'Month') {
    loadMonthView(false);
  } else if (selectedOption === 'Day') {
    loadDayView(selectedMonthDay);
  }
}
document.getElementById('monthSelect').addEventListener('change', load);
initButtons();
document.addEventListener('DOMContentLoaded', function () {
  const monthSelect = document.getElementById('monthSelect');
  monthSelect.value = 'Month';
  load();
});
