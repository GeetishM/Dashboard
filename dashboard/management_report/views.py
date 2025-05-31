from django.shortcuts import render
from .models import BudgetData, BudgetDataOther, PrRelPendLive

def home(request):
    return render(request, 'management_report/home.html')

# --- Budget Analysis Views ---

def shop_wise_budget(request):
    data = BudgetData.objects.all()
    return render(request, 'management_report/shop_wise.html', {'data': data})

def fund_wise(request):
    return render(request, 'management_report/fund_wise.html',{'data': data})

def commitment_item_wise(request):
    data = BudgetData.objects.all()
    return render(request, 'management_report/commitment_item_wise.html', {'data': data})


# --- Purchase Status Views ---

def pr_created_release_pending(request):
    return render(request, 'management_report/pr_created_release_pending.html')

def pr_released_enquiry_pending(request):
    return render(request, 'management_report/pr_released_enquiry_pending.html')

def enquiry_created_po_pending(request):
    return render(request, 'management_report/enquiry_created_po_pending.html')

def po_delivery_pending(request):
    return render(request, 'management_report/po_delivery_pending.html')

def po_dp_next_30_days(request):
    return render(request, 'management_report/po_dp_next_30_days.html')

def po_dp_expired(request):
    return render(request, 'management_report/po_dp_expired.html')


# --- Reports ---

def stock_position(request):
    return render(request, 'management_report/stock_position.html')


def shop_wise_budget(request):
    queryset = BudgetData.objects.all().order_by('gjahr', 'shop')
    year_list = sorted(set(queryset.values_list('gjahr', flat=True)))

    # Convert queryset to list of dictionaries for JSON serialization
    data = list(queryset.values(
        'shop', 'budget', 'opitems', 'invoice', 'av_budget', 'gjahr'
    ))

    return render(request, 'management_report/shop_wise.html', {
        'data': data,
        'year_list': year_list,
    })

def fund_wise(request):
    queryset = BudgetData.objects.all().order_by('gjahr', 'fonds')
    year_list = sorted(set(queryset.values_list('gjahr', flat=True)))

    # Convert queryset to list of dictionaries for JSON serialization
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

    # Convert queryset to list of dictionaries for JSON serialization
    data = list(queryset.values(
        'citem', 'budget', 'opitems', 'invoice', 'av_budget', 'gjahr'
    ))

    return render(request, 'management_report/commitment_item_wise.html', {
        'data': data,
        'year_list': year_list,
    })

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