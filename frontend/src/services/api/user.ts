import type {
  LoginPayload,
  SignupPayload,
  TokenResponse,
  User,
} from "../../types/user";
import { API_BASE_URL, requestJson } from "./api";

export async function login(payload: LoginPayload): Promise<TokenResponse> {
  return requestJson<TokenResponse>(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export async function register(payload: SignupPayload): Promise<User> {
  return requestJson<User>(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}
