let
    Raw = Table.Buffer(RawRetail),
    Prepared = Table.Buffer(PreparedRetail),
    Valid = Table.SelectRows(Prepared, each [ValidationStatus] = "Valid"),
    Unique = Table.Distinct(Table.Buffer(Table.RemoveColumns(Valid, {"ValidationStatus"}))),
    Scope = ScopedRetail,
    Audit = #table(type table [Step=text, Rows=Int64.Type], {
        {"01 Source rows", Table.RowCount(Raw)},
        {"02 Invalid rows excluded", Table.RowCount(Prepared) - Table.RowCount(Valid)},
        {"03 Exact duplicates removed", Table.RowCount(Valid) - Table.RowCount(Unique)},
        {"04 Outside Jan-Nov 2011", Table.RowCount(Unique) - Table.RowCount(Scope)},
        {"05 Rows loaded", Table.RowCount(Scope)},
        {"06 Unidentified customer rows", Table.RowCount(Table.SelectRows(Scope, each [CustomerID] = "Unknown"))}
    })
in
    Audit
