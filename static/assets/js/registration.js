let signup=document.querySelector('#signup');
let login=document.querySelector('#login');

function toggleTab(tab) {
    if (tab === 'login') {
        login.style.display = 'block';
        signup.style.display = 'none';
    } else if (tab === 'signup') {
        login.style.display = 'none';
        signup.style.display = 'block';
    }
}
let navLinks = document.querySelectorAll(".sidebar-list .sidebar-list-item")
let app_orders=document.getElementById("app-orders");
let app_Statistics=document.getElementById("app-Statistics");
let app_Home=document.getElementById("app-Home");
let app_address=document.getElementById("app-address");

navLinks.forEach(link => {
    link.addEventListener("click", function () {
        navLinks.forEach(navLink => {
            navLink.classList.remove("active");
        });

        link.classList.add("active");
    });
});

function sort_home() {
    hideProjects();
    showProjectsByCategory("app_home");
}

function sort_orders() {
    hideProjects();
    showProjectsByCategory("app_orders");
}
function sort_stats() {
    hideProjects();
    showProjectsByCategory("app_stats");
}
function sort_address() {
    hideProjects();
    showProjectsByCategory("app_address");
}
function sort_notify() {
    hideProjects();
    showProjectsByCategory("app_notify");
}

// Function to hide all projects
function hideProjects() {
    var projects = document.querySelectorAll('.app-content .products-area-wrapper');
    projects.forEach(function (project) {
        project.style.display = 'none';
    });
}

// Function to show projects by category
function showProjectsByCategory(category) {
    var projects = document.querySelectorAll('.app-content .products-area-wrapper');
    projects.forEach(function (project) {
        var projectCategory = project.getAttribute('data-category');
        if (projectCategory === category || category === "Show All") {
            project.style.display = 'block';
        }
    });
}
