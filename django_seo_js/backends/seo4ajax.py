from django_seo_js import settings
from .base import SEOBackendBase, RequestsBasedBackend
from urllib.parse import urlparse
 
class SEO4Ajax(SEOBackendBase, RequestsBasedBackend):
    """Implements the backend for seo4ajax.com"""
    BASE_URL = "https://api.seo4ajax.com/"
    RECACHE_URL = "https://api.seo4ajax.com/"
 
    def __init__(self, *args, **kwargs):
        super(SEOBackendBase, self).__init__(*args, **kwargs)
        self.token = self._get_token()
 
    def _get_token(self):
        if settings.SEO4AJAX_TOKEN is None:
            raise ValueError("Missing SEO_JS_SEO4AJAX_TOKEN in settings.")
        return settings.SEO4AJAX_TOKEN
 
    def get_response_for_url(self, url):
        """
        Accepts a fully-qualified url.
        Returns an HttpResponse, passing through all headers and the status code.
        """
 
        if not url or "//" not in url:
            raise ValueError("Missing or invalid url: %s" % url)
        
        parsed_url = urlparse(url)
        render_url = self.BASE_URL + self.token + '/' + parsed_url.path + '?' + parsed_url.query
        r = self.session.get(render_url, allow_redirects=False)
 
        return self.build_django_response_from_requests_response(r)
 
    def update_url(self, url):
        """
        Accepts a fully-qualified url.
        Returns True if successful, False if not successful.
        """
 
        if not url:
            raise ValueError("Missing url")
 
        parsed_url = urlparse(url)
        recache_url = self.BASE_URL + self.token + '/' + parsed_url.path + '?' + parsed_url.query
 
        r = self.session.post(recache_url, data=data)
        return r.status_code < 500