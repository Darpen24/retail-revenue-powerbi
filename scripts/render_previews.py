"""Create clearly labelled reference renders from independently verified metrics.

These are shareable data previews, not screenshots of Power BI Desktop.
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'docs/verified-metrics.json').read_text())
BG='#F2F5F8'; INK='#143247'; MUTED='#607584'; TEAL='#0D9488'; BLUE='#395C8A'; GOLD='#D69531'; GRID='#E5EBEF'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,'axes.labelcolor':MUTED,'xtick.color':MUTED,'ytick.color':MUTED})

def base(title,subtitle):
    f=plt.figure(figsize=(16,10),dpi=160,facecolor=BG)
    f.text(.035,.944,title,fontsize=24,fontweight='bold')
    f.text(.035,.909,subtitle,fontsize=11,color=MUTED)
    f.text(.035,.028,'DARPEN BHANDARI  /  UCI Online Retail · Chen (2015) · CC BY 4.0',fontsize=8,color=MUTED)
    f.text(.965,.028,'Reference render · Power BI project included',ha='right',fontsize=8,color=MUTED)
    return f

def panel(f,rect,title):
    x,y,w,h=rect
    f.add_artist(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.005,rounding_size=0.008',facecolor='white',edgecolor='none',transform=f.transFigure,zorder=0))
    f.text(x+.016,y+h-.033,title,fontsize=12,fontweight='bold')
    ax=f.add_axes([x+.055,y+.055,w-.078,h-.112],facecolor='white')
    ax.spines[['top','right','left']].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(axis='both',length=0,pad=9)
    return ax

def kpi(f,x,w,label,value,sub=None):
    f.add_artist(FancyBboxPatch((x,.76),w,.111,boxstyle='round,pad=0.005,rounding_size=0.008',facecolor='white',edgecolor='none',transform=f.transFigure,zorder=0))
    f.text(x+.015,.843,label,fontsize=9,color=MUTED,fontweight='bold')
    f.text(x+.015,.792,value,fontsize=25,fontweight='bold',color=INK)
    if sub: f.text(x+.015,.77,sub,fontsize=8,color=MUTED)

k=d['kpis']; months=[r['Month'][-2:] for r in d['monthly']]
labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov']
f=base('RETAIL / REVENUE INTELLIGENCE','Commercial performance  •  January–November 2011  •  GBP  •  Historical public data')
for i,(label,value) in enumerate([('NET SALES',f"£{k['net_sales']/1e6:.2f}m"),('SALES ORDERS',f"{k['orders']:,}"),('AVG. GROSS ORDER',f"£{k['aov']:,.2f}"),('KNOWN CUSTOMERS',f"{k['known_customers']:,}"),('CREDIT / GROSS',f"{k['credit_value_ratio']:.2%}")]):
    kpi(f,.035+i*.19,.17,label,value)
ax=panel(f,(.035,.365,.575,.36),'Monthly sales | gross vs net')
x=list(range(11)); gross=[r['GrossValue']/1e6 for r in d['monthly']]; net=[r['NetValue']/1e6 for r in d['monthly']]
ax.plot(x,gross,color=BLUE,lw=2,ls='--',label='Gross sales')
ax.plot(x,net,color=TEAL,lw=3,marker='o',ms=4,label='Net sales')
ax.fill_between(x,net,alpha=.07,color=TEAL)
ax.set_xticks(x,labels);ax.set_ylim(0,1.7);ax.set_yticks([0,.5,1,1.5]);ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'£{v:.1f}m'))
ax.grid(axis='y',color=GRID,zorder=0);ax.legend(frameon=False,loc='upper left',fontsize=9,ncol=2)
ax=panel(f,(.635,.365,.33,.36),'Net sales | domestic vs international')
uk=d['uk_net_sales'];total=k['net_sales']
ax.set_position([.682,.418,.235,.222]);ax.axis('off')
ax.pie([uk,total-uk],colors=[TEAL,BLUE],startangle=90,counterclock=False,wedgeprops={'width':.24,'edgecolor':'white','linewidth':3})
ax.text(0,.04,f'{uk/total:.1%}',ha='center',fontsize=26,fontweight='bold')
ax.text(0,-.29,'UK share',ha='center',fontsize=10,color=MUTED)
f.text(.669,.392,'● United Kingdom',fontsize=9,color=TEAL);f.text(.825,.392,'● International',fontsize=9,color=BLUE)
ax=panel(f,(.035,.078,.575,.252),'International markets | top 5 by net sales')
pos = ax.get_position(); ax.set_position([pos.x0+.025,pos.y0,pos.width-.025,pos.height])
cs=[(c,v) for c,v in d['top_countries'].items() if c!='United Kingdom'][:5]
ax.barh([c for c,v in cs][::-1],[v/1000 for c,v in cs][::-1],color=TEAL,height=.58)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'£{v:,.0f}k'));ax.grid(axis='x',color=GRID);ax.set_axisbelow(True)
for i,(c,v) in enumerate(cs[::-1]):ax.text(v/1000+3,i,f'£{v/1000:,.0f}k',va='center',fontsize=9)
ax.set_xlim(0,310)
f.add_artist(FancyBboxPatch((.635,.078),.33,.252,boxstyle='round,pad=0.005,rounding_size=0.008',facecolor='#E4EEF2',edgecolor='none',transform=f.transFigure,zorder=0))
f.text(.653,.291,'WHAT TO LOOK AT',fontsize=12,fontweight='bold')
f.text(.653,.258,'November is the strongest sales month.\nThe UK contributes 83.2% of net sales.\nCustomer IDs cover 84.9% of gross sales.',fontsize=12,linespacing=1.8,va='top')
f.text(.653,.112,'Credit notes include cancellations and adjustments.\nThe ratio is not a physical product return rate.',fontsize=9,color=MUTED,linespacing=1.5)
f.savefig(ROOT/'assets/revenue-overview-preview.png',facecolor=BG)
plt.close(f)

a=d['audit'];f=base('TRUST / THE NUMBERS','Power Query audit trail  •  Full source → validated reporting scope  •  No silent removal of unknown customers')
for i,(label,value) in enumerate([('SOURCE ROWS',a['source_rows']),('INVALID ROWS EXCLUDED',a['invalid_rows']),('EXACT DUPLICATES REMOVED',a['duplicates_removed']),('ROWS IN REPORT',a['rows_loaded'])]):
    kpi(f,.035+i*.24,.22,label,f'{value:,}')
ax=panel(f,(.035,.365,.45,.36),'Row reconciliation | every exclusion accounted for')
ax.axis('off')
rows=[('Source workbook',a['source_rows']),('− Invalid lines',a['invalid_rows']),('− Exact duplicate records',a['duplicates_removed']),('− Outside Jan–Nov 2011',a['outside_period']),('= Reporting rows',a['rows_loaded'])]
for i,(label,v) in enumerate(rows):
    yy=.89-i*.195
    ax.text(-.08,yy,label,transform=ax.transAxes,fontsize=12,fontweight='bold' if i==4 else 'normal')
    ax.text(1.02,yy,f'{v:,}',ha='right',transform=ax.transAxes,fontsize=13,fontweight='bold',color=TEAL if i==4 else INK)
ax=panel(f,(.51,.365,.455,.36),'Credit value | month of credit note')
ax.bar(x,[r['CreditValue']/1000 for r in d['monthly']],color=GOLD,width=.63)
ax.set_xticks(x,labels);ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'£{v:.0f}k'));ax.grid(axis='y',color=GRID);ax.set_axisbelow(True)
ticklabels = ax.get_xticklabels()
for xx in [1,2,4,5,7,8,10]: ticklabels[xx].set_visible(False)
for x0,w,title,body in [(.035,.29,'01  POWER QUERY','Explicit data types and text cleanup.\nInvalid-row rules and exact deduplication.\nComplete-month scope and derived values.'),(.365,.29,'02  MODEL + DAX','Sales fact + date, country, product dimensions.\nSingle-direction relationships.\nMeasures define sales, orders and credit ratios.'),(.695,.27,'03  INTERPRETATION','Unknown IDs remain in revenue.\nDuplicates assumed repeated records.\nNo cost data: no profit claim.')]:
    f.add_artist(FancyBboxPatch((x0,.078),w,.252,boxstyle='round,pad=0.005,rounding_size=0.008',facecolor='#E4EEF2',edgecolor='none',transform=f.transFigure,zorder=0))
    f.text(x0+.016,.289,title,fontsize=12,fontweight='bold')
    f.text(x0+.016,.248,body,fontsize=10,linespacing=1.9,va='top')
f.savefig(ROOT/'assets/data-quality-preview.png',facecolor=BG)
plt.close(f)
print('Two reference previews rendered')
