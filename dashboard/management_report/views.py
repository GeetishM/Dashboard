from django.shortcuts import render
from .models import BudgetData, BudgetDataOther, PrRelPendLive, PrEnqStatusLive, PendPoStatusLive

def home(request):
    return render(request, 'management_report/home.html')

# --- Budget Analysis Views ---

def shop_wise_budget(request):
    # Fetch all data from both tables, add 'type' for internal distinction
    store_spares = BudgetData.objects.all().values(
        'fonds', 'shop', 'budget', 'opitems', 'invoice', 'av_budget', 'gjahr', 'citem', 'fictr', 'fund_center'
    )
    store_spares = [
        {**row, 'type': 'STORE-SPARES'} for row in store_spares
    ]

    other_services = BudgetDataOther.objects.all().values(
        'fonds', 'shop', 'budget', 'opitems', 'invoice', 'av_budget', 'gjahr', 'citem', 'fictr', 'fund_center'
    )
    other_services = [
        {**row, 'type': 'OTHER-SERVICES'} for row in other_services
    ]

    # Merge both lists
    budget_data = store_spares + other_services

    # Prepare unique filter lists (from both tables)
    shop_list = sorted({row['shop'] for row in budget_data})
    fund_list = sorted({row['fonds'] for row in budget_data})
    citem_list = sorted({row['citem'] for row in budget_data})
    year_list = sorted({row['gjahr'] for row in budget_data})

    context = {
        'budget_data': budget_data,
        'shop_list': shop_list,
        'fund_list': fund_list,
        'citem_list': citem_list,
        'year_list': year_list,
    }
    return render(request, 'management_report/shop_wise.html', context)

def fund_wise(request):
    # Fetch data from both tables
    store_spares = BudgetData.objects.all().values(
        'fonds', 'budget', 'opitems', 'invoice', 'av_budget', 'gjahr'
    )
    other_services = BudgetDataOther.objects.all().values(
        'fonds', 'budget', 'opitems', 'invoice', 'av_budget', 'gjahr'
    )

    # Merge both lists
    data = list(store_spares) + list(other_services)

    # Prepare unique year list for filter
    year_list = sorted({row['gjahr'] for row in data})

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