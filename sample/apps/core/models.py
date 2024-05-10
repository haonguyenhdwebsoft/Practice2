from django.db import models


class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ['-created_at', '-updated_at']

class APIResponse():
    def __init__(self, status_code, success, data):
        self.status_code = status_code
        self.success = success
        self.data = data
    
    def get_response(self):
        return {
            "status_code": self.status_code,
            "success": self.success,
            "data": self.data
        }