from django.db import models

class TemporaryTransaction(models.Model):
    file_url =  models.URLField()
    file_summary = models.TextField()
    ranked_ids = models.CharField(max_length=255)

class UserEmail(models.Model):
    email = models.EmailField(unique=True)
    frequency = models.CharField(max_length=20)

class Resume(models.Model):
    user_email = models.ForeignKey(UserEmail, on_delete=models.CASCADE)
    resume_url =  models.URLField()
    resume_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class JobRecommendation(models.Model):
    user_email = models.ForeignKey(UserEmail, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    ranked_job_ids = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class UserFeedback(models.Model):
    user_email = models.ForeignKey(UserEmail, on_delete=models.SET_NULL, null=True, blank=True)
    temporary_transaction = models.ForeignKey(TemporaryTransaction, on_delete=models.SET_NULL, null=True, blank=True)
    applied_job_ids = models.CharField(max_length=255)
    user_ranking = models.CharField(max_length=255, null=True, blank=True)
    feedback_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(temporary_transaction__isnull=False) |
                    models.Q(user_email__isnull=False)
                ),
                name='feedback_has_temporary_transaction_or_user'
            )
        ]