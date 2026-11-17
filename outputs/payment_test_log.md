# Payment test log

All of this is MOCKED: a simulated provider, test buyers, no real charges, refunds or payouts.
Product: SQL Interview Practice Workbook for Junior Data Analysts. Price: $11.99.

## Event trail

1. checkout created ord_fa991b62 for $11.99 (MOCKED hosted checkout; no card data touches our system)
2. checkout created ord_8a76f98e for $11.99 (MOCKED hosted checkout; no card data touches our system)
3. delivered ord_fa991b62: download token issued, delivery email STUBBED
4. ignored duplicate event evt_b7549c8cc7
5. delivery skipped for ord_fa991b62: already delivered (idempotent)
6. rejected event evt_forged: bad signature
7. delivered ord_8a76f98e: download token issued, delivery email STUBBED
8. access revoked for ord_fa991b62

## Deliveries (STUBBED emails)

- ord_fa991b62 -> buyer-A (test): /download/dl_315cf81c2315 (STUBBED: email recorded, not sent)
- ord_8a76f98e -> buyer-B (test): /download/dl_6797828c1f86 (STUBBED: email recorded, not sent)

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
