import { ServiceStatus } from "@/components/ServiceStatus";

export default function HomePage() {
  return (
    <main>
      <h1>SupportPilot</h1>
      <p className="subtitle">AI Support Operations</p>
      <ServiceStatus />
    </main>
  );
}
