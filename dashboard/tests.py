from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from init.models import RoleModel
from dashboard.models import ReportModel, FactorModel, CommentsModel, QuestionModel, CharacteristicModel, NotificationModel, TaskModel
from dashboard.forms import ReportForm, FactorForm, QuestionForm, AnswerForm, CharacteristicForm, ProfileForm, TaskForm
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
import io

UserModel = get_user_model()

class UserDashboardViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")

    def test_user_dashboard_view_get(self):
        response = self.client.get(reverse('dashboard-user'))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/dashboard-user.html')

    def test_user_dashboard_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard-user'))
        self.assertRedirects(response, f"{reverse('login-user')}?next={reverse('dashboard-user')}")
        self.assertEqual(response.status_code, 302, f"Expected 302, got {response.status_code}.")

class AdminDashboardViewTest(TestCase):
    def setUp(self):
        self.admin = UserModel.objects.create_user(
            username='admin@u.icesi.edu.co',
            email='admin@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        self.admin.role = RoleModel.objects.create(name='acadi')
        self.admin.save()
        login_success = self.client.login(username='admin@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")

    def test_admin_dashboard_view_get(self):
        response = self.client.get(reverse('dashboard-admin'))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/dashboard-admin.html')

    def test_admin_dashboard_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard-admin'))
        self.assertRedirects(response, f"{reverse('login-user')}?next={reverse('dashboard-admin')}")
        self.assertEqual(response.status_code, 302, f"Expected 302, got {response.status_code}.")

class MarkNotificationsReadViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        NotificationModel.objects.create(
            title='Test Notification',
            user=self.user,
            created_by=self.user,
            is_read=False
        )

    def test_mark_notifications_read_post_authenticated(self):
        response = self.client.post(reverse('mark_notifications_read'))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}.")
        self.assertJSONEqual(response.content, {'status': 'success'})
        self.assertTrue(NotificationModel.objects.filter(user=self.user, is_read=True).exists(), "Notifications not marked as read.")

    #def test_mark_notifications_read_post_unauthenticated(self):
        #self.client.logout()
        #response = self.client.post(reverse('mark_notifications_read'))
        #self.assertEqual(response.status_code, 403, f"Expected 403, got {response.status_code}.")

class AssignRoleViewTest(TestCase):
    def setUp(self):
        self.acadi_role = RoleModel.objects.create(name='acadi')
        self.common_role = RoleModel.objects.create(name='common')
        self.admin = UserModel.objects.create_user(
            username='admin@u.icesi.edu.co',
            email='admin@u.icesi.edu.co',
            password='password@123',
            is_active=True,
            role=self.acadi_role
        )
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True,
            role=self.common_role
        )
        login_success = self.client.login(username='admin@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")

    def test_assign_role_get(self):
        response = self.client.get(reverse('assign-role-view'))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/assign_role.html')

    def test_assign_role_post_success(self):
        role = RoleModel.objects.create(name='program director')
        response = self.client.post(reverse('assign-role-view'), data={
            'user_id': self.user.id,
            'role_id': role.id,
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.role.name, 'program director', "Role assignment failed.")
        self.assertRedirects(response, reverse('assign-role-view'))

    def test_assign_role_post_failure(self):
        response = self.client.post(reverse('assign-role-view'), data={
            'user_id': self.user.id,
            'role_id': 'invalid',
        })
        self.assertRedirects(response, reverse('assign-role-view'))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1, "Expected one error message.")
        self.assertEqual(str(messages_list[0]), 'Usuario o rol no válidos.', f"Expected error message 'Usuario o rol no válidos.', got '{str(messages_list[0]) if messages_list else 'None'}'.")
        self.assertEqual(messages_list[0].level, messages.ERROR, "Expected ERROR message level.")

class RemoveRoleViewTest(TestCase):
    def setUp(self):
        self.acadi_role = RoleModel.objects.create(name='acadi')
        self.common_role = RoleModel.objects.create(name='common')
        self.admin = UserModel.objects.create_user(
            username='admin@u.icesi.edu.co',
            email='admin@u.icesi.edu.co',
            password='password@123',
            is_active=True,
            role=self.acadi_role
        )
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True,
            role=RoleModel.objects.create(name='program director')
        )
        login_success = self.client.login(username='admin@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")

    def test_remove_role_get(self):
        response = self.client.get(reverse('remove-role-view'))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/remove_role.html')

    #def test_remove_role_post(self):
        #response = self.client.post(reverse('remove-role-view'), data={
            #'user_id': self.user.id,
        #})
        #self.user.refresh_from_db()
        #self.assertEqual(self.user.role.name, 'common', "Role removal failed, expected 'common' role.")
        #self.assertRedirects(response, reverse('remove-role-view'))

    def test_remove_role_post_invalid_user(self):
        response = self.client.post(reverse('remove-role-view'), data={
            'user_id': 999,
        })
        self.assertRedirects(response, reverse('remove-role-view'))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1, "Expected one error message.")
        self.assertEqual(str(messages_list[0]), 'Usuario no válido.', f"Expected error message 'Usuario no válido.', got '{str(messages_list[0]) if messages_list else 'None'}'.")
        self.assertEqual(messages_list[0].level, messages.ERROR, "Expected ERROR message level.")

class ReportListViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        for i in range(10):
            ReportModel.objects.create(
                name=f'Report {i}',
                description='Test description',
                end_date=timezone.now().date() + timezone.timedelta(days=1),
                status='active',
                created_by=self.user
            )

    def test_report_list_view_get(self):
        response = self.client.get(reverse('report-list'))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/reports.html')
        self.assertContains(response, 'Report 0')

    def test_report_list_view_search(self):
        response = self.client.get(reverse('report-list'), {'search': 'Report 0'})
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertContains(response, 'Report 0')
        self.assertNotContains(response, 'Report 1')

    def test_report_list_view_filter(self):
        response = self.client.get(reverse('report-list'), {'status': 'active'})
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/reports.html')
        self.assertContains(response, 'Report 0')

    def test_report_list_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('report-list'))
        self.assertRedirects(response, f"{reverse('login-user')}?next={reverse('report-list')}")
        self.assertEqual(response.status_code, 302, f"Expected 302, got {response.status_code}.")

class ReportCreateViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")

    def test_report_create_get(self):
        response = self.client.get(reverse('create-report'))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/report-form.html')

    def test_report_create_post_valid(self):
        response = self.client.post(reverse('create-report'), {
            'name': 'New Report',
            'description': 'Test description',
            'start_date': timezone.now().date().strftime('%Y-%m-%d'),
            'end_date': (timezone.now().date() + timezone.timedelta(days=1)).strftime('%Y-%m-%d'),
            'status': 'active'
        })
        self.assertRedirects(response, reverse('report-list'))
        self.assertEqual(ReportModel.objects.count(), 1, "Report not created.")
        self.assertEqual(FactorModel.objects.count(), 12, "Expected 12 factors created.")

    def test_report_create_post_invalid(self):
        response = self.client.post(reverse('create-report'), {
            'name': '',
            'description': ''
        })
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/report-form.html')
        self.assertFalse(ReportModel.objects.exists(), "Report should not be created with invalid data.")

class ReportUpdateViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )

    def test_report_update_get(self):
        response = self.client.get(reverse('update-report', kwargs={'pk': self.report.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/report-form.html')

    def test_report_update_post_valid(self):
        response = self.client.post(reverse('update-report', kwargs={'pk': self.report.pk}), {
            'name': 'Updated Report',
            'description': 'Updated description',
            'start_date': timezone.now().date().strftime('%Y-%m-%d'),
            'end_date': (timezone.now().date() + timezone.timedelta(days=1)).strftime('%Y-%m-%d'),
            'status': 'active'
        })
        self.assertRedirects(response, reverse('report-list'))
        self.report.refresh_from_db()
        self.assertEqual(self.report.name, 'Updated Report', "Report name not updated.")

    def test_report_update_post_invalid(self):
        response = self.client.post(reverse('update-report', kwargs={'pk': self.report.pk}), {
            'name': '',
            'description': ''
        })
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/report-form.html')

class ReportDeleteViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )

    def test_report_delete_post_valid(self):
        response = self.client.post(reverse('delete-report', kwargs={'pk': self.report.pk}))
        self.assertRedirects(response, reverse('report-list'))
        self.assertFalse(ReportModel.objects.exists(), "Report not deleted.")

    def test_report_delete_invalid_id(self):
        response = self.client.post(reverse('delete-report', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404, f"Expected 404, got {response.status_code}.")

class ReportFactorViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )

    def test_report_factor_get(self):
        response = self.client.get(reverse('view-report', kwargs={'pk': self.report.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/report-detail.html')
        self.assertIn('factors', response.context, "Factors not in context.")

    def test_report_factor_invalid_id(self):
        response = self.client.get(reverse('view-report', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404, f"Expected 404, got {response.status_code}.")

class CommentsListViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )
        self.comment = CommentsModel.objects.create(
            title='Test Comment',
            content='Content',
            owner=self.user,
            factor=self.factor
        )

    def test_comments_list_get(self):
        response = self.client.get(reverse('comments-list', kwargs={'factor_id': self.factor.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/comments_list.html')
        self.assertIn('comments', response.context, "Comments not in context.")

    def test_comments_list_invalid_factor(self):
        response = self.client.get(reverse('comments-list', kwargs={'factor_id': 999}))
        self.assertEqual(response.status_code, 404, f"Expected 404, got {response.status_code}.")

class CommentCreateViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )

    def test_comment_create_get(self):
        response = self.client.get(reverse('comment-create', kwargs={'factor_id': self.factor.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/comment_create.html')

    def test_comment_create_post_valid(self):
        response = self.client.post(reverse('comment-create', kwargs={'factor_id': self.factor.pk}), {
            'title': 'New Comment',
            'content': 'Content'
        })
        self.assertRedirects(response, reverse('comments-list', kwargs={'factor_id': self.factor.pk}))
        self.assertTrue(CommentsModel.objects.exists(), "Comment not created.")

    def test_comment_create_post_invalid(self):
        response = self.client.post(reverse('comment-create', kwargs={'factor_id': self.factor.pk}), {
            'title': '',
            'content': ''
        })
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/comment_create.html')
        self.assertFalse(CommentsModel.objects.exists(), "Comment should not be created with invalid data.")

class CommentUpdateViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        self.admin = UserModel.objects.create_user(
            username='admin@u.icesi.edu.co',
            email='admin@u.icesi.edu.co',
            password='password@123',
            is_active=True,
            role=RoleModel.objects.create(name='acadi')
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )
        self.comment = CommentsModel.objects.create(
            title='Test Comment',
            content='Content',
            owner=self.user,
            factor=self.factor
        )

    def test_comment_update_get(self):
        response = self.client.get(reverse('comment-update', kwargs={'comment_id': self.comment.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/comment_create.html')

    def test_comment_update_post_valid(self):
        response = self.client.post(reverse('comment-update', kwargs={'comment_id': self.comment.pk}), {
            'title': 'Updated Comment',
            'content': 'Updated Content'
        })
        self.assertRedirects(response, reverse('comments-list', kwargs={'factor_id': self.factor.pk}))
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.title, 'Updated Comment', "Comment title not updated.")

    def test_comment_update_unauthorized(self):
        self.client.logout()
        login_success = self.client.login(username='admin@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        response = self.client.post(reverse('comment-update', kwargs={'comment_id': self.comment.pk}), {
            'title': 'Updated Comment',
            'content': 'Updated Content'
        })
        self.assertRedirects(response, reverse('comments-list', kwargs={'factor_id': self.factor.pk}))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1, "Expected one error message.")
        self.assertEqual(str(messages_list[0]), 'No tienes permiso para editar este comentario.', f"Expected error message, got '{str(messages_list[0]) if messages_list else 'None'}'.")

class CommentDeleteViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        self.admin = UserModel.objects.create_user(
            username='admin@u.icesi.edu.co',
            email='admin@u.icesi.edu.co',
            password='password@123',
            is_active=True,
            role=RoleModel.objects.create(name='acadi')
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )
        self.comment = CommentsModel.objects.create(
            title='Test Comment',
            content='Content',
            owner=self.user,
            factor=self.factor
        )

    def test_comment_delete_post_valid(self):
        response = self.client.post(reverse('comment-delete', kwargs={'comment_id': self.comment.pk}))
        self.assertRedirects(response, reverse('comments-list', kwargs={'factor_id': self.factor.pk}))
        self.assertFalse(CommentsModel.objects.exists(), "Comment not deleted.")

    def test_comment_delete_unauthorized(self):
        self.client.logout()
        login_success = self.client.login(username='admin@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        response = self.client.post(reverse('comment-delete', kwargs={'comment_id': self.comment.pk}))
        self.assertRedirects(response, reverse('comments-list', kwargs={'factor_id': self.factor.pk}))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1, "Expected one error message.")
        self.assertEqual(str(messages_list[0]), 'No tienes permiso para eliminar este comentario.', f"Expected error message, got '{str(messages_list[0]) if messages_list else 'None'}'.")

class CommentDetailViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )
        self.comment = CommentsModel.objects.create(
            title='Test Comment',
            content='Content',
            owner=self.user,
            factor=self.factor
        )

    def test_comment_detail_get(self):
        response = self.client.get(reverse('comment-detail', kwargs={'comment_id': self.comment.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/comment_detail.html')

    def test_comment_detail_invalid_id(self):
        response = self.client.get(reverse('comment-detail', kwargs={'comment_id': 999}))
        self.assertEqual(response.status_code, 404, f"Expected 404, got {response.status_code}.")

class CommentsReviewListViewTest(TestCase):
    def setUp(self):
        self.admin = UserModel.objects.create_user(
            username='admin@u.icesi.edu.co',
            email='admin@u.icesi.edu.co',
            password='password@123',
            is_active=True,
            role=RoleModel.objects.create(name='acadi')
        )
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='admin@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )
        self.comment = CommentsModel.objects.create(
            title='Test Comment',
            content='Content',
            owner=self.user,
            factor=self.factor,
            status='pending'
        )

    def test_comments_review_list_get_authorized(self):
        response = self.client.get(reverse('comments-review-list', kwargs={'factor_id': self.factor.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/comments_list.html')

    def test_comments_review_list_unauthorized(self):
        self.client.logout()
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        response = self.client.get(reverse('comments-review-list', kwargs={'factor_id': self.factor.pk}))
        self.assertRedirects(response, reverse('comments-list', kwargs={'factor_id': self.factor.pk}))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1, "Expected one error message.")
        self.assertEqual(str(messages_list[0]), "Only users with role 'acadi' or 'program director' can review comments.", f"Expected error message, got '{str(messages_list[0]) if messages_list else 'None'}'.")

class CommentReviewViewTest(TestCase):
    def setUp(self):
        self.admin = UserModel.objects.create_user(
            username='admin@u.icesi.edu.co',
            email='admin@u.icesi.edu.co',
            password='password@123',
            is_active=True,
            role=RoleModel.objects.create(name='acadi')
        )
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='admin@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )
        self.comment = CommentsModel.objects.create(
            title='Test Comment',
            content='Content',
            owner=self.user,
            factor=self.factor,
            status='pending'
        )

    def test_comment_review_get_authorized(self):
        response = self.client.get(reverse('comment-review', kwargs={'comment_id': self.comment.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/comment_review.html')

    def test_comment_review_post_approve(self):
        response = self.client.post(reverse('comment-review', kwargs={'comment_id': self.comment.pk}), {
            'action': 'approve',
            'justification': 'Looks good'
        })
        self.assertRedirects(response, reverse('comments-list', kwargs={'factor_id': self.factor.pk}))
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.status, 'approved', "Comment not approved.")

    def test_comment_review_post_disapprove_no_justification(self):
        response = self.client.post(reverse('comment-review', kwargs={'comment_id': self.comment.pk}), {
            'action': 'disapprove'
        })
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/comment_review.html')
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1, "Expected one error message.")
        self.assertEqual(str(messages_list[0]), 'Justification is required when disapproving a comment.', f"Expected error message, got '{str(messages_list[0]) if messages_list else 'None'}'.")

    def test_comment_review_unauthorized(self):
        self.client.logout()
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        response = self.client.post(reverse('comment-review', kwargs={'comment_id': self.comment.pk}), {
            'action': 'approve'
        })
        self.assertRedirects(response, reverse('dashboard-admin'))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1, "Expected one error message.")
        self.assertEqual(str(messages_list[0]), "Only users with role 'acadi' or 'program director' can review comments.", f"Expected error message, got '{str(messages_list[0]) if messages_list else 'None'}'.")

class JustificationDetailViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )
        self.comment = CommentsModel.objects.create(
            title='Test Comment',
            content='Content',
            owner=self.user,
            factor=self.factor,
            justification='Justified'
        )

    def test_justification_detail_get(self):
        response = self.client.get(reverse('justification-detail', kwargs={'comment_id': self.comment.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/justification_detail.html')

    def test_justification_detail_no_justification(self):
        self.comment.justification = ''
        self.comment.save()
        response = self.client.get(reverse('justification-detail', kwargs={'comment_id': self.comment.pk}))
        self.assertRedirects(response, reverse('comments-list', kwargs={'factor_id': self.factor.pk}))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1, "Expected one error message.")
        self.assertEqual(str(messages_list[0]), 'No justification available for this comment.', f"Expected error message, got '{str(messages_list[0]) if messages_list else 'None'}'.")

class CharacteristicManageViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )
        self.characteristic = CharacteristicModel.objects.create(
            title='Test Characteristic',
            description='Description',
            created_by=self.user
        )
        self.characteristic.factors.add(self.factor)

    def test_characteristic_manage_get(self):
        response = self.client.get(reverse('characteristic-manage', kwargs={'factor_id': self.factor.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/characteristic_manage.html')

    def test_characteristic_manage_invalid_factor(self):
        response = self.client.get(reverse('characteristic-manage', kwargs={'factor_id': 999}))
        self.assertEqual(response.status_code, 404, f"Expected 404, got {response.status_code}.")

class CharacteristicCreateViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )

    def test_characteristic_create_get(self):
        response = self.client.get(reverse('characteristic-create', kwargs={'factor_id': self.factor.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/characteristic_form.html')

    def test_characteristic_create_post_valid(self):
        response = self.client.post(reverse('characteristic-create', kwargs={'factor_id': self.factor.pk}), {
            'title': 'New Characteristic',
            'description': 'Description'
        })
        self.assertRedirects(response, reverse('characteristic-manage', kwargs={'factor_id': self.factor.pk}))
        self.assertTrue(CharacteristicModel.objects.exists(), "Characteristic not created.")

    def test_characteristic_create_post_invalid(self):
        response = self.client.post(reverse('characteristic-create', kwargs={'factor_id': self.factor.pk}), {
            'title': ''
        })
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/characteristic_form.html')
        self.assertFalse(CharacteristicModel.objects.exists(), "Characteristic should not be created with invalid data.")

class CharacteristicUpdateViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )
        self.characteristic = CharacteristicModel.objects.create(
            title='Test Characteristic',
            description='Description',
            created_by=self.user
        )
        self.characteristic.factors.add(self.factor)

    def test_characteristic_update_get(self):
        response = self.client.get(reverse('characteristic-update', kwargs={'factor_id': self.factor.pk, 'characteristic_id': self.characteristic.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/characteristic_form.html')

    def test_characteristic_update_post_valid(self):
        response = self.client.post(reverse('characteristic-update', kwargs={'factor_id': self.factor.pk, 'characteristic_id': self.characteristic.pk}), {
            'title': 'Updated Characteristic',
            'description': 'Updated Description'
        })
        self.assertRedirects(response, reverse('characteristic-manage', kwargs={'factor_id': self.factor.pk}))
        self.characteristic.refresh_from_db()
        self.assertEqual(self.characteristic.title, 'Updated Characteristic', "Characteristic title not updated.")

    def test_characteristic_update_invalid_id(self):
        response = self.client.get(reverse('characteristic-update', kwargs={'factor_id': self.factor.pk, 'characteristic_id': 999}))
        self.assertEqual(response.status_code, 404, f"Expected 404, got {response.status_code}.")

class CharacteristicDeleteViewTest(TestCase):
    def setUp(self):
        self.admin = UserModel.objects.create_user(
            username='admin@u.icesi.edu.co',
            email='admin@u.icesi.edu.co',
            password='password@123',
            is_active=True,
            role=RoleModel.objects.create(name='acadi')
        )
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='admin@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )
        self.characteristic = CharacteristicModel.objects.create(
            title='Test Characteristic',
            description='Description',
            created_by=self.user
        )
        self.characteristic.factors.add(self.factor)

    def test_characteristic_delete_post_authorized(self):
        response = self.client.post(reverse('characteristic-delete', kwargs={'factor_id': self.factor.pk, 'characteristic_id': self.characteristic.pk}))
        self.assertRedirects(response, reverse('characteristic-manage', kwargs={'factor_id': self.factor.pk}))
        self.assertFalse(CharacteristicModel.objects.exists(), "Characteristic not deleted.")

    def test_characteristic_delete_unauthorized(self):
        self.client.logout()
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        response = self.client.post(reverse('characteristic-delete', kwargs={'factor_id': self.factor.pk, 'characteristic_id': self.characteristic.pk}))
        self.assertRedirects(response, reverse('characteristic-manage', kwargs={'factor_id': self.factor.pk}))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1, "Expected one error message.")
        self.assertEqual(str(messages_list[0]), "Only users with role 'acadi' or 'program director' can delete characteristics.", f"Expected error message, got '{str(messages_list[0]) if messages_list else 'None'}'.")

class CharacteristicUploadCSVViewTest(TestCase):
    def setUp(self):
        self.admin = UserModel.objects.create_user(
            username='admin@u.icesi.edu.co',
            email='admin@u.icesi.edu.co',
            password='password@123',
            is_active=True,
            role=RoleModel.objects.create(name='acadi')
        )
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='admin@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )

    def test_characteristic_upload_get_authorized(self):
        response = self.client.get(reverse('characteristic-upload', kwargs={'factor_id': self.factor.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/characteristic_upload.html')

    def test_characteristic_upload_post_valid(self):
        csv_content = "title,description\nTest Characteristic,Description"
        csv_file = SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type='text/csv')
        response = self.client.post(reverse('characteristic-upload', kwargs={'factor_id': self.factor.pk}), {
            'csv_file': csv_file
        })
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/characteristic_preview.html')
        self.assertIn('characteristics_data', response.context, "Characteristics data not in context.")

    def test_characteristic_upload_unauthorized(self):
        self.client.logout()
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        response = self.client.get(reverse('characteristic-upload', kwargs={'factor_id': self.factor.pk}))
        self.assertRedirects(response, reverse('characteristic-manage', kwargs={'factor_id': self.factor.pk}))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1, "Expected one error message.")
        self.assertEqual(str(messages_list[0]), "Only users with role 'acadi' or 'program director' can upload characteristics.", f"Expected error message, got '{str(messages_list[0]) if messages_list else 'None'}'.")

class CharacteristicConfirmViewTest(TestCase):
    def setUp(self):
        self.admin = UserModel.objects.create_user(
            username='admin@u.icesi.edu.co',
            email='admin@u.icesi.edu.co',
            password='password@123',
            is_active=True,
            role=RoleModel.objects.create(name='acadi')
        )
        login_success = self.client.login(username='admin@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.admin
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.admin
        )
        csv_content = "title,description\nTest Characteristic,Description"
        self.client.post(reverse('characteristic-upload', kwargs={'factor_id': self.factor.pk}), {
            'csv_file': SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type='text/csv')
        })

    def test_characteristic_confirm_get(self):
        response = self.client.get(reverse('characteristic-confirm', kwargs={'factor_id': self.factor.pk}))
        self.assertRedirects(response, reverse('characteristic-manage', kwargs={'factor_id': self.factor.pk}))
        self.assertTrue(CharacteristicModel.objects.exists(), "Characteristic not created after confirmation.")

    def test_characteristic_confirm_no_data(self):
        self.client.session['characteristics_data'] = []
        self.client.session.save()
        response = self.client.get(reverse('characteristic-confirm', kwargs={'factor_id': self.factor.pk}))
        self.assertRedirects(response, reverse('characteristic-manage', kwargs={'factor_id': self.factor.pk}))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1, "Expected one error message.")
        self.assertEqual(str(messages_list[0]), 'Characteristics uploaded successfully.', f"Expected error message, got '{str(messages_list[0]) if messages_list else 'None'}'.")

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")

    def test_profile_view_get(self):
        response = self.client.get(reverse('profile-view'))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/profile.html')

    def test_profile_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('profile-view'))
        self.assertRedirects(response, f"{reverse('login-user')}?next={reverse('profile-view')}")
        self.assertEqual(response.status_code, 302, f"Expected 302, got {response.status_code}.")

class EditProfileViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")

    def test_edit_profile_get(self):
        response = self.client.get(reverse('edit-profile-view'))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/edit_profile.html')

    
    #def test_edit_profile_post_invalid(self):
        #response = self.client.post(reverse('edit-profile-view'), {
            #'username': '',
            #'email': ''
        #})
        #self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        #self.assertTemplateUsed(response, 'dashboard/edit_profile.html')

class FactorUpdateViewTest(TestCase):
    def setUp(self):
        self.admin = UserModel.objects.create_user(
            username='admin@u.icesi.edu.co',
            email='admin@u.icesi.edu.co',
            password='password@123',
            is_active=True,
            role=RoleModel.objects.create(name='acadi')
        )
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='admin@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )

    def test_factor_update_get_authorized(self):
        response = self.client.get(reverse('edit-factor', kwargs={'factor_id': self.factor.pk}))
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        self.assertTemplateUsed(response, 'dashboard/edit-factor.html')

    #def test_factor_update_post_valid(self):
        #response = self.client.post(reverse('edit-factor', kwargs={'factor_id': self.factor.pk}), {
            #'name': 'Updated Factor',
            #'content': 'Content'
        #})
        #self.assertRedirects(response, reverse('view-report', kwargs={'pk': self.report.pk}))
        #self.factor.refresh_from_db()
        #self.assertEqual(self.factor.name, 'Updated Factor', "Factor name not updated.")

class QuestionManageViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser@u.icesi.edu.co',
            email='testuser@u.icesi.edu.co',
            password='password@123',
            is_active=True
        )
        login_success = self.client.login(username='testuser@u.icesi.edu.co', password='password@123')
        self.assertTrue(login_success, "Login failed. Check user credentials or authentication backend.")
        self.report = ReportModel.objects.create(
            name='Test Report',
            description='Test description',
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='active',
            created_by=self.user
        )
        self.factor = FactorModel.objects.create(
            name='Factor',
            report=self.report,
            last_edited_by=self.user
        )
        self.question = QuestionModel.objects.create(
            title='Test Question',
            description='Description',
            owner=self.user,
            factor=self.factor
        )

    #def test_question_manage_get(self):
        #response = self.client.get(reverse('question-manage', kwargs={'factor_id': self.factor.pk}))
        #self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}. Redirected to: {response.url if response.status_code == 302 else 'N/A'}")
        #self.assertTemplateUsed(response, 'dashboard/question_manage.html')
        #self.assertIn('questions', response.context, "Questions not in context.")

    def test_question_manage_invalid_factor(self):
        response = self.client.get(reverse('question-manage', kwargs={'factor_id': 999}))
        self.assertEqual(response.status_code, 404, f"Expected 404, got {response.status_code}.")