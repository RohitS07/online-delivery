---
id: BPM-0002
title: A customer orders from the village agent
type: bpm
domain: ordering
status: accepted
actors: [customer, app, API, village agent]
triggers: [the customer opens the app during the order window]
constrained_by: [ADR-0006, ADR-0007, ADR-0008, ADR-0009, ADR-0010]
stories: []
---

# BPM-0002 — A customer orders from the village agent

## Purpose

A signed-in customer buys the day's stock of their village's one agent, pays in one step, and gets it delivered the same evening.

## Flow

1. The customer opens the app. It shows their village's stock for today's service date ([ADR-0008](../adr/ADR-0008-work-out-the-daily-order-window-from-the-clock-with-no-scheduled-job.md)), with each item's price and remaining quantity.
2. The customer searches by name, filters by category, and adds items to the cart.
3. The cart shows the subtotal, the delivery fee, the platform fee and the total. Both fees are admin settings and are fixed per order.
4. The customer checks out with their saved mock payment method and presses Pay Now. Payment goes through the payment interface of [ADR-0009](../adr/ADR-0009-outside-providers-sit-behind-interfaces-with-mocks-first.md).
5. When the payment succeeds, the order is created as `Placed` with payment `Paid`. The ordered quantities come off the remaining stock.
6. The customer sees the order number, the items, the total and "Expected delivery: before XX:00". That time is the close time plus the village's delivery hours.
7. The agent buys, travels and delivers. The customer sees `Out for Delivery`, then `Delivered`, and gets an in-app notification for each change.

## Decision points

- Is the order window open now? If not, the app shows when ordering opens next, and nothing can be ordered.
- Does the village have an approved agent? If not, the customer sees "Service will start soon in your village".
- Is there enough remaining quantity for every line at checkout? If not, the customer is told which line is short, and nothing is charged.
- Does the customer cancel? Only until the window closes. The mock refund sets payment to `Refunded`, and the quantities go back to stock. An admin may cancel at any time.

## Failure modes

- The window closes while the cart is open. The cart is emptied, and checkout is refused.
- Another customer takes the last units first. Checkout reports the short line.
- The payment fails (not possible with the mock, kept for a real provider). No order is created.
- The agent entered no stock for today. The village shows nothing to order.

## Outcome

Each checkout makes exactly one paid order for the village's agent, at prices fixed for the day, delivered the same day before the village's expected delivery time, or cancelled and refunded.
