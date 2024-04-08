
function toggleTenant1() {
    var t1 = document.getElementById('t1');
    var t2 = document.getElementById('t2');
    var t3 = document.getElementById('t3');

    if (getComputedStyle(t1).display === 'none') {
      t1.style.display = 'flex';
      t2.style.display = 'none';
      t3.style.display = 'none'
    } 
    else if (getComputedStyle(t1).display === 'flex') {
      alert('tenant 1 is already visible.')
    }
  }

  function toggleTenant2() {
    var t1 = document.getElementById('t1');
    var t2 = document.getElementById('t2');
    var t3 = document.getElementById('t3');

    if (getComputedStyle(t2).display === 'none') {
        t2.style.setProperty('display', 'flex', 'important');
        t1.style.setProperty('display', 'none', 'important');
        t3.style.setProperty('display', 'none', 'important');
    } 
    else if (getComputedStyle(t2).display === 'flex') {
      alert('tenant 2 is already visible.')
    }
  }

  function toggleTenant3() {
    var t1 = document.getElementById('t1');
    var t2 = document.getElementById('t2');
    var t3 = document.getElementById('t3');

    if (getComputedStyle(t3).display == 'none') {
        t3.style.setProperty('display', 'flex', 'important');
        t1.style.setProperty('display', 'none', 'important');
        t2.style.setProperty('display', 'none', 'important');
    } 
    else if (getComputedStyle(t3).display === 'flex') {
      alert('tenant 3 is already visible.')
    }
  }

  const hamburger = document.querySelector(".hamburger");
  const navMenu = document.querySelector(".nav-menu");
  
  hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
  });
  
  document.querySelectorAll(".nav-link").forEach((link) =>
    link.addEventListener("click", () => {
      hamburger.classList.remove("active");
      navMenu.classList.remove("active");
    })
  );

