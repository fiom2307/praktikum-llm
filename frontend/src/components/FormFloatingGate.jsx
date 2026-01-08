import { useLocation } from "react-router-dom";
import { useFormSettings } from "../hooks/useFormSettings";
import FloatingFormButton from "./FloatingFormButton";

export default function FormFloatingGate() {
  const {
    pretest_enabled,
    pretest_url,
    posttest_enabled,
    posttest_url,
  } = useFormSettings();
  const location = useLocation();

  const isAuthenticated = !!localStorage.getItem("authToken");

  const isAuthPage =
    location.pathname === "/login" ||
    location.pathname === "/register";

  if (!isAuthenticated || isAuthPage) {
    return null;
  }

  if (pretest_enabled && pretest_url) {
    return <FloatingFormButton baseUrl={pretest_url} />;
  }

  if (posttest_enabled && posttest_url) {
    return <FloatingFormButton baseUrl={posttest_url} />;
  }
  return null;
}