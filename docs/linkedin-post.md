I built a retail revenue dashboard with Power BI and Power Query using UCI's public Online Retail dataset.

The most useful part was deciding what the numbers should mean before choosing the charts.

The Power Query pipeline types and cleans the source, flags invalid records, removes exact duplicates under a documented assumption, retains sales with missing customer IDs, and separates sales from credit notes. I used January–November 2011 so the incomplete December period would not distort the monthly trend.

The report has two pages: a revenue overview and a data-quality audit. The second page makes the cleaning decisions visible rather than hiding them behind the final KPIs.

The historical reporting period contains £8.57m in net sales and 17,582 sales orders. The 6.69% credit-value ratio includes cancellations and adjustments—it is not a physical returns rate. I independently reconciled the totals against the workbook with Python; Power Query performs the actual model transformations.

The Power BI report, M scripts, DAX measures, validation code and source attribution are available on GitHub: https://github.com/Darpen24/retail-revenue-powerbi

Dataset: Chen, D. (2015), Online Retail, UCI Machine Learning Repository, CC BY 4.0. https://doi.org/10.24432/C5BW33

#PowerBI #PowerQuery #DataAnalytics #BusinessIntelligence #DataVisualization

---

Sharing note: use `RetailRevenue.pdf` as a LinkedIn document or the native exports `assets/revenue-overview.png` and `assets/data-quality.png`. The separately labelled `*-preview.png` files are independent reference renders. Review the caption before posting.
