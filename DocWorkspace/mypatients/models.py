from django.db import models
from django.urls import reverse

def record_file_name(instance, filename):
    return '/'.join(['records', str(instance.date_time.year), str(instance.date_time.month), str(instance.patient.name), filename])

def examination_file_name(instance, filename):
    return '/'.join(['records', str(instance.record.date_time.year), str(instance.record.date_time.month), str(instance.record.patient.name), filename])

class Doctor(models.Model):

    name = models.CharField("ФИО", max_length=50)
    login = models.CharField("Логин", max_length=20)
    password = models.CharField("Пароль", max_length=20)

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    def __str__(self):
        return self.name

class Notification(models.Model):

    value = models.TextField("Уведомление")
    url = models.URLField("Ссылка")
    date_time = models.DateTimeField("Время", auto_now_add=True)
    doctor = models.ForeignKey(Doctor, verbose_name="Врач", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return self.value

    def get_absolute_url(self):
        return self.url

class Patient(models.Model):

    name = models.CharField("ФИО", max_length=50)
    birth_date = models.DateField("Дата рождения")

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self):
        return self.name

class ClinicalRecord(models.Model):

    patient = models.ForeignKey(Patient, verbose_name="Пациент", on_delete=models.DO_NOTHING)
    ward = models.PositiveSmallIntegerField("Номер палаты")
    diagnosis = models.TextField("Краткий диагноз")
    doctor = models.ForeignKey(Doctor, verbose_name="Врач", on_delete=models.DO_NOTHING)
    date_time = models.DateTimeField("Время поступления", auto_now_add=True)
    record = models.FileField("Файл", upload_to=record_file_name)

    class Meta:
        verbose_name = "История болезни"
        verbose_name_plural = "Истории болезней"

    def __str__(self):
        return self.patient.name

    def get_absolute_url(self):
        return reverse("ClinicalRecord_detail", kwargs={"pk": self.pk})

class Temperature(models.Model):

    date_time = models.DateTimeField("Время замера", auto_now_add=True)
    value = models.DecimalField("Значение", max_digits=3, decimal_places=1)
    record = models.ForeignKey(ClinicalRecord, verbose_name="История болезни", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Температура"
        verbose_name_plural = "Температуры"

class Pressure(models.Model):

    date_time = models.DateTimeField("Время замера", auto_now_add=True)
    puls = models.PositiveSmallIntegerField("Пульс")
    pressure = models.CharField("Двление", max_length=7)
    record = models.ForeignKey(ClinicalRecord, verbose_name="История болезни", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Давление и пульс"
        verbose_name_plural = "Значения давления и пульса"

class Examination(models.Model):

    name = models.CharField("Вид обследования", max_length=50)
    date_1 = models.DateTimeField("Дата назначения", auto_now_add=True)
    date_2 = models.DateTimeField("Дата исполнения", auto_now=True, blank=True)
    record = models.ForeignKey(ClinicalRecord, verbose_name="История болезни", on_delete=models.CASCADE)
    result = models.FileField("Результат", upload_to=examination_file_name, blank=True)

    class Meta:
        verbose_name = "Обследование"
        verbose_name_plural = "Обследования"

    def __str__(self):
        return self.name

class Prescription(models.Model):

    name = models.CharField("Назначение", max_length=50)
    date_1 = models.DateField("Дата начала приема")
    date_2 = models.DateField("Дата окончания приема")
    record = models.ForeignKey(ClinicalRecord, verbose_name="История болезни", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Назначение"
        verbose_name_plural = "Назначения"

    def __str__(self):
        return self.name