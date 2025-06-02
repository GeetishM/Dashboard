from django.shortcuts import render
from .models import BudgetData, BudgetDataOther, PrRelPendLive, PrEnqStatusLive, PendPoStatusLive

def home(request):
    return render(request, 'management_report/home.html')

# --- Budget Analysis Views ---

def shop_wise_budget(request):
    # Main: Store-Spares
    queryset_main = (
        BudgetData.objects
        .order_by('gjahr', 'shop')
        .values('shop', 'budget', 'opitems', 'invoice', 'av_budget', 'gjahr')
        .distinct()
    )
    data_main = [
        row for row in queryset_main
        if row['shop'] and (
            row['budget'] or row['opitems'] or row['invoice'] or row['av_budget']
        )
    ]
    year_list_main = sorted(set(row['gjahr'] for row in data_main))

    # Main: Other Services
    queryset_other = (
        BudgetDataOther.objects
        .order_by('gjahr', 'shop')
        .values('shop', 'budget', 'opitems', 'invoice', 'av_budget', 'gjahr')
        .distinct()
    )
    data_other = [
        row for row in queryset_other
        if row['shop'] and (
            row['budget'] or row['opitems'] or row['invoice'] or row['av_budget']
        )
    ]
    year_list_other = sorted(set(row['gjahr'] for row in data_other))

    return render(request, 'management_report/shop_wise.html', {
        'data_main': data_main,
        'year_list_main': year_list_main,
        'data_other': data_other,
        'year_list_other': year_list_other,
    })

def fund_wise(request):
    queryset = BudgetData.objects.all().order_by('gjahr', 'fonds')
    year_list = sorted(set(queryset.values_list('gjahr', flat=True)))
    data = list(queryset.values(
        'fonds', 'budget', 'opitems', 'invoice', 'av_budget', 'gjahr'
    ))
    return render(request, 'management_report/fund_wise.html', {
        'data': data,
        'year_list': year_list,
    })

def commitment_item_wise(request):
    queryset = BudgetData.objects.all().order_by('gjahr', 'citem')
    year_list = sorted(set(queryset.values_list('gjahr', flat=True)))
    data = list(queryset.values(
        'citem', 'budget', 'opitems', 'invoice', 'av_budget', 'gjahr'
    ))
    return render(request, 'management_report/commitment_item_wise.html', {
        'data': data,
        'year_list': year_list,
    })

# --- Purchase Status Views ---

def pr_created_release_pending(request):
    queryset = PrRelPendLive.objects.all().order_by('pur_grp_grp')
    data = []
    for row in queryset:
        data.append({
            'pur_grp_grp': row.pur_grp_grp or '',
            'item_value': row.item_value or 0,
            'pr_value': row.pr_value or 0,
        })
    return render(request, 'management_report/pr_created_release_pending.html', {
        'data': data,
    })

def pr_released_enquiry_pending(request):
    queryset = PrEnqStatusLive.objects.all().order_by('pur_grp_grp')
    data = []
    for row in queryset:
        data.append({
            'pur_grp_grp': row.pur_grp_grp or '',
            'pr_value': row.pr_value or 0,
        })
    return render(request, 'management_report/pr_released_enquiry_pending.html', {
        'data': data,
    })

def enquiry_created_po_pending(request):
    return render(request, 'management_report/enquiry_created_po_pending.html')

def po_delivery_pending(request):
    queryset = PendPoStatusLive.objects.all().order_by('pur_grp_grp')
    data = []
    for row in queryset:
        data.append({
            'pur_grp_grp': row.pur_grp_grp or '',
            'po_value': row.item_value or 0,
            'delivery_status': row.mat_desc or '',
        })
    return render(request, 'management_report/po_delivery_pending.html', {
        'data': data,
    })

def po_dp_next_30_days(request):
    queryset = PendPoStatusLive.objects.exclude(shop__isnull=True).exclude(shop__exact='').order_by('shop')
    data = []
    for row in queryset:
        data.append({
            'shop': row.shop,
            'item_value': row.item_value or 0,
        })
    return render(request, 'management_report/po_dp_next_30_days.html', {
        'data': data,
    })

def po_dp_expired(request):
    queryset = (
        PendPoStatusLive.objects
        .exclude(pur_grp_grp__isnull=True)
        .exclude(pur_grp_grp__exact='')
        .order_by('pur_grp_grp')
        .values('pur_grp_grp')
        .distinct()
    )
    data = []
    for row in queryset:
        # Get the first item_value for each pur_grp_grp (or aggregate as needed)
        item = (
            PendPoStatusLive.objects
            .filter(pur_grp_grp=row['pur_grp_grp'])
            .first()
        )
        data.append({
            'pur_grp_grp': row['pur_grp_grp'],
            'item_value': item.item_value if item and item.item_value else 0,
        })
    return render(request, 'management_report/po_dp_expired.html', {
        'data': data,
    })

# --- Reports ---

def stock_position(request):
    return render(request, 'management_report/stock_position.html')