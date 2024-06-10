"use strict";

document.getElementById("sifre").addEventListener("input", handlePasswordInput);
document
  .getElementById("showPassword")
  .addEventListener("change", togglePasswordVisibility.bind(null, "sifre"));

document
  .getElementById("showPasswordDownload")
  .addEventListener(
    "change",
    togglePasswordVisibility.bind(null, "downloadPassword")
  );

document
  .getElementById("showPasswordDelete")
  .addEventListener(
    "change",
    togglePasswordVisibility.bind(null, "deletePassword")
  );

function handlePasswordInput() {
  const password = this.value;
  const strength = checkPasswordStrength(password);

  updateStrengthMeter(strength.score);
  updateStrengthText(strength.message);
}

function checkPasswordStrength(password) {
  let score = 0;
  const scoreCriteria = [
    { regex: /.{8,}/, message: "Minimum 8 karakter", points: 1 },
    { regex: /[A-Z]/, message: "Büyük harf", points: 1 },
    { regex: /[a-z]/, message: "Küçük harf", points: 1 },
    { regex: /[0-9]/, message: "Rakam", points: 1 },
    { regex: /[^A-Za-z0-9]/, message: "Özel karakter", points: 1 },
  ];

  scoreCriteria.forEach((criteria) => {
    if (criteria.regex.test(password)) score += criteria.points;
  });

  const messages = ["Zayıf", "Orta", "Güçlü", "Çok Güçlü"];
  const message = messages[Math.min(score, messages.length - 1)];

  return { score: score, message: message };
}

function updateStrengthMeter(score) {
  const strengthMeter = document.getElementById("strengthMeter");
  strengthMeter.value = score;
}

function updateStrengthText(message) {
  const strengthText = document.getElementById("strengthText");
  strengthText.textContent = message;
}

function togglePasswordVisibility(inputId) {
  const passwordInput = document.getElementById(inputId);
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
  } else {
    passwordInput.type = "password";
  }
}
