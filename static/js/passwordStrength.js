// passwordStrength.js
import { passwordStrength } from "check-password-strength";

export function getPasswordStrength(password) {
  return passwordStrength(password);
}
