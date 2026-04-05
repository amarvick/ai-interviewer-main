import { clearAuthToken, getAuthToken } from "../auth";

const ENV_TARGET =
  (import.meta.env.VITE_ENV_TARGET ?? import.meta.env.MODE ?? "development")
    .toString()
    .toLowerCase();

const LOCAL_API_BASE =
  import.meta.env.VITE_API_BASE_URL_LOCAL ?? "http://127.0.0.1:8000";

const PROD_API_BASE =
  import.meta.env.VITE_API_BASE_URL_PROD ??
  import.meta.env.VITE_API_BASE_URL ??
  LOCAL_API_BASE;

export const API_BASE_URL =
  ENV_TARGET === "prod" || ENV_TARGET === "production"
    ? PROD_API_BASE
    : LOCAL_API_BASE;

export function buildAuthHeaders(headers: HeadersInit = {}): HeadersInit {
  const token = getAuthToken();
  if (!token) {
    return headers;
  }
  return {
    Authorization: `Bearer ${token}`,
    ...headers,
  };
}

export async function requestJson<T>(
  input: RequestInfo | URL,
  init?: RequestInit
): Promise<T> {
  let response: Response;
  try {
    response = await fetch(input, init);
  } catch (error) {
    const message =
      error instanceof Error
        ? `Network request failed: ${error.message}`
        : "Network request failed.";
    throw new Error(message);
  }
  return parseJson<T>(response);
}

export async function parseJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    if (response.status === 401) {
      clearAuthToken();
    }
    const fallback = `Request failed with status ${response.status}`;
    let message = fallback;
    try {
      const errorPayload = (await response.json()) as { detail?: string };
      if (errorPayload?.detail) {
        message = errorPayload.detail;
      }
    } catch {
      // keep fallback
    }
    throw new Error(message);
  }

  return (await response.json()) as T;
}
