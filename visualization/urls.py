from django.urls import path

from . import views

app_name = 'visualization'
urlpatterns = [
    path('', views.index, name='index'),
    path('echarts/', views.echarts, name='echarts'),
    path('edit/', views.edit, name='edit'),
    path('save_path_info/', views.save_path_info, name='update_path'),
    path('test/', views.test, name='test'),
    path('road_loc/', views.road_loc, name='road_loc'),
    path('delete_seg/', views.delete_seg, name='delete_seg'),
    path('miss_price/', views.miss_price, name='miss_price'),
    path('use_rank/', views.use_rank, name='use_rank'),
    path('block_vote/', views.block_vote, name='block_vote'),
    path('aggregate_rates/', views.aggregate_rates, name='aggregate_rates'),
    path('get_aggregate_rates_data/', views.get_aggregate_rates_data, name='get_aggregate_rates_data'),
    path('block_rate/', views.block_rate, name='block_rate'),
    path('parking_proportion/', views.parking_proportion_and_future, name='parking_proportion'),
    path('draw_sum_up_pie/', views.draw_sum_up_pie, name='draw_sum_up_pie'),
    path('draw_road_predict/', views.draw_road_predict, name='draw_road_predict'),
]
