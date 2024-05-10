import json

from rest_framework.renderers import JSONRenderer


class SampleJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    
    def render(self, data, media_type=None, renderer_context=None):
        return super().render(data, media_type, renderer_context)
