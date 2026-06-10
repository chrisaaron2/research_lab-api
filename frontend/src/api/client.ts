import { clearToken, getToken } from "../auth/auth";

type ImportMetaWithEnv = ImportMeta & {
  env: {
    VITE_API_BASE_URL?: string;
  };
};

export const API_BASE_URL =
  (import.meta as ImportMetaWithEnv).env.VITE_API_BASE_URL ||
  "http://localhost:8000";

export type ApiRequestOptions = {
  method?: "GET" | "POST" | "PUT" | "DELETE";
  body?: unknown;
  headers?: Record<string, string>;
};

export class ApiError extends Error {
  status: number;
  detail: unknown;

  constructor(message: string, status: number, detail: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

function buildHeaders(options: ApiRequestOptions): Headers {
  const headers = new Headers(options.headers);
  const token = getToken();

  if (options.body !== undefined) {
    headers.set("Content-Type", "application/json");
  }

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  return headers;
}

function getResponseDetail(data: unknown): unknown {
  if (data && typeof data === "object" && "detail" in data) {
    return data.detail;
  }
  return data;
}

export async function apiRequest<T>(
  path: string,
  options: ApiRequestOptions = {},
): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method: options.method ?? "GET",
      headers: buildHeaders(options),
      body: options.body === undefined ? undefined : JSON.stringify(options.body),
    });
  } catch {
    throw new Error(
      `Could not reach the API at ${API_BASE_URL}. Check that FastAPI is running and CORS is configured.`,
    );
  }

  const contentType = response.headers.get("content-type") ?? "";
  const data = contentType.includes("application/json")
    ? await response.json()
    : null;

  if (!response.ok) {
    const detail = getResponseDetail(data);
    if (response.status === 401) {
      clearToken();
    }
    throw new ApiError(
      `Request failed with status ${response.status}`,
      response.status,
      detail,
    );
  }

  return data as T;
}
