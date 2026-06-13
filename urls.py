from django.urls import path
from . import views

urlpatterns = [
    # Sub-Allotment Advice
    path('',                       views.index,           name='index'),
    path('new/',                   views.create_advice,   name='create_advice'),
    path('<int:pk>/',              views.detail_advice,   name='detail_advice'),
    path('<int:pk>/edit/',         views.edit_advice,     name='edit_advice'),
    path('<int:pk>/delete/',       views.delete_advice,   name='delete_advice'),

    # Allotment Statement
    path('allotment/',                   views.allotment_list,    name='allotment_list'),
    path('allotment/new/',               views.allotment_create,  name='allotment_create'),
    path('allotment/<int:pk>/edit/',     views.allotment_edit,    name='allotment_edit'),
    path('allotment/<int:pk>/delete/',   views.allotment_delete,  name='allotment_delete'),

    # Master Lists Management
    path('master-lists/', views.master_lists, name='master_lists'),

    # Master Table APIs
    path('api/gaa/',              views.api_get_gaa,           name='api_gaa'), 
    path('api/object-codes/',     views.api_get_object_codes,  name='api_object_codes'),
    path('api/descriptions/',     views.api_get_descriptions,  name='api_descriptions'),
    path('api/advice-numbers/',   views.api_get_advice_numbers,name='api_advice_numbers'),
    path('api/cis/',              views.api_get_cis,           name='api_cis'),
    path('api/save/',             views.api_save_item,         name='api_save'),
    path('api/delete/',           views.api_delete_item,       name='api_delete'),
    path('api/suballotment-records/', views.api_get_suballotment_records, name='api_suballotment_records'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('province/<str:office>/<str:province>/', views.province_table, name='province_table'),
    path('province/save/', views.save_province_table, name='save_province_table'),
]
