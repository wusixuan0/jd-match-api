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
    user_email = models.ForeignKey(UserEmail, on_delete=models.CASCADE)
    applied_job_ids = models.CharField(max_length=255)
    user_ranking = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)