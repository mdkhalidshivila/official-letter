from unicodedata import name
from django.urls import path
from . import views
from .views import EmailAttachementView, GeneratePdfView, RelivingEmailAttachementView, AppreciationEmailAttachementView

urlpatterns = [
    path('index/', views.index, name = 'index'),
    path("register/", views.register_request, name="register"),
    path("", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path(r'^delete/<id>/', views.deleteView, name = 'deleteView'),
    path(r'^delete_candidates/<id>/', views.delete, name = 'delete'),
    # path('update/<int:id>/', views.updateView, name = 'updateView'),
    path(r'^updatedata/<id>/', views.updatedata, name="updatedata"),
    path('bill-form/', views.formView, name = 'formView'),
    path('direct-form/', views.directmailView, name = 'directmailView'),
    path('success/', views.success, name = 'success'),
    path('reexp-form/', views.reexpView, name = 'reexpView'),
    path('reexp/', views.reexp, name = 'reexp'),
    path(r'^pdf/<id>/', views.pdf, name='pdf'),
    path(r'^exp_pdf/<id>/', views.exp_pdf, name='exp_pdf'),
    path(r'^offer_pdf/<id>/', views.offer_pdf, name='offer_pdf'),
    path('emailattachment/', EmailAttachementView.as_view(), name='emailattachment'),
    path('relivingemailattachment/', RelivingEmailAttachementView.as_view(), name='relivingemailattachment'),
    path('appreciationemailattachment/', AppreciationEmailAttachementView.as_view(), name='appreciationemailattachment'),
    path(r'^sendemaildirect/<id>/', views.sendemaildirect, name ='sendemaildirect'),
    path('pdf/', GeneratePdfView.as_view(), name='generatepdf'),
    path('export_to_excel/', views.export_data_excel, name= 'export_to_excel'),
    path(r'^linkemail/<id>/', views.linkemail, name="linkemail"),
    # path('attachpdf/<int:id>/', views.attachpdf, name="attachpdf"),
    path('SearchView/', views.SearchView, name='SearchView'),
    path('EmployeeSearchView/', views.employeeSearchView, name='employeeSearchView'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('appreciation-form/', views.appreciationView, name = 'appreciationView'),
    path('appreciate/', views.appreciation, name = 'appreciate'),
    path(r'^appreciation_pdf/<id>/', views.appreciation_pdf, name='appreciation_pdf'),  
]