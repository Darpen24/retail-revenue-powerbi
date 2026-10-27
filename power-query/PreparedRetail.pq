let
    Source = RawRetail,
    Trimmed = Table.TransformColumns(Source, {{"InvoiceNo", each if _ = null then "" else Text.Upper(Text.Trim(Text.Clean(_))), type text}, {"StockCode", each if _ = null then "" else Text.Upper(Text.Trim(Text.Clean(_))), type text}, {"Country", each if _ = null or Text.Trim(_) = "" then "Unknown" else Text.Trim(Text.Clean(_)), type text}, {"Description", each if _ = null or Text.Trim(_) = "" then "Unlabelled item" else Text.Trim(Text.Clean(_)), type text}, {"CustomerID", each if _ = null or Text.Trim(_) = "" then "Unknown" else Text.Trim(_), type text}}),
    WithStatus = Table.AddColumn(Trimmed, "ValidationStatus", each
        if [InvoiceNo] = "" or [StockCode] = "" or [InvoiceDate] = null then "Missing key/date"
        else if [UnitPrice] = null or [UnitPrice] <= 0 then "Non-positive price"
        else if [Quantity] = null or [Quantity] = 0 then "Zero/missing quantity"
        else if Text.StartsWith([InvoiceNo], "C") and [Quantity] > 0 then "Cancellation sign mismatch"
        else "Valid", type text)
in
    WithStatus
