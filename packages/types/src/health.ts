export interface ServiceHealth {
  status: "ok" | "error";
  service: string;
}

export type ServiceHealthStatus = ServiceHealth["status"];
