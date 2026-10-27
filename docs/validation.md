# Validation record · 27 October 2026

## Data checks

The unmodified source workbook SHA-256 is recorded in `verified-metrics.json`.
`verify_data.py --check` passed the workbook checksum, all audit counts, business
KPI totals, and monthly financial totals against the committed baseline. Additional
assertions cover the gross-minus-credit identity, duplicate exclusion, date scope,
positive prices, and eleven months of coverage.

## Power BI Desktop

Store package version: **2.159.883.0**.

- Opened the native PBIP project without a report-definition error.
- Executed the actual M import queries in Power BI, loading FactSales, DimDate,
  DimCountry, DimProduct and QualityAudit.
- Verified the rendered overview: £8.57m net sales, 17,582 orders, £522.29 gross
  AOV, 4,173 known customers and 6.69% credit-value ratio.
- Verified the rendered audit: 541,909 source rows, 2,517 invalid rows, 5,263 exact
  duplicates, 66,902 outside-period rows, 467,227 loaded rows and 109,396 rows with
  unidentified customers. Identified gross-sales share is 84.94%.
- Selected January in the month slicer: net sales displayed £0.56m and the
  credit-value ratio 19.04%, consistent with the independently calculated month.
- Cleared that selection and restored the complete reporting period.
- Saved a populated PBIX and exported both pages directly from Desktop to PDF.
- Rendered the PDF pages with Poppler and inspected both pages for clipping and
  readability. The native PNG deliverables come from this PDF.

## Report source checks

Forty PBIR definition JSON files passed Microsoft's public schemas. Desktop wrote
some visual schema references as 2.14.0, whose public URL was unavailable at the
time of validation. Their references were normalized to published 2.13.0 after
confirming the actual definitions conform to that schema. Power BI reopened and
rendered the compatible report source successfully.

## Scope and limitations

This is a historical portfolio analysis, not a current operating business report.
The source lacks reliable invoice-line IDs and cost data. Deduplication is a
documented assumption; no profit KPI or physical-returns rate is claimed. Public
customer IDs are pseudonymous identifiers from the supplied dataset, not customer
names or contact information. No Power BI Service deployment was performed.
