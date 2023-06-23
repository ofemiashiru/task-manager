const now = new Date();
const year = now.getFullYear();

// Used to help https://stackoverflow.com/questions/33070428/add-a-year-to-todays-date
const yearFromNow = new Date();
yearFromNow.setFullYear(yearFromNow.getFullYear() + 1);

document.querySelector(".footer-copyright .container").innerHTML = `© ${year} Task Manager`;


document.addEventListener("DOMContentLoaded", function () {
    // sidenav initialization
    let sidenav = document.querySelectorAll(".sidenav");
    M.Sidenav.init(sidenav);

    // modal pop up
    let modal = document.querySelectorAll('.modal');
    M.Modal.init(modal);

    // date picker
    let datePicker = document.querySelectorAll(".datepicker");
    M.Datepicker.init(datePicker, {
        format: "dd mmm, yyyy",
        minDate: now,
        maxDate: yearFromNow,
        yearRange: [year, year + 1],
        i18n: {
            done: "Select"
        }
    });

    // drop down
    let selects = document.querySelectorAll("select");
    M.FormSelect.init(selects);
});
