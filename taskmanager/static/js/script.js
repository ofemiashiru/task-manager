document.addEventListener("DOMContentLoaded", function() {
    // sidenav initialization
    let sidenav = document.querySelectorAll(".sidenav");
    M.Sidenav.init(sidenav);

    // modal pop up
    let modal = document.querySelectorAll('.modal');
    M.Modal.init(modal);
});

let now = new Date()
let year = now.getFullYear()

document.querySelector(".footer-copyright .container").innerHTML = `© ${year} Task Manager`