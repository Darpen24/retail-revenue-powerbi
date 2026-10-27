let
    Pairs = Table.SelectColumns(ScopedRetail, {"StockCode", "Description"}),
    Grouped = Table.Group(Pairs, {"StockCode"}, {{"Product", each List.First(List.Sort(List.Distinct([Description]))), type text}})
in
    Grouped
