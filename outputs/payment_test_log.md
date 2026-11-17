# Payment test log

All of this is MOCKED: a simulated provider, test buyers, no real charges, refunds or payouts.
Product: SQL Interview Practice Workbook for Junior Data Analysts. Price: $11.99.

## Event trail

1. checkout created ord_010fcba2 for $11.99 (MOCKED hosted checkout; no card data touches our system)
2. checkout created ord_d244f78e for $11.99 (MOCKED hosted checkout; no card data touches our system)
3. delivered ord_010fcba2: download token issued, delivery email STUBBED
4. ignored duplicate event evt_5b1b2d78f4
5. delivery skipped for ord_010fcba2: already delivered (idempotent)
6. rejected event evt_forged: bad signature
7. delivered ord_d244f78e: download token issued, delivery email STUBBED
8. access revoked for ord_010fcba2

## Deliveries (STUBBED emails)

- ord_010fcba2 -> buyer-A (test): /download/dl_dabd9a5d45db (STUBBED: email recorded, not sent)
- ord_d244f78e -> buyer-B (test): /download/dl_8b862a9f4822 (STUBBED: email recorded, not sent)

## Checks

- PASS: checkout_creates_pending_order_without_access
- PASS: unpaid_order_cannot_be_delivered
- PASS: payment_triggers_delivery
- PASS: duplicate_event_is_ignored
- PASS: retry_with_new_event_id_does_not_double_deliver
- PASS: forged_webhook_rejected
- PASS: paid_buyer_can_download
- PASS: refund_blocked_without_founder_approval
- PASS: agent_cannot_approve_its_own_refund
- PASS: refund_revokes_access
- PASS: books_reconcile_orders_payments_fees_payouts

## Reconciliation

```json
{
 "orders": 2,
 "gross": 23.98,
 "refunded": 11.99,
 "fees": 1.3,
 "payouts": 10.69,
 "expected_net": 10.69,
 "balanced": true,
 "issues": []
}
```
