# from django.db import models
# from django.contrib.auth.models import User

# class Category(models.Model):
#     name = models.CharField(max_length=100, verbose_name="Название")
#     slug = models.SlugField(unique=True, verbose_name="Слаг")
    
#     def __str__(self):
#         return self.name
    
#     class Meta:
#         verbose_name = "Категория"
#         verbose_name_plural = "Категории"

# class Problem(models.Model):
#     DIFFICULTY_CHOICES = [
#         ('easy', 'Лёгкая'),
#         ('medium', 'Средняя'),
#         ('hard', 'Сложная'),
#     ]
    
#     title = models.CharField(max_length=200, verbose_name="Название")
#     description = models.TextField(verbose_name="Условие")
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='problems')
#     difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
#     time_limit = models.FloatField(default=1.0, help_text="Ограничение по времени (сек)")
#     memory_limit = models.IntegerField(default=256, help_text="Ограничение по памяти (MB)")
    
#     def __str__(self):
#         return self.title
    
#     class Meta:
#         verbose_name = "Задача"
#         verbose_name_plural = "Задачи"

# class TestCase(models.Model):
#     problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
#     input_data = models.TextField(verbose_name="Входные данные")
#     output_data = models.TextField(verbose_name="Ожидаемый вывод")
#     is_sample = models.BooleanField(default=False, verbose_name="Пример из условия")
    
#     def __str__(self):
#         return f"Тест #{self.id} для {self.problem.title}"

# class Hint(models.Model):
#     problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='hints')
#     content = models.TextField(verbose_name="Подсказка")
#     order = models.IntegerField(default=0, verbose_name="Порядок")
    
#     def __str__(self):
#         return f"Подсказка {self.order} для {self.problem.title}"

# class UserProblemStatus(models.Model):
#     STATUS_CHOICES = [
#         ('solved', 'Решено'),
#         ('want', 'Хочу решить'),
#         ('not_started', 'Не начато'),
#     ]
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_statuses')
#     problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='user_statuses')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
#     solved_at = models.DateTimeField(null=True, blank=True)
    
#     class Meta:
#         unique_together = ['user', 'problem']
    
#     def __str__(self):
#         return f"{self.user.username} - {self.problem.title}: {self.status}"

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Role(models.Model):
    """Роль пользователя (OneToOne с User)"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название роли")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

class Problem(models.Model):
    """Задача из архива"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Лёгкая'),
        ('medium', 'Средняя'),
        ('hard', 'Сложная'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название")
    statement = models.TextField(verbose_name="Условие задачи")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    time_limit = models.FloatField(default=1.0, verbose_name="Ограничение по времени (сек)")
    memory_limit = models.IntegerField(default=256, verbose_name="Ограничение по памяти (MB)")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

class Tag(models.Model):
    """Тег для задач (ManyToMany с Problem)"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название тега")
    problems = models.ManyToManyField(Problem, related_name='tags', blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

class TestCase(models.Model):
    """Тест-кейсы для задачи (ForeignKey к Problem)"""
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField(verbose_name="Входные данные")
    expected_output = models.TextField(verbose_name="Ожидаемый вывод")
    is_sample = models.BooleanField(default=False, verbose_name="Пример из условия")
    
    def __str__(self):
        return f"Тест #{self.id} для {self.problem.title}"
    
    class Meta:
        verbose_name = "Тест-кейс"
        verbose_name_plural = "Тест-кейсы"

class Contest(models.Model):
    """Соревнование"""
    name = models.CharField(max_length=200, verbose_name="Название")
    start_time = models.DateTimeField(verbose_name="Время начала")
    duration = models.IntegerField(help_text="Длительность в минутах", verbose_name="Длительность")
    difficulty = models.CharField(max_length=20, default='medium', verbose_name="Сложность")
    problems = models.ManyToManyField(Problem, related_name='contests', blank=True, verbose_name="Задачи")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Соревнование"
        verbose_name_plural = "Соревнования"

class UserProblemStatus(models.Model):
    """Статус решения задачи пользователем (ForeignKey к User и Problem)"""
    STATUS_CHOICES = [
        ('not_started', 'Не начато'),
        ('in_progress', 'В процессе'),
        ('solved', 'Решено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_statuses')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='user_statuses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    attempts = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    solved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'problem']
        verbose_name = "Статус решения задачи"
        verbose_name_plural = "Статусы решения задач"
    
    def __str__(self):
        return f"{self.user.username} - {self.problem.title}: {self.status}"

# Расширение User через OneToOne (добавляем роль)
class UserProfile(models.Model):
    """Профиль пользователя (OneToOne с User)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')
    contests_attended = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Профиль {self.user.username}"
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"