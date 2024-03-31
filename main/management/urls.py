from django.urls import path
from .views import (
    MedicalHistoryListView,
    MedicalHistoryDetailsView,
    MedicalHistoryCreateView,
    MedicalHistoryUpdateView,
    MedicalHistoryDeleteView,

    

    TestResultListAPIView,
    TestResultDetailAPIView,
    TestResultCreateAPIView,
    TestResultUpdateAPIView,
    TestResultDeleteAPIView,

    InsuranceList, 
    InsuranceDetail,
    InsuranceCreate,
    InsuranceUpdate,
    InsuranceDelete

)


urlpatterns = [
    path('medical-histories/', MedicalHistoryListView.as_view(), name='medical-history-list'),
    path('medical-histories/<int:pk>/', MedicalHistoryDetailsView.as_view(), name='medical-history-details'),
    path('medical-histories/create/', MedicalHistoryCreateView.as_view(), name='medical-history-create'),
    path('medical-histories/<int:pk>/update/', MedicalHistoryUpdateView.as_view(), name='medical-history-update'),
    path('medical-histories/<int:pk>/delete/', MedicalHistoryDeleteView.as_view(), name='medical-history-delete'),

    

    path('test-results/', TestResultListAPIView.as_view(), name='testresult-list'),
    path('test-results/<int:pk>/', TestResultDetailAPIView.as_view(), name='testresult-detail'),
    path('test-results/upload/', TestResultCreateAPIView.as_view(), name='testresult-create'),
    path('test-results/<int:pk>/update/', TestResultUpdateAPIView.as_view(), name='testresult-update'),
    path('test-results/<int:pk>/delete/', TestResultDeleteAPIView.as_view(), name='testresult-delete'),

    path('insurance/', InsuranceList.as_view(), name='insurance-list'),
    path('insurance/<int:pk>/', InsuranceDetail.as_view(), name='insurance-detail'),
    path('insurance/create/', InsuranceCreate.as_view(), name='insurance-create'),
    path('insurance/<int:pk>/update/', InsuranceUpdate.as_view(), name='insurance-update'),
    path('insurance/<int:pk>/delete/', InsuranceDelete.as_view(), name='insurance-delete'),

]