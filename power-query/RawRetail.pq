let
    Workbook = Excel.Workbook(File.Contents(SourceFile), null, true),
    Sheet = Workbook{[Item="Online Retail", Kind="Sheet"]}[Data],
    Headers = Table.PromoteHeaders(Sheet, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"InvoiceNo", type text}, {"StockCode", type text}, {"Description", type text}, {"Quantity", Int64.Type}, {"InvoiceDate", type datetime}, {"UnitPrice", Currency.Type}, {"CustomerID", type text}, {"Country", type text}}, "en-GB")
in
    Typed
