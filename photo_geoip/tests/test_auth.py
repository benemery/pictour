from django.contrib.auth import login, authenticate

from django_any import any_model
from photo_geoip.models import UserAuthTokens
import pytest

@pytest.mark.django_db
class TestTokenBackend():
    def test_ok(self):
        """Does our token system work?"""
        any_model(UserAuthTokens, dropbox_uid=123, token='foobar')

        user = authenticate(dropbox_uid=123, token='foobar')
        assert user

    def test_bad(self):
        """Do we fail to log people in?"""
        any_model(UserAuthTokens, dropbox_uid=123, token='foobar')
        user = authenticate(dropbox_uid=000, token='INCORRECT')
        assert not user
