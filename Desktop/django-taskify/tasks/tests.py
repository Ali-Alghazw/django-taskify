from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from .models import Task
from .forms import TaskForm


# ==================== MODEL TESTS ====================
class TaskModelTest(TestCase):
    """Test cases for the Task model"""
    
    def setUp(self):
        """Set up test user and task"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            due_date=date.today() + timedelta(days=7),
            is_completed=False
        )
    
    def test_task_creation(self):
        """Test that a task is created correctly"""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertFalse(self.task.is_completed)
        self.assertEqual(self.task.user, self.user)
    
    def test_task_str_method(self):
        """Test the string representation of task"""
        self.assertEqual(str(self.task), 'Test Task')
    
    def test_task_timestamps(self):
        """Test that created_at and updated_at are set"""
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)
    
    def test_task_default_values(self):
        """Test default values for task fields"""
        task = Task.objects.create(
            user=self.user,
            title='Minimal Task'
        )
        self.assertEqual(task.description, '')
        self.assertIsNone(task.due_date)
        self.assertFalse(task.is_completed)
    
    def test_task_user_relationship(self):
        """Test that task is linked to correct user"""
        self.assertEqual(self.task.user.username, 'testuser')
    
    def test_task_completion_toggle(self):
        """Test toggling task completion status"""
        self.assertFalse(self.task.is_completed)
        self.task.is_completed = True
        self.task.save()
        self.assertTrue(self.task.is_completed)


# ==================== FORM TESTS ====================
class TaskFormTest(TestCase):
    """Test cases for TaskForm"""
    
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'title': 'New Task',
            'description': 'Task description',
            'due_date': date.today() + timedelta(days=1)
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_without_title(self):
        """Test form validation fails without title"""
        form_data = {
            'description': 'Task description',
            'due_date': date.today()
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_form_with_empty_optional_fields(self):
        """Test form is valid with only required fields"""
        form_data = {
            'title': 'Minimal Task',
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_fields(self):
        """Test that form has the correct fields"""
        form = TaskForm()
        self.assertIn('title', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('due_date', form.fields)


# ==================== VIEW TESTS ====================
class TaskViewsTest(TestCase):
    """Test cases for task views"""
    
    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            due_date=date.today() + timedelta(days=7)
        )
    
    def test_task_list_view_requires_login(self):
        """Test that task list requires authentication"""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_task_list_view_with_login(self):
        """Test task list view with authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
    
    def test_task_list_shows_only_user_tasks(self):
        """Test that users only see their own tasks"""
        # Create task for other user
        Task.objects.create(
            user=self.other_user,
            title='Other User Task',
            description='Should not be visible'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task_list'))
        
        # Check that only user's task is in context
        tasks = response.context['page_obj']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, 'Test Task')
    
    def test_add_task_view_get(self):
        """Test GET request to add task view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('add_task'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], TaskForm)
    
    def test_add_task_view_post_valid(self):
        """Test POST request with valid data creates task"""
        self.client.login(username='testuser', password='testpass123')
        task_data = {
            'title': 'New Test Task',
            'description': 'New Description',
            'due_date': date.today() + timedelta(days=5)
        }
        response = self.client.post(reverse('add_task'), data=task_data)
        
        # Check redirect to task list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        
        # Check task was created
        self.assertTrue(Task.objects.filter(title='New Test Task').exists())
    
    def test_add_task_view_post_invalid(self):
        """Test POST request with invalid data doesn't create task"""
        self.client.login(username='testuser', password='testpass123')
        task_data = {
            'description': 'Missing title'
        }
        response = self.client.post(reverse('add_task'), data=task_data)
        
        # Should not redirect
        self.assertEqual(response.status_code, 200)
        # Task should not be created
        self.assertEqual(Task.objects.count(), 1)  # Only setUp task exists
    
    def test_edit_task_view_get(self):
        """Test GET request to edit task view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('edit_task', kwargs={'task_id': self.task.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], TaskForm)
    
    def test_edit_task_view_post_valid(self):
        """Test POST request updates task"""
        self.client.login(username='testuser', password='testpass123')
        updated_data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'due_date': date.today() + timedelta(days=10)
        }
        response = self.client.post(
            reverse('edit_task', kwargs={'task_id': self.task.id}),
            data=updated_data
        )
        
        # Check redirect
        self.assertRedirects(response, reverse('task_list'))
        
        # Check task was updated
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Description')
    
    def test_edit_other_user_task_forbidden(self):
        """Test that user cannot edit another user's task"""
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(
            reverse('edit_task', kwargs={'task_id': self.task.id})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_delete_task_view_get(self):
        """Test GET request to delete task view shows confirmation"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('delete_task', kwargs={'task_id': self.task.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete_task.html')
    
    def test_delete_task_view_post(self):
        """Test POST request deletes task"""
        self.client.login(username='testuser', password='testpass123')
        task_id = self.task.id
        
        response = self.client.post(
            reverse('delete_task', kwargs={'task_id': task_id})
        )
        
        # Check redirect
        self.assertRedirects(response, reverse('task_list'))
        
        # Check task was deleted
        self.assertFalse(Task.objects.filter(id=task_id).exists())
    
    def test_delete_other_user_task_forbidden(self):
        """Test that user cannot delete another user's task"""
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.post(
            reverse('delete_task', kwargs={'task_id': self.task.id})
        )
        self.assertEqual(response.status_code, 404)
        # Task should still exist
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
    
    def test_toggle_task_completion(self):
        """Test toggling task completion status"""
        self.client.login(username='testuser', password='testpass123')
        
        # Initially not completed
        self.assertFalse(self.task.is_completed)
        
        # Toggle to completed
        response = self.client.get(
            reverse('toggle_task_completion', kwargs={'task_id': self.task.id})
        )
        self.assertRedirects(response, reverse('task_list'))
        
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
        
        # Toggle back to incomplete
        response = self.client.get(
            reverse('toggle_task_completion', kwargs={'task_id': self.task.id})
        )
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)


# ==================== AUTHENTICATION TESTS ====================
class AuthenticationTest(TestCase):
    """Test cases for authentication"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_signup_view_get(self):
        """Test GET request to signup view"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
    
    def test_signup_view_post_valid(self):
        """Test POST request with valid signup data"""
        signup_data = {
            'username': 'newuser',
            'password1': 'newpass123!@#',
            'password2': 'newpass123!@#'
        }
        response = self.client.post(reverse('signup'), data=signup_data)
        
        # Check redirect to login
        self.assertRedirects(response, reverse('login'))
        
        # Check user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_redirect_to_task_list(self):
        """Test that successful login redirects to task list"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('task_list'))
    
    def test_logout_redirect(self):
        """Test that logout redirects to login page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))


# ==================== FILTER & SEARCH TESTS ====================
class TaskFilterSearchTest(TestCase):
    """Test cases for filtering and searching tasks"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create multiple tasks
        Task.objects.create(
            user=self.user,
            title='Completed Task',
            description='This is completed',
            is_completed=True
        )
        Task.objects.create(
            user=self.user,
            title='Pending Task',
            description='This is pending',
            is_completed=False
        )
        Task.objects.create(
            user=self.user,
            title='Another Pending',
            description='Also pending',
            is_completed=False
        )
        
        self.client.login(username='testuser', password='testpass123')
    
    def test_filter_completed_tasks(self):
        """Test filtering completed tasks"""
        response = self.client.get(reverse('task_list') + '?filter=completed')
        tasks = response.context['page_obj']
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, 'Completed Task')
    
    def test_filter_pending_tasks(self):
        """Test filtering pending tasks"""
        response = self.client.get(reverse('task_list') + '?filter=pending')
        tasks = response.context['page_obj']
        
        self.assertEqual(len(tasks), 2)
    
    def test_search_tasks_by_title(self):
        """Test searching tasks by title"""
        response = self.client.get(reverse('task_list') + '?q=Completed')
        tasks = response.context['page_obj']
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, 'Completed Task')
    
    def test_search_tasks_by_description(self):
        """Test searching tasks by description"""
        response = self.client.get(reverse('task_list') + '?q=pending')
        tasks = response.context['page_obj']
        
        self.assertGreaterEqual(len(tasks), 2)
    
    def test_sort_by_title(self):
        """Test sorting tasks by title"""
        response = self.client.get(reverse('task_list') + '?sort=title')
        tasks = list(response.context['page_obj'])
        
        self.assertEqual(tasks[0].title, 'Another Pending')
        self.assertEqual(tasks[1].title, 'Completed Task')


# ==================== PAGINATION TESTS ====================
class PaginationTest(TestCase):
    """Test cases for pagination"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create 10 tasks (pagination is set to 5 per page)
        for i in range(10):
            Task.objects.create(
                user=self.user,
                title=f'Task {i+1}',
                description=f'Description {i+1}'
            )
        
        self.client.login(username='testuser', password='testpass123')
    
    def test_first_page_has_5_tasks(self):
        """Test first page shows 5 tasks"""
        response = self.client.get(reverse('task_list'))
        tasks = response.context['page_obj']
        
        self.assertEqual(len(tasks), 5)
    
    def test_second_page_exists(self):
        """Test second page is accessible"""
        response = self.client.get(reverse('task_list') + '?page=2')
        tasks = response.context['page_obj']
        
        self.assertEqual(len(tasks), 5)
        self.assertEqual(response.context['page_obj'].number, 2)
    
    
# ==================== INTEGRATION TESTS ====================
class IntegrationTest(TestCase):
    """End-to-end integration tests"""
    
    def setUp(self):
        self.client = Client()
    
    def test_complete_user_workflow(self):
        """Test complete workflow: signup -> login -> create task -> edit -> delete"""
        
        # 1. Signup
        signup_data = {
            'username': 'integrationuser',
            'password1': 'testpass123!@#',
            'password2': 'testpass123!@#'
        }
        response = self.client.post(reverse('signup'), data=signup_data)
        self.assertEqual(response.status_code, 302)
        
        # 2. Login
        login_success = self.client.login(
            username='integrationuser',
            password='testpass123!@#'
        )
        self.assertTrue(login_success)
        
        # 3. Create task
        task_data = {
            'title': 'Integration Test Task',
            'description': 'Testing full workflow',
            'due_date': date.today() + timedelta(days=7)
        }
        response = self.client.post(reverse('add_task'), data=task_data)
        self.assertEqual(response.status_code, 302)
        
        # 4. Verify task exists
        task = Task.objects.get(title='Integration Test Task')
        self.assertIsNotNone(task)
        
        # 5. Edit task
        updated_data = {
            'title': 'Updated Integration Task',
            'description': 'Updated description',
            'due_date': date.today() + timedelta(days=10)
        }
        response = self.client.post(
            reverse('edit_task', kwargs={'task_id': task.id}),
            data=updated_data
        )
        self.assertEqual(response.status_code, 302)
        
        # 6. Verify update
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Integration Task')
        
        # 7. Toggle completion
        response = self.client.get(
            reverse('toggle_task_completion', kwargs={'task_id': task.id})
        )
        task.refresh_from_db()
        self.assertTrue(task.is_completed)
        
        # 8. Delete task
        response = self.client.post(
            reverse('delete_task', kwargs={'task_id': task.id})
        )
        self.assertEqual(response.status_code, 302)
        
        # 9. Verify deletion
        self.assertFalse(
            Task.objects.filter(title='Updated Integration Task').exists()
        )