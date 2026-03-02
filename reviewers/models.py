"""
Reviewer service models. All managed=False and db_table set to match SUPERGOODI
so this service can use the same database (set DB_PATH to SUPERGOODI's db.sqlite3).
"""
from django.db import models

# ---- Stub models for FK/M2M (same tables as SUPERGOODI) ----

class Panel(models.Model):
    id = models.IntegerField(primary_key=True)
    chair = models.CharField(max_length=60)
    mission = models.CharField(max_length=10)
    cycle = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'review_panel'


class NuSTARPropData(models.Model):
    record_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'proposals_nustarpropdata'


class SubjectArea(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'subjectareas_subjectarea'


class TargetCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'subjectareas_targetcategory'


# ---- Reviewer and related ----

STATUS_CHOICES = (
    ("Y", "Yes"), ("N", "No"), ("U", "Unknown"), ("M", "Maybe"),
    ("V", "Volunteer"), ("S", "Suggestion"), ("A", "Awaiting reply"),
    ("L", "Leader"), ("X", "External"), ("F", "Facilitator"),
)
YESNO = (("Y", "Yes"), ("N", "No"))


class Reviewer(models.Model):
    user_id = models.CharField(max_length=15, blank=True)
    isChair = models.CharField(max_length=1, choices=YESNO, default="N")
    isDepChair = models.CharField(max_length=1, choices=YESNO, default="N")
    source = models.CharField(max_length=50, default="")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="U")
    emailed1 = models.DateField(null=True, blank=True)
    reply1 = models.CharField(max_length=50, null=True, blank=True)
    emailed2 = models.DateField(null=True, blank=True)
    reply2 = models.CharField(max_length=50, null=True, blank=True)
    emailed3 = models.DateField(null=True, blank=True)
    reply3 = models.CharField(max_length=50, null=True, blank=True)
    onNuSTARTeam = models.CharField(max_length=1, choices=YESNO, default="N")
    NuSTARProjectFunding = models.CharField(max_length=1, choices=YESNO, default="N")
    AtForeignInst = models.CharField(max_length=1, choices=YESNO, default="N")
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    inst = models.CharField(max_length=60, blank=True)
    inst2 = models.CharField(max_length=60, blank=True)
    email = models.EmailField(null=True, blank=True)
    Expertise_major = models.CharField(max_length=6, default="xgal")
    expertise_minor = models.ManyToManyField(TargetCategory, blank=True, related_name='+')
    expertise_desc = models.CharField(max_length=200, blank=True)
    conflicts_PI = models.ManyToManyField(NuSTARPropData, related_name='+', blank=True)
    conflicts_CoI = models.ManyToManyField(NuSTARPropData, related_name='+', blank=True)
    conflicts_inst = models.ManyToManyField(NuSTARPropData, related_name='+', blank=True)
    conflicts_collab = models.ManyToManyField(NuSTARPropData, related_name='+', blank=True)
    conflicts_other = models.ManyToManyField(NuSTARPropData, related_name='+', blank=True)
    conflicts_target = models.ManyToManyField(NuSTARPropData, related_name='+', blank=True)
    panel = models.ForeignKey(Panel, on_delete=models.PROTECT)
    mission = models.CharField(max_length=20, default='nustar', blank=True)
    cycle = models.IntegerField(null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    proposals_primary = models.ManyToManyField(NuSTARPropData, related_name='+', blank=True)
    proposals_secondary = models.ManyToManyField(NuSTARPropData, related_name='+', blank=True)
    notes = models.TextField(blank=True)
    url = models.URLField(blank=True)

    class Meta:
        managed = False
        db_table = 'reviewers_reviewer'

    def __str__(self):
        return f"{self.fname} {self.lname} - {self.status}"


class ReviewerSubjectAreas(models.Model):
    reviewer = models.ForeignKey(Reviewer, on_delete=models.PROTECT)
    area = models.ForeignKey(SubjectArea, on_delete=models.PROTECT)
    priority = models.IntegerField(default=1, null=True)
    notes = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = 'reviewers_reviewer_subject_areas'


class ReviewerHistory(models.Model):
    reviewer = models.ForeignKey(Reviewer, on_delete=models.PROTECT)
    mission = models.CharField(max_length=2, default="nu")
    htype = models.CharField(max_length=1, default="U")
    cycle = models.IntegerField(default=1)
    notes = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'reviewers_reviewerhistory'
