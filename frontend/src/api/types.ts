export type TokenResponse = {
  access_token: string;
  token_type: "bearer";
};

export type LoginRequest = {
  username: string;
  password: string;
};

export type HealthResponse = {
  status: string;
  service: string;
};

export type CountableRecord = Record<string, unknown>;
