---
id: BPM-0003
title: An agent runs the daily stock and delivery cycle
type: bpm
domain: fulfilment
status: accepted
actors: [village agent, city vendors, app, API]
triggers: [the order window of the previous service date closes]
constrained_by: [ADR-0007, ADR-0008, ADR-0009, ADR-0010]
stories: []
---

# BPM-0003 — An agent runs the daily stock and delivery cycle

## Purpose

The one approved agent of a village publishes the day's confirmed stock before the window opens, then buys and delivers everything ordered.

## Flow

1. Before the open time (default 8:00 IST), the agent confirms items, quantities and prices with city vendors, usually by phone.
2. The agent enters the day's stock: name, category, quantity, price and an optional image. A name can be picked from items used on earlier days. That fills name, category and image. Quantity and price always start blank.
3. The agent presses Update. They may change and update as often as they like until the open time. Customers do not see this stock yet.
4. At the open time, editing closes and the stock goes live ([ADR-0008](../adr/ADR-0008-work-out-the-daily-order-window-from-the-clock-with-no-scheduled-job.md)). During the window the agent sees remaining quantities but cannot edit.
5. At the close time (default 18:00 IST), ordering stops and any remaining stock is no longer offered.
6. The agent views the day's orders and one purchase list that adds up each item across all orders. Both can be downloaded as PDF.
7. The agent buys from the vendors, who hold the confirmed quantities, and travels to the village.
8. The agent marks each order `Out for Delivery`, then `Delivered`, before the village's expected delivery time.

## Decision points

- Is it before the open time? Only then can stock be added, changed or removed.
- Is the agent approved for this village? An agent who is waiting or blocked cannot enter stock.
- Is the service date a holiday? Then the window does not open, and no stock is entered for that date.

## Failure modes

- The agent enters no stock before the open time. The village has nothing to order that day.
- The agent tries to edit after the open time. The API refuses.
- The agent forgets to mark an order delivered. It stays `Out for Delivery` and shows in the admin's order list.

## Outcome

Every order placed in the window is bought and delivered the same day. Stock never carries over to the next service date. There is no shortage handling, because vendors hold the confirmed quantities.
