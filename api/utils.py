
def get_token(request):
    return request.headers.get('memex-token', '')