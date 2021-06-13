from urllib.parse import urlencode
from django import template


register = template.Library()

@register.simple_tag
def get_login_qq_url():
    params = {
        'response_type':'code',
        'client_id':'101958390',
        'redirect_uri':'https://shnuer.club/user/login_by_qq',
        'state':'shnuer',
    }
    return 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(params)