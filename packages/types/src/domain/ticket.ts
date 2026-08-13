/**
 * Placeholder domain types for future shared contracts.
 * Real ticket/organization models will be added in later development steps.
 */

export type TicketStatus = "open" | "pending" | "resolved" | "closed";

export interface TicketSummary {
  id: string;
  subject: string;
  status: TicketStatus;
  createdAt: string;
}
