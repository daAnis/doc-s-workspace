from django.conf.urls import url
from django.db import models
from django.urls import reverse

from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField

from django.conf import settings

from .defaults import CLINACAL_RECORD_DEFAULTS, DIARIES_DEFAULTS


def record_file_name(instance, filename):
    return "/".join(
        [
            "records",
            str(instance.date_time.year),
            str(instance.date_time.month),
            str(instance.patient.name),
            filename,
        ]
    )


def examination_file_name(instance, filename):
    return "/".join(
        [
            "records",
            str(instance.record.date_time.year),
            str(instance.record.date_time.month),
            str(instance.record.patient.name),
            filename,
        ]
    )


class Notification(models.Model):

    value = models.TextField("Уведомление")
    url = models.URLField("Ссылка")
    date_time = models.DateTimeField("Время", auto_now_add=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Врач", on_delete=models.CASCADE)

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
    phone_number = PhoneNumberField("Номер телефона", blank=True, null=True)
    address = models.CharField("Адрес", max_length=50, blank=True, null=True)
    height = models.PositiveSmallIntegerField("Рост", blank=True, null=True)
    weight = models.PositiveSmallIntegerField("Вес", blank=True, null=True)

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        latestRecord = ClinicalRecord.objects.filter(patient=self.pk).latest('date_time')
        return reverse("record", kwargs={"ward": latestRecord.ward, "record_id": latestRecord.pk})


class ClinicalRecord(models.Model):

    patient = models.ForeignKey(
        Patient, verbose_name="Пациент", on_delete=models.DO_NOTHING
    )
    ward = models.PositiveSmallIntegerField("Номер палаты")
    diagnosis = models.TextField("Краткий диагноз")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Врач", on_delete=models.DO_NOTHING)
    date_time = models.DateTimeField("Время поступления", auto_now_add=True)
    complaint = RichTextField("Жалобы при поступлении", blank=True, null=True)
    anamnesis = RichTextField("Anamnesis morbi", blank=True, null=True)
    habitual_intoxication = RichTextField(
        "Привычные интоксикации",
        blank=True,
        null=True,
        default=CLINACAL_RECORD_DEFAULTS["habitual_intoxication"],
    )
    occupational_hazards = RichTextField(
        "Профессиональные вредности",
        blank=True,
        null=True,
        default=CLINACAL_RECORD_DEFAULTS["occupational_hazards"],
    )
    epidanamnesis = RichTextField(
        "Эпиданамнез",
        blank=True,
        null=True,
        default=CLINACAL_RECORD_DEFAULTS["epidanamnesis"],
    )
    allergic_history = RichTextField(
        "Аллергический анамнез",
        blank=True,
        null=True,
        default=CLINACAL_RECORD_DEFAULTS["allergic_history"],
    )
    blood_transfusion = RichTextField(
        "Гемотрансфузии",
        blank=True,
        null=True,
        default=CLINACAL_RECORD_DEFAULTS["blood_transfusion"],
    )
    expert_history = RichTextField(
        "Экспертный анамнез",
        blank=True,
        null=True,
        default=CLINACAL_RECORD_DEFAULTS["expert_history"],
    )
    past_illnesses = RichTextField(
        "Перенесенные заболевания",
        blank=True,
        null=True,
        default=CLINACAL_RECORD_DEFAULTS["past_illnesses"],
    )
    status_p_c = RichTextField(
        "Status praesens communis",
        blank=True,
        null=True,
        default=CLINACAL_RECORD_DEFAULTS["status_p_c"],
    )
    respiratory_system = RichTextField(
        "Органы дыхания",
        blank=True,
        null=True,
        default=CLINACAL_RECORD_DEFAULTS["respiratory_system"],
    )
    circulatory_organs = RichTextField(
        "Органы кровообращения",
        blank=True,
        null=True,
        default=CLINACAL_RECORD_DEFAULTS["circulatory_organs"],
    )
    digestive_organs = RichTextField(
        "Органы пищеварения",
        blank=True,
        null=True,
        default=CLINACAL_RECORD_DEFAULTS["digestive_organs"],
    )
    urinary_organs = RichTextField(
        "Органы мочевыделения",
        blank=True,
        null=True,
        default=CLINACAL_RECORD_DEFAULTS["urinary_organs"],
    )
    status_localis = RichTextField(
        "Status localis",
        blank=True,
        null=True,
        default=CLINACAL_RECORD_DEFAULTS["status_localis"],
    )
    preliminary_diagnosis = RichTextField(
        "Предварительный диагноз", blank=True, null=True
    )
    primary_diagnosis = RichTextField("Основной диагноз", blank=True, null=True)
    data_from_additional_research_methods = RichTextField(
        "Данные дополнительных методов исследования", blank=True, null=True
    )
    recommendation = RichTextField("Рекомендации", blank=True, null=True)
    discharge = models.FileField("Выписка", upload_to=record_file_name, blank=True, null=True)
    record = models.FileField("История", upload_to=record_file_name, blank=True, null=True)

    class Meta:
        verbose_name = "История болезни"
        verbose_name_plural = "Истории болезней"

    def __str__(self):
        return self.patient.name

    def get_absolute_url(self):
        return reverse("record", kwargs={"ward": self.ward, "record_id": self.pk})

    def save(self, *args, **kwargs):
        if not ClinicalRecord.objects.filter(pk=self.pk).exists():
            super().save(*args, **kwargs)
            context = { 'ward': self.ward, 'record_id': self.pk }
            n = Notification(
                value=f'Поступил новый пациент, { self.patient.name }.',
                url=reverse('record', kwargs=context),
                doctor=self.doctor
            )
            n.save()
        super().save(*args, **kwargs)


class Diary(models.Model):

    date_time = models.DateTimeField("Время", default=timezone.now)
    complaint = RichTextField("Жалобы на", blank=True, null=True)
    status_p_c = RichTextField(
        "Объективный статус",
        blank=True,
        null=True,
        default=DIARIES_DEFAULTS["status_p_c"],
    )
    status_localis = RichTextField(
        "Неврологический статус",
        blank=True,
        null=True,
        default=DIARIES_DEFAULTS["status_localis"],
    )
    record = models.ForeignKey(
        ClinicalRecord, verbose_name="История болезни", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Дневник"
        verbose_name_plural = "Дневники"

    def __str__(self):
        return self.date_time.strftime("%Y-%m-%d")



class Temperature(models.Model):

    date_time = models.DateTimeField("Время замера", auto_now_add=True)
    value = models.DecimalField("Значение", max_digits=3, decimal_places=1)
    record = models.ForeignKey(
        ClinicalRecord, verbose_name="История болезни", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Температура"
        verbose_name_plural = "Температуры"

    def __str__(self):
        return self.date_time.strftime("%Y-%m-%d")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.value > 38.0:
            context = { 'ward': self.record.ward, 'record_id': self.record.pk }
            n = Notification(
                value=f'Высокая температура у пациента: { str(self.value) }! Пациент - { self.record.patient.name }.',
                url=reverse('observation', kwargs=context),
                doctor=self.record.doctor
            )
            n.save()


class Pressure(models.Model):

    date_time = models.DateTimeField("Время замера", auto_now_add=True)
    diastole = models.PositiveSmallIntegerField("Дистола")
    systole = models.PositiveSmallIntegerField("Систола")
    puls = models.PositiveSmallIntegerField("Пульс")
    record = models.ForeignKey(
        ClinicalRecord, verbose_name="История болезни", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Давление и пульс"
        verbose_name_plural = "Значения давления и пульса"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.diastole > 139 and self.systole > 59:
            context = { 'ward': self.record.ward, 'record_id': self.record.pk }
            n = Notification(
                value=f'Высокое А/Д у пациента: { str(self.diastole) }/{ str(self.systole) }! Пациент - { self.record.patient.name }.',
                url=reverse('observation', kwargs=context),
                doctor=self.record.doctor
            )
            n.save()
        elif self.diastole < 101 and self.systole < 61:
            context = { 'ward': self.record.ward, 'record_id': self.record.pk }
            n = Notification(
                value=f'Низкое А/Д у пациента: { str(self.diastole) }/{ str(self.systole) }! Пациент - { self.record.patient.name }.',
                url=reverse('observation', kwargs=context),
                doctor=self.record.doctor
            )
            n.save()


class Examination(models.Model):

    name = models.CharField("Вид обследования", max_length=50)
    date_1 = models.DateTimeField("Дата назначения", auto_now_add=True)
    date_2 = models.DateTimeField("Дата исполнения", auto_now=True, blank=True)
    record = models.ForeignKey(
        ClinicalRecord, verbose_name="История болезни", on_delete=models.CASCADE
    )
    result = models.FileField("Результат", upload_to=examination_file_name, blank=True)

    class Meta:
        verbose_name = "Обследование"
        verbose_name_plural = "Обследования"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.date_2 > self.date_1:
            context = { 'ward': self.record.ward, 'record_id': self.record.pk }
            n = Notification(
                value=f'Готов результат обследования: { self.name }.  Пациент - { self.record.patient.name }.',
                url=reverse('examination', kwargs=context),
                doctor=self.record.doctor
            )
            n.save()
            


class Prescription(models.Model):

    name = models.CharField("Назначение", max_length=50)
    date_1 = models.DateField("Дата начала приема")
    date_2 = models.DateField("Дата окончания приема")
    record = models.ForeignKey(
        ClinicalRecord, verbose_name="История болезни", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Назначение"
        verbose_name_plural = "Назначения"

    def __str__(self):
        return self.name
