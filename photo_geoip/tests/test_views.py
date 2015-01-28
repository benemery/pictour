
from django.core.urlresolvers import reverse

class TestViewWebhook():
    def test_get(self, client):
        """Do we respond to a challenge correctly?"""
        challenge = "this-is-a-challenge"
        response = client.get(reverse('webhook'), {'challenge': challenge})

        assert response.status_code == 200
        assert response.content == challenge

    def test_post_invalid_sig(self, client):
        """What happens if we supply an incorrect sig?"""
        response = client.post(reverse('webhook'), X_Dropbox_Signature="FOOBAR")
        assert response.status_code == 403

