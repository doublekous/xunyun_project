from django.db import models


class Ip(models.Model):
    ip = models.CharField(verbose_name='ip', max_length=255)
    ip_status = models.CharField(verbose_name='ip状态', max_length=255, blank=True, null=True)
    # add_people = models.CharField(verbose_name='添加人', max_length=255, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True, blank=True, null=True)
    # last_modified_data = models.DateTimeField(verbose_name='最新修改时间', auto_now_add=True, blank=True, null=True)
    comment = models.CharField(verbose_name='备注', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'xy_ip'






