export function updateStrengthMeter(score) {
  const strengthMeter = document.getElementById("strengthMeter");
  if (strengthMeter) {
    strengthMeter.value = score;
  }
}

export function updateStrengthText(message) {
  const strengthText = document.getElementById("strengthText");
  if (strengthText) {
    strengthText.textContent = message;
  }
}
