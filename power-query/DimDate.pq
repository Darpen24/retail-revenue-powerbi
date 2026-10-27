let
    Dates = Table.FromList(List.Dates(#date(2011,1,1), 334, #duration(1,0,0,0)), Splitter.SplitByNothing(), {"Date"}),
    Typed = Table.TransformColumnTypes(Dates, {{"Date", type date}}),
    Month = Table.AddColumn(Typed, "Month", each Date.ToText([Date], "yyyy-MM"), type text),
    MonthName = Table.AddColumn(Month, "MonthName", each Date.ToText([Date], "MMM", "en-GB"), type text),
    MonthNo = Table.AddColumn(MonthName, "MonthNo", each Date.Month([Date]), Int64.Type)
in
    MonthNo
