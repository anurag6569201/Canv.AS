let navbar = document.querySelector(".navbar");
window.addEventListener("scroll", () => {
  const offset = window.pageYOffset;
  console.log(offset);
  if (offset >= 10) {
    navbar.style.background= "rgba(255, 255, 255, 1)";
    navbar.style.boxShadow = "0 0 3px 10px white";
  }
  else {
    navbar.style.background = "rgba(255, 255, 255, 0)";
    navbar.style.boxShadow = "0 0 3px 10px transparent";
  }

});