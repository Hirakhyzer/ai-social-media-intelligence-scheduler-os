# Scheduler design

The scheduler is intentionally a simulation layer in version 1.

Calendar records contain platform, topic, draft, scheduled date, scheduled time, backup time, approval state, brand-safety risk, and owner. The queue turns calendar items into scheduled tasks but keeps `real_adapter_enabled` set to false.

Future adapters can export to CSV, Google Calendar, Notion, or approved platform APIs. Adapter execution should be blocked unless human approval is present and the platform adapter validates credentials, rate limits, and policy compliance.
