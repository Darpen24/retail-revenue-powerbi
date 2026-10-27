let
    Source = ScopedRetail,
    Date = Table.AddColumn(Source, "Date", each Date.From([InvoiceDate]), type date),
    Kind = Table.AddColumn(Date, "LineType", each if [Quantity] < 0 then "Credit" else "Sale", type text),
    Gross = Table.AddColumn(Kind, "GrossValue", each if [Quantity] > 0 then [Quantity] * [UnitPrice] else 0, Currency.Type),
    Credits = Table.AddColumn(Gross, "CreditValue", each if [Quantity] < 0 then -[Quantity] * [UnitPrice] else 0, Currency.Type),
    Net = Table.AddColumn(Credits, "NetValue", each [Quantity] * [UnitPrice], Currency.Type),
    Renamed = Table.RenameColumns(Net, {{"CustomerID", "CustomerKey"}}),
    Selected = Table.SelectColumns(Renamed, {"InvoiceNo", "StockCode", "CustomerKey", "Country", "Date", "Quantity", "UnitPrice", "LineType", "GrossValue", "CreditValue", "NetValue"})
in
    Selected
