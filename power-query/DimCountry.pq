let
    Countries = Table.Distinct(Table.SelectColumns(ScopedRetail, {"Country"})),
    Market = Table.AddColumn(Countries, "Market", each if [Country] = "United Kingdom" then "United Kingdom" else "International", type text)
in
    Market
