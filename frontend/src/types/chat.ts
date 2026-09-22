export type Role = "user" | "assistant" | "tool";

export interface Message {
  role: Role;
  content: string;
  toolName?: string;
}