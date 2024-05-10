from apps.core.renderers import SampleJSONRenderer


class ProfileJSONRenderer(SampleJSONRenderer):
    object_label = 'profile'
    pagination_object_label = 'profiles'
    pagination_count_label = 'profilesCount'
