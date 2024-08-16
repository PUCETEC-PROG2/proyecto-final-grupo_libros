from django.urls import path
from . import views

app_name = "libreria"
urlpatterns = [
    path("", views.index, name="index"),
    path("category/", views.list_category, name="list_category"),
    path("category/add_category/", views.add_category, name="add_category"),
    path("category/edit_category/<int:category_id>/", views.edit_category, name="edit_category"),
    path("category/delete_category/<int:category_id>/", views.delete_category, name="delete_category"),
    path("client/", views.list_client, name="list_client"),
    path("client/<int:client_id>/", views.client, name="client"),
    path("client/add_client/", views.add_client, name="add_client"),
    path("client/edit_client/<int:id>/", views.edit_client, name="edit_client"),
    path("client/delete_client/<int:id>/", views.delete_client, name="delete_client"),
    path("product/", views.list_product, name="list_product"),
    path("product/<int:product_id>/", views.product, name="product"),
    path("product/add_product/", views.add_product, name="add_product"),
    path("product/edit_product/<int:product_id>/", views.edit_product, name="edit_product"),
    path("product/delete_product/<int:product_id>/", views.delete_product, name="delete_product"),
    path("purchase/", views.list_purchase, name="list_purchase"),
    path("purchase/add_purchase/", views.add_purchase, name="add_purchase"),
    path("purchase/<int:purchase_id>/", views.purchase, name="purchase"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
]
