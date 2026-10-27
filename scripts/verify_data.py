"""Independently reconcile the M transformation rules against the public workbook.

Python is a QA reference, not the data source for the Power BI semantic model.
"""
from pathlib import Path
import hashlib
import json
import argparse
import math

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true', help='Compare against committed metrics without rewriting them')
args = parser.parse_args()
source = ROOT / 'data/raw/Online Retail.xlsx'
raw = pd.read_excel(source, engine='openpyxl', dtype={'InvoiceNo':'str', 'StockCode':'str', 'CustomerID':'str'})
df = raw.copy()
for col in ['InvoiceNo','StockCode','Country','Description','CustomerID']:
    df[col] = df[col].str.replace(r'[\x00-\x1f]', '', regex=True).str.strip()
df['InvoiceNo'] = df.InvoiceNo.fillna('').str.upper()
df['StockCode'] = df.StockCode.fillna('').str.upper()
df['CustomerID'] = df.CustomerID.fillna('Unknown').replace('', 'Unknown')
df['Country'] = df.Country.fillna('Unknown').replace('', 'Unknown')
df['Description'] = df.Description.fillna('Unlabelled item').replace('', 'Unlabelled item')
df['UnitPrice'] = df.UnitPrice.round(4)
invalid = ((df.InvoiceNo == '') | (df.StockCode == '') | df.InvoiceDate.isna()
           | df.UnitPrice.isna() | (df.UnitPrice <= 0) | df.Quantity.isna() | (df.Quantity == 0)
           | (df.InvoiceNo.str.startswith('C') & (df.Quantity > 0)))
valid = df.loc[~invalid].copy()
unique = valid.drop_duplicates()
scope = unique.loc[(unique.InvoiceDate >= '2011-01-01') & (unique.InvoiceDate < '2011-12-01')].copy()
scope['NetValue'] = scope.Quantity * scope.UnitPrice
scope['GrossValue'] = scope.NetValue.where(scope.Quantity > 0, 0)
scope['CreditValue'] = -scope.NetValue.where(scope.Quantity < 0, 0)
scope['Month'] = scope.InvoiceDate.dt.strftime('%Y-%m')
gross, credit = float(scope.GrossValue.sum()), float(scope.CreditValue.sum())
orders = int(scope.loc[scope.Quantity>0, 'InvoiceNo'].nunique())
audit = {
    'source_rows':len(raw), 'invalid_rows':int(invalid.sum()),
    'duplicates_removed':len(valid)-len(unique), 'outside_period':len(unique)-len(scope),
    'rows_loaded':len(scope), 'unknown_customer_rows':int((scope.CustomerID=='Unknown').sum()),
}
assert audit['source_rows'] == sum(audit[key] for key in ['invalid_rows','duplicates_removed','outside_period','rows_loaded'])
assert abs(float(scope.NetValue.sum()) - (gross-credit)) < 0.01
assert scope.InvoiceDate.min() >= pd.Timestamp('2011-01-01')
assert scope.InvoiceDate.max() < pd.Timestamp('2011-12-01')
assert not scope.duplicated(subset=list(raw.columns)).any()
assert scope.UnitPrice.gt(0).all()
assert scope.groupby('Month').size().shape[0] == 11
monthly = scope.groupby('Month')[['GrossValue','CreditValue','NetValue']].sum().round(4).reset_index()
country = scope.groupby('Country').NetValue.sum().sort_values(ascending=False)
qa = {
    'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'period':'2011-01-01 to 2011-11-30', 'currency':'GBP', 'audit':audit,
    'kpis': {'gross_sales':round(gross,2),'credit_value':round(credit,2),'net_sales':round(gross-credit,2),
             'orders':orders,'aov':round(gross/orders,2),
             'known_customers':int(scope.loc[(scope.Quantity>0)&(scope.CustomerID!='Unknown'),'CustomerID'].nunique()),
             'credit_value_ratio':round(credit/gross,10),
             'identified_sales_share':round(float(scope.loc[scope.CustomerID!='Unknown','GrossValue'].sum()/gross),10)},
    'monthly':monthly.to_dict(orient='records'),
    'top_countries':country.head(10).round(2).to_dict(),
    'uk_net_sales':round(float(country.get('United Kingdom',0)),2),
}
if args.check:
    expected=json.loads((ROOT/'docs/verified-metrics.json').read_text(encoding='utf-8'))
    assert qa['source_sha256'] == expected['source_sha256'], 'Workbook checksum changed'
    assert qa['audit'] == expected['audit'], 'Row counts differ from committed baseline'
    for name,value in qa['kpis'].items():
        assert math.isclose(value, expected['kpis'][name], abs_tol=0.0001), f'KPI mismatch: {name}'
    for observed, reference in zip(qa['monthly'], expected['monthly'], strict=True):
        assert observed['Month'] == reference['Month']
        for name in ['GrossValue','CreditValue','NetValue']:
            assert math.isclose(observed[name],reference[name],abs_tol=0.0001)
    print('Workbook checksum, audit counts, KPIs, and monthly totals match the committed baseline')
else:
    (ROOT/'docs/verified-metrics.json').write_text(json.dumps(qa,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,indent=2))
