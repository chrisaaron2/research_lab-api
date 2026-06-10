import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { apiRequest } from "../api/client";
import { endpoints } from "../api/endpoints";
import type { LoginRequest, TokenResponse } from "../api/types";
import { setToken } from "../auth/auth";

export default function LoginPage(): JSX.Element {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<LoginRequest>({
    username: "admin",
    password: "admin123",
  });
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      const token = await apiRequest<TokenResponse>(endpoints.auth.login, {
        method: "POST",
        body: formData,
      });
      setToken(token.access_token);
      navigate("/dashboard");
    } catch {
      setErrorMessage("Login failed. Check the username and password.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="login-page">
      <section className="login-card">
        <div className="page-heading">
          <span>Admin access</span>
          <h1>Research Lab Manager</h1>
          <p>Sign in to manage demo data and protected write routes.</p>
        </div>
        <form className="form-stack" onSubmit={handleSubmit}>
          <label>
            Username
            <input
              onChange={(event) =>
                setFormData((current) => ({
                  ...current,
                  username: event.target.value,
                }))
              }
              value={formData.username}
            />
          </label>
          <label>
            Password
            <input
              onChange={(event) =>
                setFormData((current) => ({
                  ...current,
                  password: event.target.value,
                }))
              }
              type="password"
              value={formData.password}
            />
          </label>
          {errorMessage ? <p className="form-error">{errorMessage}</p> : null}
          <button className="button primary" disabled={isSubmitting} type="submit">
            {isSubmitting ? "Signing in..." : "Sign in"}
          </button>
        </form>
      </section>
    </main>
  );
}
