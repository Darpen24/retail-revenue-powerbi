let
    Valid = Table.SelectRows(PreparedRetail, each [ValidationStatus] = "Valid"),
    OriginalFields = Table.RemoveColumns(Valid, {"ValidationStatus"}),
    Deduplicated = Table.Distinct(Table.Buffer(OriginalFields)),
    CompleteMonths = Table.SelectRows(Deduplicated, each [InvoiceDate] >= #datetime(2011,1,1,0,0,0) and [InvoiceDate] < #datetime(2011,12,1,0,0,0))
in
    CompleteMonths
