export function togglePasswordVisibility(inputId) {
  const passwordInput = document.getElementById(inputId);
  passwordInput.type = passwordInput.type === "password" ? "text" : "password";
}
