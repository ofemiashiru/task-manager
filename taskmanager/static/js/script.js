document.addEventListener("DOMContentLoaded", function() {
    // sidenav initialization
    let sidenav = document.querySelectorAll(".sidenav");
    M.Sidenav.init(sidenav);
});

let now = new Date()
let year = now.getFullYear()

document.querySelector(".footer-copyright .container").innerHTML = `© ${year} Task Manager`