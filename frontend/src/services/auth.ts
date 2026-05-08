const AUTH_TOKEN_KEY = "ai_interviewer_token";
const AUTH_CHANGED_EVENT = "auth-changed";
const AUTH_BROADCAST_CHANNEL = "ai-interviewer-auth";

function decodeBase64Url(value: string): string {
  const normalized = value.replace(/-/g, "+").replace(/_/g, "/");
  const padded = normalized.padEnd(Math.ceil(normalized.length / 4) * 4, "=");
  return atob(padded);
}

function getTokenExpiration(token: string): number | null {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) {
      return null;
    }
    const payloadText = decodeBase64Url(parts[1]);
    const payload = JSON.parse(payloadText) as { exp?: number };
    if (typeof payload.exp !== "number") {
      return null;
    }
    return payload.exp;
  } catch {
    return null;
  }
}

function isTokenExpired(token: string): boolean {
  const expiresAtSeconds = getTokenExpiration(token);
  if (!expiresAtSeconds) {
    return true;
  }
  const nowSeconds = Math.floor(Date.now() / 1000);
  return expiresAtSeconds <= nowSeconds;
}

function getCookie(name: string): string | null {
  const cookie = document.cookie
    .split("; ")
    .find((entry) => entry.startsWith(`${name}=`));
  if (!cookie) {
    return null;
  }
  return decodeURIComponent(cookie.slice(name.length + 1));
}

function getCookieAttributes(maxAgeSeconds?: number): string {
  const attributes = ["Path=/", "SameSite=Strict"];
  if (maxAgeSeconds !== undefined) {
    attributes.push(`Max-Age=${Math.max(0, maxAgeSeconds)}`);
  }
  if (window.location.protocol === "https:") {
    attributes.push("Secure");
  }
  return attributes.join("; ");
}

function setCookie(name: string, value: string, maxAgeSeconds?: number): void {
  document.cookie = `${name}=${encodeURIComponent(value)}; ${getCookieAttributes(
    maxAgeSeconds
  )}`;
}

function deleteCookie(name: string): void {
  document.cookie = `${name}=; ${getCookieAttributes(0)}`;
}

function clearLegacyLocalStorageToken(): void {
  localStorage.removeItem(AUTH_TOKEN_KEY);
}

function getLegacyLocalStorageToken(): string | null {
  return localStorage.getItem(AUTH_TOKEN_KEY);
}

function getStoredToken(): string | null {
  const cookieToken = getCookie(AUTH_TOKEN_KEY);
  if (cookieToken) {
    clearLegacyLocalStorageToken();
    return cookieToken;
  }

  const legacyToken = getLegacyLocalStorageToken();
  if (!legacyToken) {
    return null;
  }
  clearLegacyLocalStorageToken();
  if (!isTokenExpired(legacyToken)) {
    setAuthTokenCookie(legacyToken);
    return legacyToken;
  }
  return null;
}

function setAuthTokenCookie(token: string): void {
  const expiresAtSeconds = getTokenExpiration(token);
  const nowSeconds = Math.floor(Date.now() / 1000);
  const maxAgeSeconds =
    expiresAtSeconds === null ? undefined : expiresAtSeconds - nowSeconds;
  setCookie(AUTH_TOKEN_KEY, token, maxAgeSeconds);
}

function notifyAuthChanged(): void {
  window.dispatchEvent(new Event(AUTH_CHANGED_EVENT));
  if (typeof BroadcastChannel === "undefined") {
    return;
  }
  const channel = new BroadcastChannel(AUTH_BROADCAST_CHANNEL);
  channel.postMessage(AUTH_CHANGED_EVENT);
  channel.close();
}

export function getAuthToken(): string | null {
  const token = getStoredToken();
  if (!token) {
    return null;
  }
  if (isTokenExpired(token)) {
    clearAuthToken();
    return null;
  }
  return token;
}

export function setAuthToken(token: string): void {
  setAuthTokenCookie(token);
  clearLegacyLocalStorageToken();
  notifyAuthChanged();
}

export function clearAuthToken(): void {
  deleteCookie(AUTH_TOKEN_KEY);
  clearLegacyLocalStorageToken();
  notifyAuthChanged();
}

export function isAuthenticated(): boolean {
  return Boolean(getAuthToken());
}

export function onAuthChanged(listener: () => void): () => void {
  const channel =
    typeof BroadcastChannel === "undefined"
      ? null
      : new BroadcastChannel(AUTH_BROADCAST_CHANNEL);
  const onBroadcast = (event: MessageEvent) => {
    if (event.data === AUTH_CHANGED_EVENT) {
      listener();
    }
  };

  window.addEventListener(AUTH_CHANGED_EVENT, listener);
  channel?.addEventListener("message", onBroadcast);

  return () => {
    window.removeEventListener(AUTH_CHANGED_EVENT, listener);
    channel?.removeEventListener("message", onBroadcast);
    channel?.close();
  };
}
