import { togglePasswordVisibility } from "./togglePasswordVisibility.js";
import { updateStrengthMeter, updateStrengthText } from "./updateUI.js";
import { getPasswordStrength } from "./passwordStrength.js";

document.addEventListener("DOMContentLoaded", function () {
  const passwordInput = document.getElementById("sifre");
  const showPasswordCheckbox = document.getElementById("showPassword");
  const showPasswordDownloadCheckbox = document.getElementById(
    "showPasswordDownload"
  );
  const showPasswordDeleteCheckbox =
    document.getElementById("showPasswordDelete");

  showPasswordCheckbox.addEventListener("change", function () {
    togglePasswordVisibility("sifre");
  });

  if (passwordInput) {
    passwordInput.addEventListener("input", function () {
      const strength = getPasswordStrength(passwordInput.value);
      updateStrengthMeter(getStrengthScore(strength.value));
      updateStrengthText(strength.value);
    });
  }

  function getStrengthScore(strengthValue) {
    switch (strengthValue) {
      case "Too weak":
        return 1;
      case "Weak":
        return 2;
      case "Medium":
        return 3;
      case "Strong":
        return 4;
      default:
        return 0;
    }
  }

  if (showPasswordDownloadCheckbox) {
    showPasswordDownloadCheckbox.addEventListener("change", function () {
      togglePasswordVisibility("downloadPassword");
    });
  }

  if (showPasswordDeleteCheckbox) {
    showPasswordDeleteCheckbox.addEventListener("change", function () {
      togglePasswordVisibility("deletePassword");
    });
  }
});
