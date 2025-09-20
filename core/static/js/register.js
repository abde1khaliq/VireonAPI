const toggleRegisterPassword = document.querySelector(
  "#toggleRegisterPassword"
);
const registerPassword = document.querySelector("#registerPassword");
const toggleConfirmPassword = document.querySelector("#toggleConfirmPassword");
const confirmPassword = document.querySelector("#confirmPassword");
const strengthMeter = document.querySelector("#passwordStrength");
const passwordHints = {
  length: document.querySelector("#lengthHint"),
  number: document.querySelector("#numberHint"),
  special: document.querySelector("#specialHint"),
};

toggleRegisterPassword.addEventListener("click", function () {
  const type =
    registerPassword.getAttribute("type") === "password" ? "text" : "password";
  registerPassword.setAttribute("type", type);
  this.innerHTML =
    type === "password"
      ? '<i class="bx bx-hide"></i>'
      : '<i class="bx bx-show"></i>';
});

toggleConfirmPassword.addEventListener("click", function () {
  const type =
    confirmPassword.getAttribute("type") === "password" ? "text" : "password";
  confirmPassword.setAttribute("type", type);
  this.innerHTML =
    type === "password"
      ? '<i class="bx bx-hide"></i>'
      : '<i class="bx bx-show"></i>';
});

// Password strength checker
registerPassword.addEventListener("input", function () {
  const password = this.value;
  let strength = 0;

  // Length check
  if (password.length >= 8) {
    strength += 1;
    passwordHints.length.classList.add("valid");
  } else {
    passwordHints.length.classList.remove("valid");
  }

  // Number check
  if (/\d/.test(password)) {
    strength += 1;
    passwordHints.number.classList.add("valid");
  } else {
    passwordHints.number.classList.remove("valid");
  }

  // Special character check
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    strength += 1;
    passwordHints.special.classList.add("valid");
  } else {
    passwordHints.special.classList.remove("valid");
  }

  // Update strength meter
  const width = (strength / 3) * 100;
  strengthMeter.style.width = `${width}%`;

  // Update meter color
  if (strength === 1) {
    strengthMeter.style.background = "var(--error-color)";
  } else if (strength === 2) {
    strengthMeter.style.background = "orange";
  } else if (strength === 3) {
    strengthMeter.style.background = "var(--success-color)";
  }
});
