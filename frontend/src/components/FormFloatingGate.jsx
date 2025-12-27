import { useLocation } from "react-router-dom";
import { useFormSettings } from "../hooks/useFormSettings";
import FloatingFormButton from "./FloatingFormButton";

export default function FormFloatingGate() {
  const { pretest_enabled, posttest_enabled } = useFormSettings();
  const location = useLocation();

  const isAuthenticated = !!localStorage.getItem("authToken");

  const isAuthPage =
    location.pathname === "/login" ||
    location.pathname === "/register";

  if (!isAuthenticated || isAuthPage) {
    return null;
  }

  if (pretest_enabled) {
    return <FloatingFormButton type="pre" />;
  }

  if (posttest_enabled) {
    return <FloatingFormButton type="post" />;
  }

  return null;
}