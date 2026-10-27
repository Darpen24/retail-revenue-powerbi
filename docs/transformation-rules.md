# Transformation rules and KPI interpretation

## Exclusion precedence

`PreparedRetail` assigns one status to each row in this order:

1. Missing invoice/stock code or invoice date.
2. Missing or non-positive unit price.
3. Missing or zero quantity.
4. A cancellation-prefixed invoice with a positive quantity.
5. Otherwise valid.

Negative quantities are valid credit lines, including negative-quantity invoices
without a C prefix. This is a sign-based financial view, not a returns logistics
model. Null CustomerID is replaced by `Unknown` and never excluded on that basis.

Exact duplicates are removed **after text normalization and validation**, using
all eight normalized original fields. They are removed before the date scope is
applied. Row reconciliation follows that same sequence, so exclusions do not
overlap. The lack of a source line ID means identical legitimate line entries
could also be removed; preserve this caveat when discussing the dashboard.

## Date scope

`InvoiceDate >= 2011-01-01` and `< 2011-12-01`.
The source is historical, ending on 9 December 2011. An incomplete December would
make a naive month-over-month comparison misleading. No year-over-year KPI is
shown because the reporting scope does not contain a complete comparable prior
year. There is no timezone conversion: invoice dates are analyzed as supplied.

## DAX and filtering

- Net sales is gross sales minus credit value, each summed from fixed-decimal line values.
- Sales orders count distinct invoice identifiers on positive-quantity rows.
- AOV uses gross sales and sales orders; it does not divide net sales by a mix of
  sales invoices and credit documents.
- Known customers exclude `Unknown` and require at least one sale in the current
  filter context. Credits alone do not create an active sales customer.
- Credit-value ratio compares credit-note value with sales value in the selected
  period. The source does not link every credit back to its original sale; it is
  not a cohort return rate.
- Identified sales share uses **gross value**, not customer count or row count.
- Month selections and chart selections filter business measures. The audit table
  is disconnected from the dimensions and always describes the refresh scope.

## Dimension design

Country is taken from the customer's source record; it is not proof of delivery
destination. `Market` separates UK from international. Product descriptions can
vary by stock code, so an alphabetically first normalized description is used as
a reproducible label. No product taxonomy, cost of goods, profit, or synthetic
targets are invented.

## QA reference

`scripts/verify_data.py` mirrors the declared rules in pandas to independently
check totals. This script does not supply cleaned data to Power BI. Refresh the
native model to execute the actual Power Query M transformations.
