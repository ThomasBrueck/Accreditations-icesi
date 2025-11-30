from django.urls import path
from . import views


urlpatterns = [
    path('user-dashboard/', views.UserDashboardView.as_view(), name='dashboard-user'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='dashboard-admin'),
    path('assign-role/', views.AssignRoleView.as_view(), name='assign-role-view'),
    path('remove-role/', views.RemoveRoleView.as_view(), name='remove-role-view'),
    path('reports/', views.ReportListView.as_view(), name='report-list'),
    path('reports/create-report/', views.ReportCreateView.as_view(), name='create-report'),
    path('reports/<int:pk>/edit/', views.ReportUpdateView.as_view(), name='update-report'),
    path('reports/<int:pk>/delete/', views.ReportDeleteView, name='delete-report'),
    path('reports/<int:pk>/view/', views.ReportFactorView.as_view(), name='view-report'),
    path('factors/<int:factor_id>/comments/', views.CommentsListView.as_view(), name='comments-list'),
    path('factors/<int:factor_id>/comments/create/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:comment_id>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:comment_id>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('comments/<int:comment_id>/detail/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('factors/<int:factor_id>/comments/review/', views.CommentsReviewListView.as_view(), name='comments-review-list'),
    path('comments/<int:comment_id>/review/', views.CommentReviewView.as_view(), name='comment-review'),
    path('comments/<int:comment_id>/justification/', views.JustificationDetailView.as_view(), name='justification-detail'),
    path('factors/<int:factor_id>/characteristics/', views.CharacteristicManageView.as_view(), name='characteristic-manage'),
    path('factors/<int:factor_id>/characteristics/create/', views.CharacteristicCreateView.as_view(), name='characteristic-create'),
    path('factors/<int:factor_id>/characteristics/<int:characteristic_id>/update/', views.CharacteristicUpdateView.as_view(), name='characteristic-update'),
    path('factors/<int:factor_id>/characteristics/<int:characteristic_id>/delete/', views.CharacteristicDeleteView.as_view(), name='characteristic-delete'),
    path('factors/<int:factor_id>/characteristics/upload/', views.CharacteristicUploadCSVView.as_view(), name='characteristic-upload'),
    path('factors/<int:factor_id>/characteristics/confirm/', views.CharacteristicConfirmView.as_view(), name='characteristic-confirm'),
    path('notifications/mark-read/', views.MarkNotificationsReadView.as_view(), name='mark_notifications_read'),
    path('profile/', views.profile_view, name='profile-view'),
    path('factors/<int:factor_id>/edit/', views.FactorUpdateView.as_view(), name='edit-factor'),
    path('profile/edit/', views.edit_profile_view, name='edit-profile-view'),
    path('factors/<int:factor_id>/questions/', views.QuestionManageView.as_view(), name='question-manage'),
    path('factors/<int:factor_id>/questions/create/', views.QuestionCreateView.as_view(), name='question-create'),
    path('tasks/assign/', views.TaskAssignView.as_view(), name='task-assign'),
    path('factors/<int:factor_id>/edit-collaborative/', views.FactorCollaborativeEditView.as_view(), name='edit-factor-collaborative'),
    path('send-notification/', views.SendAccreditationNotificationView.as_view(), name='send_notification'),
    path('notification-history/', views.NotificationHistoryView.as_view(), name='notification_history'),
    path('start-accreditation/', views.StartAccreditationProcessView.as_view(), name='start-accreditation'),
    path('get-accreditation-status/', views.GetAccreditationStatusView.as_view(), name='get_accreditation_status'),
    # ... New routes
    path('factor/<int:factor_id>/characteristic/<int:characteristic_id>/develop/', views.CharacteristicDevelopView.as_view(), name='characteristic-develop'),
    path('factor/<int:factor_id>/characteristic/<int:characteristic_id>/complete/', views.CharacteristicCompleteView.as_view(), name='characteristic-complete'),
    path('factor/<int:factor_id>/characteristic/<int:characteristic_id>/details/', views.CharacteristicDetailsView.as_view(), name='characteristic-details'),
    path('dofa/generate/', views.DOFADocumentView.as_view(), name='generate-dofa'),
    # ... New routes
]

