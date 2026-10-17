# Delivery Service Web Application — Project Specification

> The source document the context tree was written from. It is kept for reference and is not an artefact.
> Where it and an artefact differ, the artefact wins.

## 1. Project Overview

The client requires a responsive web application that connects customers in villages with delivery agents who purchase requested goods from a nearby city and deliver them to customers.

Customers browse items available in their village, add them to a cart, place orders, make payment through a saved mock Stripe payment method, and track delivery status. Delivery agents manage village-specific stock, view daily customer requests, purchase items from the city, deliver orders, and update order status. Administrators manage users, master data, orders, platform configuration, notifications, and reports.

Each village has exactly one approved delivery agent, and each agent serves exactly one village. The agent maintains the stock for that village.

During sign-up, a customer selects their city and village. The application then shows the village's delivery agent and that agent's stock for the day.

### Daily Operating Cycle

All times are in IST. The open and close times are admin settings, with defaults of 8:00 and 18:00.

| Time | What happens |
|---|---|
| Before 8:00 | The agent confirms items, quantities and prices with city vendors, usually by phone. The agent enters the day's stock in the app and presses Update. They may update as often as they like. Customers cannot see this stock yet. |
| 8:00 | Stock editing closes for the agent. The stock goes live, and customers can place orders. |
| 8:00 – 18:00 | Customers order. Each order reduces the remaining quantity. Prices and items cannot change. |
| 18:00 | The order window closes for the day. Any remaining stock is cleared. Stock never carries over to the next day. |
| After 18:00 | The agent buys the ordered items from the vendors, travels to the village and delivers the orders before the village's expected delivery time. |

- The vendor holds the confirmed quantities for the agent, even if the agent arrives after 18:00. There is no shortage handling.
- The price the customer pays is final. The agent never pays vendors a difference after purchase.
- If the agent enters no stock before 8:00, the village has nothing to order that day.
- A change to the open or close time applies from the next day, never during an open window.
- No orders can be placed outside the order window. Every order is delivered on the day it is placed.

### Initial Service Coverage

| City | Villages |
|---|---|
| Pune | Mulshi, Jejuri |
| Mumbai | Pali, Matheran |

The platform must support adding more cities and villages later through the admin module.

### Project Goal

Define the functional and non-functional scope required to estimate effort, propose architecture, plan development phases, and build the initial version of the platform.

## 2. User Roles

| Role | Description |
|---|---|
| Customer | A village resident who registers, selects items, adds them to a cart, pays for orders, places orders, and tracks delivery status. |
| Delivery Agent | A person serving exactly one village who manages the day's stock, views daily requests, purchases items from the city, delivers orders, and updates delivery status. |
| Admin | A platform user who manages customers, delivery agents, cities, villages, stock, orders, notifications, configuration, and reports. |

## 3. Core Modules and Features

### 3.1 Customer Module

#### Authentication and Profile

- Register and log in using Indian mobile number and OTP.
- OTP verification may use a demo/mock provider in Phase 1; the implementation must allow replacement with a real SMS provider later.
- Manage profile details:
  - Full name
  - Contact number
  - Delivery address
  - City
  - Village
  - Saved payment method token/reference

#### Item Browsing and Cart

- View today's in-stock items for the customer’s village, during the order window.
- Outside the order window, see when ordering opens next.
- In a village with no approved agent, customers can register but see "Service will start soon in your village".
- Search items by name and filter by category.
- View item details: name, image, category, remaining quantity, price, and delivery agent.
- Add items to the cart.
- Update item quantity in the cart.
- Remove items from the cart.
- View cart subtotal, delivery fee, platform fee, and order total.
- Each order has a fixed delivery fee (default ₹90) and a fixed platform fee (default ₹10). Both are admin settings.

#### Order Placement

- Submit an order from the cart.
- Orders can be submitted only during the order window.
- An order cannot exceed the remaining quantity of any item.
- A cart left open when the window closes is emptied.
- The customer can cancel an order until the window closes. An admin can cancel at any time. A cancelled order is refunded (mocked) and its quantities are returned to stock while the window is open.
- Select or use the saved mock payment method.
- Pay for the order using a one-click mock payment flow.
- Order placement should be allowed only after successful payment simulation.
- Display a clear order confirmation with order number, items, total amount, payment status, and expected delivery time, shown as "Expected delivery: before XX:00".

#### Order History and Tracking

- View a list of past and current orders.
- Search and filter order history by date, status, or item.
- View order details:
  - Ordered items
  - Quantity
  - Item price
  - Delivery fee
  - Platform fee
  - Total amount
  - Payment status
  - Order status
  - Assigned delivery agent
  - Expected delivery time
- Receive in-app notifications for order and payment status changes.

### 3.2 Delivery Agent Module

#### Authentication and Profile

- Sign up with mobile number and OTP, choosing the city and the one village to serve.
- A new agent waits for admin approval and cannot add stock until approved.
- A village that already has an approved agent cannot get a second one. Another agent who signs up for it stays waiting for approval.
- Manage profile and contact details.

#### Daily Stock

See the Daily Operating Cycle in section 1.

- Between the close of the previous order window and the next opening time, enter the day's stock items:
  - Item name, typed or picked from items the agent used on earlier days
  - Item image (optional)
  - Category
  - Quantity
  - Price
- Picking an earlier item fills in its name, category and image only. Quantity and price are always blank and must be entered for the day.
- Edit or remove items and press Update as many times as needed before the opening time.
- At the opening time, editing closes and the stock goes live.
- Between the opening and closing times, view the remaining quantity of each item. No edits are possible.
- At the closing time, any remaining stock is cleared. Nothing carries over to the next day.

#### Daily Orders and Purchasing

- View today’s orders for the agent's village.
- View individual order details:
  - Customer name
  - Customer contact number
  - Customer delivery address
  - Ordered items
  - Quantity
  - Item prices
  - Order total
- Download an individual order as a PDF.
- View an aggregated purchase list for the day.
- The aggregated list must consolidate quantities of the same item across all of the day's orders. It is final once the order window closes.
- Download the daily aggregated purchase list as a PDF.

#### Delivery Management

- Update order status.
- View delivered order history for the last 10 days.
- Search and filter delivered orders by date, customer, or order status.

### 3.3 Admin Module

#### Authentication and Access Control

- Secure admin login with role-based access control.
- Support multiple admin roles if required, for example super admin and operations admin.

#### Customer Management

- View, search, and filter customers.
- View customer profile, village, contact details, and order history.
- Approve, block, or unblock customers.

#### Delivery Agent Management

- View, search, and filter delivery agents.
- View agent profile, assigned city/village, stock, and order history.
- Approve, block, or unblock delivery agents.
- Approve an agent only for a village that has no approved agent.
- Replace a village's agent by blocking the current agent and approving a waiting one.

#### Order Management

- View all orders with search and filters:
  - Date range
  - Order status
  - Payment status
  - City
  - Village
  - Customer
  - Delivery agent
- View complete order details.
- Edit eligible order details.
- Cancel orders.
- Create an order on behalf of a customer.

#### Stock and Master Data Management

- Manage stock items:
  - Name
  - Image
  - Category
  - Price
  - Quantity
  - Delivery agent
  - Availability status
- Manage item categories.
- Manage cities and villages.
- Set each village's delivery hours. The expected delivery time is the closing time plus these hours. For example, 18:00 plus 3 hours shows customers "Expected delivery: before 21:00".
- Manage delivery agents and their village assignment.

#### Platform Configuration

- Configure the daily order window: opening time (default 8:00 IST) and closing time (default 18:00 IST).
- Configure the delivery fee added to each order. Default: ₹90.
- Configure the platform fee added to each order. Default: ₹10.
- Changes to fees apply to new orders only.
- Add, edit, or remove cities and villages.
- Configure holidays or service pause dates. On these dates the order window does not open.
- Configure notification templates for SMS and in-app notifications.

#### Reporting and Analytics

- Daily, weekly, and monthly order volume.
- Revenue reports.
- Most-requested items.
- Delivery agent performance.
- Order volume per delivery agent.
- Order volume per village.
- Export reports as CSV or PDF.

### 3.4 Payments — Phase 1 Mock Integration

- Customers can save a Stripe-style payment method using a mock UI.
- No real card, bank account, or sensitive payment data will be collected or stored in Phase 1.
- Customers can pay using a one-click “Pay Now” action.
- The mock payment flow simulates a successful payment.
- On successful mock payment, the order payment status changes to `Paid`.
- Payment status must be visible in current order details and order history.
- The payment architecture must be designed so a real Stripe integration can be added later without major redesign.

### 3.5 Common Platform Features

- Role-based authentication and authorization.
- In-app notifications for:
  - Order placed
  - Payment received
  - Out for delivery
  - Delivered
  - Order cancelled
- Responsive, mobile-first UI for customers and delivery agents.
- Desktop-friendly admin interface.
- Search and filtering across relevant lists.
- CSV and PDF export for admin reports.
- Audit logging for critical admin actions, such as blocking users, editing orders, changing configuration, and cancelling orders.

## 4. Order Lifecycle

Every order is placed and delivered on the same day. An order is created only after the mock payment succeeds. There is no acceptance step: every order placed in the window is fulfilled.

```text
Placed -> Out for Delivery -> Delivered

Placed -> Cancelled
```

| Status | Description |
|---|---|
| Placed | Customer has submitted the order and mock payment is successful. |
| Out for Delivery | The agent has bought the items and started delivery. |
| Delivered | The agent has delivered the order. |
| Cancelled | Cancelled by the customer before the window closes, or by an admin at any time. |

Payment status is a separate field: Paid, Refunded. Pending and Failed are reserved for a real payment provider later.

## 5. Data Model Outline

The following entities are recommended for the initial implementation:

| Entity | Key Fields |
|---|---|
| User | Id, role, name, mobile number, email, status, created date |
| CustomerProfile | User Id, address, city Id, village Id, contact number |
| DeliveryAgentProfile | User Id, city Id, village Id, status (waiting, approved, blocked), contact details. At most one approved agent per village. |
| City | Id, name, is active |
| Village | Id, city Id, name, delivery hours, is active |
| Category | Id, name, is active |
| StockItem | Id, delivery agent Id, service date, name, image URL, category Id, price, quantity, remaining quantity. Belongs to one service date and is never carried over. |
| Cart | Id, customer Id, status |
| CartItem | Id, cart Id, stock item Id, quantity, unit price |
| Order | Id, order number, customer Id, delivery agent Id, village Id, service date, expected delivery time, status, payment status, customer name, phone and address at order time, subtotal, delivery fee, platform fee, total amount |
| OrderItem | Id, order Id, stock item Id, item name, quantity, unit price, line total |
| Payment | Id, order Id, payment method reference, amount, status, transaction reference, paid date |
| PaymentMethod | Id, customer Id, provider, mock token/reference, is default |
| Notification | Id, user Id, type, title, message, is read, created date |
| NotificationTemplate | Id, event type, channel, subject, body, is active |
| PlatformSetting | Key, value, description |
| ServiceHoliday | Id, date, reason, is active |

Platform settings include the order window opening time, closing time, delivery fee and platform fee.
| AuditLog | Id, user Id, action, entity type, entity Id, old value, new value, created date |

## 6. Non-Functional Requirements

### Platform and Usability

- Responsive web application supporting mobile browsers and desktop browsers.
- Mobile-first design for customer and delivery agent flows.
- Accessible and simple UI suitable for users in rural areas.
- Support for the latest versions of major browsers.

### Security

- Secure authentication and session management.
- Role-based authorization for all APIs and screens.
- Encrypt sensitive data in transit using HTTPS/TLS.
- Store passwords securely using a modern password-hashing algorithm where applicable.
- Do not store raw card or bank data, even in the mock payment implementation.
- Follow payment-security best practices so real Stripe integration can be added safely.
- Protect APIs against common vulnerabilities, including unauthorized access, injection, CSRF, and abuse.

### Performance

- Dashboard and order-history screens should load quickly as data grows.
- Use pagination, indexing, and efficient queries for order and report data.
- PDF generation should not block the main user workflow.
- Optimize images and static assets for mobile networks.

### Scalability and Availability

- Architecture should support growth in customers, villages, delivery agents, and order volume.
- Use a cloud-hosted, horizontally scalable architecture where practical.
- Target standard small-to-medium business application availability.
- Implement structured application logging and error monitoring.

### Data Backup and Retention

- Schedule regular automated database backups.
- Retain order and payment records according to business and compliance requirements.
- Provide a documented backup and restore process.

## 7. Suggested Technology Approach

The following stack is suggested; final technology decisions may be confirmed during discovery.

| Area | Suggested Technology |
|---|---|
| Frontend | React with TypeScript, mobile-first responsive UI |
| Backend | .NET Web API / ASP.NET Core REST API |
| Database | PostgreSQL |
| ORM | Entity Framework Core |
| Authentication | Mobile OTP-based authentication with JWT or secure session tokens |
| OTP/SMS | Indian SMS provider; mock provider acceptable for Phase 1 |
| Payments | Mock Stripe-style integration; real Stripe integration later |
| PDF Generation | Server-side PDF library |
| Notifications | In-app notifications; SMS template support for future use |
| File/Image Storage | Azure Blob Storage or equivalent cloud object storage |
| Hosting | Azure App Service, Azure Database for PostgreSQL, Azure Blob Storage |
| CI/CD | GitHub Actions or Azure DevOps |
| Monitoring | Application Insights or equivalent |

## 8. Suggested Development Phases

### Phase 1 — Foundation

- Project setup, repository, CI/CD, environments, and database schema.
- Authentication and role-based access.
- City, village, category, and user management foundations.
- Basic admin dashboard.

### Phase 2 — Customer Experience

- Customer registration, OTP login, and profile management.
- Village-based item browsing and filtering.
- Cart and order placement.
- Mock payment method and one-click payment.
- Order history and in-app notifications.

### Phase 3 — Delivery Agent Experience

- Delivery agent onboarding and stock management.
- Daily order list and order details.
- Aggregated daily purchase list.
- PDF downloads.
- Order status updates and delivered-order history.

### Phase 4 — Admin and Operations

- Full customer, agent, order, and stock administration.
- Platform configuration: order window times, delivery and platform fees, village delivery hours, holidays, cities, and villages.
- Notification template management.
- Reporting, analytics, CSV, and PDF exports.

### Phase 5 — Hardening and Go-Live

- Security review and penetration-testing fixes.
- Performance testing and load testing.
- UAT with real customers and delivery agents.
- Deployment, monitoring, backup configuration, documentation, and training.

## 9. Acceptance Criteria

- A customer can register using a mobile number, select a village, and view relevant stock.
- A customer can add items to a cart, pay using the mock payment method, and place an order.
- An agent can enter the day's stock only before the opening time. At the opening time the stock goes live and cannot be edited.
- Customers can order only between the opening and closing times. At the closing time, remaining stock is cleared.
- An order never exceeds an item's remaining quantity.
- Each village has at most one approved agent. A new agent waits for admin approval.
- A delivery agent can view today’s orders and download an individual order PDF.
- A delivery agent can view and download an aggregated purchase list for the day.
- A delivery agent can update order status and view delivered orders from the last 10 days.
- An admin can manage customers, delivery agents, stock, orders, cities, villages, fees, order window times, and holidays.
- Admin users can view operational and revenue reports and export them as CSV or PDF.
- Users receive in-app notifications for relevant order and payment events.
- The application is responsive on mobile and desktop browsers.
- The payment implementation can be replaced with real Stripe integration without a major redesign.

## 10. Open Questions for Discovery

- What is the expected number of customers, delivery agents, villages, and daily orders at launch?
- What is the refund or cancellation policy after payment?
- Which SMS/OTP provider will be used in production?
- What reporting metrics and date ranges are required at launch?
- Are there regional-language requirements for the customer interface?
- What are the data-retention, privacy, and compliance requirements?

## 11. Deliverables

- Technical architecture proposal, including stack, hosting approach, and data model outline.
- UI/UX wireframes for customer, delivery agent, and admin roles.
- Development plan with phases, milestones, and estimated timeline.
- Cost estimate, either fixed bid or time and materials.
- Test plan, including unit, integration, security, performance, and UAT testing.
- Deployment setup and environment configuration.
- Admin and delivery-agent documentation and basic training.

## 12. Assumptions

- Phase 1 uses mock OTP and mock Stripe payment flows.
- Real SMS and real payment-gateway integration will be handled in a later phase.
- The initial platform supports the cities and villages listed above, with admin-managed expansion.
- The customer selects their village during registration.
- Delivery agents are responsible for adding and maintaining their own stock.
- Each village has exactly one approved delivery agent, and each agent serves exactly one village.
- Delivery agents confirm stock and prices with city vendors before the order window opens. Vendors hold the confirmed quantities, so there is no shortage handling.
- Item prices are fixed for the day once the window opens. The agent never pays vendors a difference.
- Every order is placed and delivered on the same day.
- Each order carries a fixed delivery fee (default ₹90) and a fixed platform fee (default ₹10), both configurable by the admin. The delivery fee goes to the agent and the platform fee to the platform.
- Final requirements, pricing rules and operational workflows will be finalized in a discovery workshop.
