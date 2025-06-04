from django.shortcuts import render
from .models import BudgetData, BudgetDataOther, InventorySheet1, InventorySheet2, InventorySheet3,StockErp, PrRelPendLive, PrEnqStatusLive, PendPoStatusLive,  EnqPoPendingLive
import pandas as pd
from datetime import date

def home(request):
    return render(request, 'management_report/home.html')

# --- Budget Analysis Views ---

def shop_wise_budget(request):
    # Fetch all data from both tables, add 'type' for internal distinction
    store_spares = BudgetData.objects.all().values(
        'fonds', 'shop', 'budget', 'opitems', 'invoice', 'av_budget', 'gjahr', 'citem'
    )
    store_spares = [
        {**row, 'type': 'STORE-SPARES'} for row in store_spares
    ]

    other_services = BudgetDataOther.objects.all().values(
        'fonds', 'shop', 'budget', 'opitems', 'invoice', 'av_budget', 'gjahr', 'citem'
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

def get_fiscal_year(dt):
    if not dt:
        return ''
    year = dt.year
    if dt.month >= 4:
        return f"FY {year}-{str(year+1)[-2:]}"
    else:
        return f"FY {year-1}-{str(year)[-2:]}"

def pr_created_release_pending(request):
    queryset = (
        PrRelPendLive.objects
        .exclude(pur_grp_grp__isnull=True)
        .exclude(pur_grp_grp__exact='')
        .order_by('pur_grp_grp')
    )
    data = []
    pur_grp_grp_set = set()
    shop_set = set()
    fy_set = set()
    for row in queryset:
        fy = get_fiscal_year(row.pr_date)
        pur_grp_grp_set.add(row.pur_grp_grp or '')
        shop_set.add(row.shop or '')
        if fy:
            fy_set.add(fy)
        data.append({
            'pur_grp_grp': row.pur_grp_grp or '',
            'pur_grp': row.pur_grp or '',
            'fund_center': row.fund_center or '',
            'shop': row.shop or '',
            'pr_date': row.pr_date.strftime('%Y-%m-%d') if row.pr_date else '',
            'del_date': row.del_date.strftime('%Y-%m-%d') if row.del_date else '',
            'item_value': row.item_value or 0,
            'pr_value': float(row.pr_value or 0),
            'fiscal_year': fy,
            'rel_pend_with': row.rel_pend_with or '',
        })
    context = {
        'data': data,
        'pur_grp_grp_list': sorted(pur_grp_grp_set),
        'shop_list': sorted(shop_set),
        'fiscal_year_list': sorted(fy_set),  #if want the reverse order, use sorted(fy_set, reverse=True)
    }
    return render(request, 'management_report/pr_created_release_pending.html', context)

def pr_released_enquiry_pending(request):
    queryset = PrEnqStatusLive.objects.all().order_by('pur_grp_grp')
    data = []
    pur_grp_grp_set = set()
    shop_set = set()
    fy_pr_set = set()
    fy_enq_set = set()

    def get_fiscal_year(dt):
        if not dt:
            return ''
        year = dt.year
        if dt.month >= 4:
            return f"FY {year}-{str(year+1)[-2:]}"
        else:
            return f"FY {year-1}-{str(year)[-2:]}"

    for row in queryset:
        fy_pr = get_fiscal_year(row.pr_date)
        fy_enq = get_fiscal_year(row.enq_date)
        pur_grp_grp_set.add(row.pur_grp_grp or '')
        shop_set.add(row.shop or '')
        if fy_pr:
            fy_pr_set.add(fy_pr)
        if fy_enq:
            fy_enq_set.add(fy_enq)
        data.append({
            'pur_grp_grp': row.pur_grp_grp or '',
            'shop': row.shop or '',
            'fund_center': row.fund_center or '',
            'sug_mod_tend': row.sug_mod_tend or '',
            'pr_date': row.pr_date.strftime('%Y-%m-%d') if row.pr_date else '',
            'enq_date': row.enq_date.strftime('%Y-%m-%d') if row.enq_date else '',
            'pr_value': float(row.pr_value or 0),
            'fy_pr': fy_pr,
            'fy_enq': fy_enq,
        })
    context = {
        'data': data,
        'pur_grp_grp_list': sorted(pur_grp_grp_set),
        'shop_list': sorted(shop_set),
        'fy_pr_list': sorted(fy_pr_set),
        'fy_enq_list': sorted(fy_enq_set),
    }
    return render(request, 'management_report/pr_released_enquiry_pending.html', context)

def enquiry_created_po_pending(request):
    queryset = EnqPoPendingLive.objects.all().order_by('pur_grp_grp')
    data = []
    pur_grp_grp_set = set()
    fy_enq_set = set()

    for row in queryset:
        fy_enq = get_fiscal_year(row.enq_date)
        pur_grp_grp_set.add(row.pur_grp_grp or '')
        if fy_enq:
            fy_enq_set.add(fy_enq)
        data.append({
            'pur_grp_grp': row.pur_grp_grp or '',
            'enq_date': row.enq_date.strftime('%Y-%m-%d') if row.enq_date else '',
            'enq_pend_days': row.enq_pend_days or 0,
            'po_pend_days': row.po_pend_days or 0,
            'enq_mode': row.enq_mode or '',
            'pur_officer': row.pur_officer or '',
            'fy_enq': fy_enq,
        })
    context = {
        'data': data,
        'pur_grp_grp_list': sorted(pur_grp_grp_set),
        'fy_enq_list': sorted(fy_enq_set),
    }
    return render(request, 'management_report/enquiry_created_po_pending.html', context)

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
    # Fetch data from all three inventory tables
    inv1 = pd.DataFrame(list(InventorySheet1.objects.all().values('mat_no', 'mat_dsc', 'val_price')))
    inv2 = pd.DataFrame(list(InventorySheet2.objects.all().values('mat_no', 'mat_dsc', 'val_price')))
    inv3 = pd.DataFrame(list(InventorySheet3.objects.all().values('mat_no', 'mat_dsc', 'val_price')))

    # Concatenate
    combined_df = pd.concat([inv1, inv2, inv3], ignore_index=True)

    # Rename columns to match DB field names if needed
    combined_df.rename(columns={
        'mat_no': 'MAT_NO',
        'mat_dsc': 'MAT_DSC',
        'val_price': 'VAL_PRICE'
    }, inplace=True)

    if combined_df.empty:
        grouped = pd.DataFrame(columns=['MAT_GROUP', 'Count', 'Total_Value', 'Average_Value', 'Max_Value'])
    else:
        combined_df['MAT_GROUP'] = combined_df['MAT_NO'].astype(str).str[:3]
        grouped = combined_df.groupby('MAT_GROUP').agg(
            Count=('VAL_PRICE', 'count'),
            Total_Value=('VAL_PRICE', 'sum'),
            Average_Value=('VAL_PRICE', 'mean'),
            Max_Value=('VAL_PRICE', 'max')
        ).reset_index()
        grouped = grouped.sort_values(by='MAT_GROUP')

    mat_group_list = grouped['MAT_GROUP'].tolist()

    # --- Add this block for pie charts ---
    df = pd.DataFrame(list(StockErp.objects.all().values('mill', 'stock')))

    # Saleable Stock
    saleable_mills = ['MM', 'URM', 'RSMR', 'RSMS', 'BRM', 'WRM']
    saleable_df = df[df['mill'].isin(saleable_mills)]
    saleable_grouped = saleable_df.groupby('mill', as_index=False)['stock'].sum()
    saleable_total = saleable_grouped['stock'].sum()

    # Rollable Stock
    rollable_mills = ['SMS2', 'SMS3']
    rollable_df = df[df['mill'].isin(rollable_mills)]
    rollable_grouped = rollable_df.groupby('mill', as_index=False)['stock'].sum()
    rollable_total = rollable_grouped['stock'].sum()

    context = {
        'grouped_data': grouped.to_dict(orient='records'),
        'mat_group_list': mat_group_list,
        'saleable_labels': list(saleable_grouped['mill']),
        'saleable_data': list(saleable_grouped['stock']),
        'saleable_total': saleable_total,
        'rollable_labels': list(rollable_grouped['mill']),
        'rollable_data': list(rollable_grouped['stock']),
        'rollable_total': rollable_total,
    }
    return render(request, 'management_report/stock_position.html', context)

def stock_pie_charts(request):
    # Fetch all data
    df = pd.DataFrame(list(StockErp.objects.all().values('mill', 'stock')))

    # Saleable Stock
    saleable_mills = ['MM', 'URM', 'RSMR', 'RSMS', 'BRM', 'WRM']
    saleable_df = df[df['mill'].isin(saleable_mills)]
    saleable_grouped = saleable_df.groupby('mill', as_index=False)['stock'].sum()
    saleable_total = saleable_grouped['stock'].sum()

    # Rollable Stock
    rollable_mills = ['SMS2', 'SMS3']
    rollable_df = df[df['mill'].isin(rollable_mills)]
    rollable_grouped = rollable_df.groupby('mill', as_index=False)['stock'].sum()
    rollable_total = rollable_grouped['stock'].sum()

    context = {
        'saleable_labels': saleable_grouped['mill'].tolist(),
        'saleable_data': saleable_grouped['stock'].tolist(),
        'saleable_total': saleable_total,
        'rollable_labels': rollable_grouped['mill'].tolist(),
        'rollable_data': rollable_grouped['stock'].tolist(),
        'rollable_total': rollable_total,
    }
    return render(request, 'management_report/stock_pie_charts.html', context)