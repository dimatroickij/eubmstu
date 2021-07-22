from django.db import models


class Semester(models.Model):
    name = models.CharField('Название', max_length=40, unique=True)
    code = models.CharField('Код', max_length=20, blank=True, unique=True)
    session = models.IntegerField('Код для сессии', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'семестр'
        verbose_name_plural = 'Семестры'
        ordering = ['code']


# Create your models here.
class Departament(models.Model):
    code = models.CharField('Код факультета', max_length=5, unique=True)
    name = models.CharField('Название факультета', max_length=200, unique=True)
    isService = models.BooleanField('Служебный департамент', default=False)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['code']
        verbose_name = 'факультет'
        verbose_name_plural = 'Факультеты'


class Subdepartament(models.Model):
    code = models.CharField('Код кафедры', max_length=11, unique=True)
    name = models.CharField('Название кафедры', max_length=200)
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE, verbose_name='Факультет')
    prove = models.BooleanField(default=False)
    isService = models.BooleanField('Служебная кафедра', default=False)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['code']
        verbose_name = 'кафедра'
        verbose_name_plural = 'Кафедры'
        unique_together = [['code', 'name']]


class Student(models.Model):
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=150)
    patronymic = models.CharField('Отчество', max_length=150, blank=True)
    gradebook = models.CharField('Номер зачётной книжки', max_length=15)
    isStudying = models.BooleanField('Обучается ли сейчас студент', default=True)
    uuid = models.UUIDField('ID студента в системе', primary_key=False, null=True, blank=True)

    def __str__(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.patronymic

    class Meta:
        unique_together = [['first_name', 'last_name', 'patronymic', 'gradebook']]
        ordering = ['last_name', 'first_name', 'patronymic']
        verbose_name = 'студента'
        verbose_name_plural = 'Студенты'


class Group(models.Model):
    LEVEL_EDUCATION = (('bachelor', 'Бакалавриат'),
                       ('magister', 'Магистратура'),
                       ('specialist', 'Специалитет / Аспирантура'),
                       ('archive', 'Архивные записи'))
    name = models.CharField('Название группы', max_length=10)
    code = models.CharField('Код группы для сайта', max_length=50)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name='Семестр')
    subdepartament = models.ForeignKey(Subdepartament, on_delete=models.CASCADE, verbose_name='Кафедра')
    levelEducation = models.CharField('Уровень образования', max_length=10, choices=LEVEL_EDUCATION, null=True)
    isEmpty = models.BooleanField('Данных в ЕУ нет', default=False)
    students = models.ManyToManyField(Student, verbose_name='Студенты')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['subdepartament']
        verbose_name = 'группа'
        verbose_name_plural = 'Группы'
        unique_together = [['name', 'code', 'semester']]


class Subject(models.Model):
    name = models.CharField('Название', max_length=500)
    subdepartament = models.ForeignKey(Subdepartament, on_delete=models.CASCADE, verbose_name='Кафедра')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'Предметы'
        unique_together = [['name', 'subdepartament']]


class GroupSubject(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')

    def __str__(self):
        return self.group.name + ' - ' + self.subject.name

    class Meta:
        verbose_name = 'группаПредмет'
        verbose_name_plural = 'ГруппыПредметы'
        unique_together = [['group', 'subject']]


class Progress(models.Model):
    subject = models.ForeignKey(GroupSubject, on_delete=models.CASCADE, verbose_name='Предмет')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    point = models.IntegerField('Количество баллов за предмет', null=True, blank=True)

    def __str__(self):
        return self.subject.subject.name + ' - ' + self.student.last_name

    class Meta:
        ordering = ['student']
        unique_together = [['subject', 'student']]
        verbose_name = 'Текущая успеваемость'
        verbose_name_plural = 'Текущая успеваемость'


class Session(models.Model):
    RATING = (('Зчт', 'Зачтено'),
              ('Нзч', 'Не зачтено'),
              ('Отл', 'Отлично'),
              ('Хор', 'Хорошо'),
              ('Удов', 'Удовлетворительно'),
              ('НА', 'Не аттестован'),
              ('Я', 'Неявка'),
              ('Напр', 'Направление'),
              ('Неуд', 'Неудовлетворительно'),
              ('Дк', 'Дк'),
              ('Д', 'Дисциплина'),
              ('П', 'Подготовка')) #Подготовка к сдаче государственного экзамена до 31.12.YYYY

    TYPE_RATING = (('Кур', 'Курсовая'),
                   ('Зач', 'Зачёт'),
                   ('Экз', 'Экзамен'),
                   ('Прк', 'Практика'),
                   ('РЭ', 'Рейтинговый экзамен'),
                   ('НРС', 'НРС'),
                   ('НИД', 'Научно-исследовательская деятельность'),
                   ('ЭК', 'ЭК'),
                   ('НКР', 'Научно-квалификационная работа'),
                   ('ГЭ', 'Государственный экзамен')
                   )

    subject = models.ForeignKey(GroupSubject, on_delete=models.CASCADE, verbose_name='Предмет')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    type_rating = models.CharField('Тип оценки', max_length=5, choices=TYPE_RATING)
    rating = models.CharField('Оценка', max_length=4, choices=RATING, null=True, blank=True)

    def __str__(self):
        return self.subject.subject.name + ' - ' + self.student.last_name

    class Meta:
        ordering = ['student']
        unique_together = [['subject', 'student', 'type_rating']]
        verbose_name = 'Результаты сессии'
        verbose_name_plural = 'Результаты сессии'
