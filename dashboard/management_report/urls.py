from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),  # <-- root URL goes to home page
    # Budget Analysis
    path('shop-wise/', views.shop_wise_budget, name='shop_wise'),
    path('fund-wise/', views.fund_wise, name='fund_wise'),
    path('commitment-item-wise/', views.commitment_item_wise, name='commitment_item_wise'),

    # Purchase Status
    path('pr-created-release-pending/', views.pr_created_release_pending, name='pr_created_release_pending'),
    path('pr-released-enquiry-pending/', views.pr_released_enquiry_pending, name='pr_released_enquiry_pending'),
    path('enquiry-created-po-pending/', views.enquiry_created_po_pending, name='enquiry_created_po_pending'),
    path('po-delivery-pending/', views.po_delivery_pending, name='po_delivery_pending'),
    path('po-dp-next-30-days/', views.po_dp_next_30_days, name='po_dp_next_30_days'),
    path('po-dp-expired/', views.po_dp_expired, name='po_dp_expired'),

    # Reports
    path('stock-position/', views.stock_position, name='stock_position'),
]
