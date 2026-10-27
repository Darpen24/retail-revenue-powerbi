"""Point the project at this checkout's workbook before opening Power BI."""
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
source=root/'data/raw/Online Retail.xlsx'
if not source.exists():
    raise SystemExit(f'Workbook not found: {source}')
expression='"'+str(source)+'" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'
path=root/'RetailRevenue.SemanticModel/model.bim'
if not path.exists():
    raise SystemExit('This model was converted to TMDL. Set SourceFile using Power BI Transform data > Manage Parameters instead.')
model=json.loads(path.read_text(encoding='utf-8'))
next(item for item in model['model']['expressions'] if item['name']=='SourceFile')['expression']=[expression]
path.write_text(json.dumps(model,indent=2,ensure_ascii=False),encoding='utf-8')
(root/'power-query/SourceFile.pq').write_text(expression+'\n',encoding='utf-8')
print(f'SourceFile configured: {source}')
