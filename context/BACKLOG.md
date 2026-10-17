# Backlog — deliberately out of scope

Real work we intend to do, none of it with an id yet. Ids are allocated when the work enters
scope, so the registry describes what is being built rather than what is imagined.

- The health check also checks the database, once the API uses it.
- HSTS on the API outside Development.
- Forwarded headers on the API when it is hosted behind Azure's TLS front end, before the HTTPS redirect goes live.
- Browser end-to-end tests that run both apps together.
- Full admin: customer and order management, editing orders, creating an order for a customer.
- Reports and analytics, with CSV and PDF export.
- An audit log of critical admin actions.
- Admin-managed notification templates, and SMS notifications.
- A real SMS provider for OTP, replacing the mock.
- A real payment gateway, replacing the mock. Which gateway can serve Indian businesses is still open.
- Image storage in cloud object storage, replacing the local folder.
- Paying agents their delivery fees and item takings.
- Hosting on Azure, with backups, monitoring and a restore process.
- A native speaker's review of all Marathi text before go-live.
