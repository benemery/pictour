from photo_geoip.models import UserAuthTokens

class DropboxAccessTokenBackend(object):
    def authenticate(self, dropbox_uid, token):
        """Have we seen this token before?"""
        query_set = UserAuthTokens.objects.filter(dropbox_uid=dropbox_uid,
                                                    token=token)
        if query_set.exists():
            uat = query_set.select_related('user').get()
            return uat.user

