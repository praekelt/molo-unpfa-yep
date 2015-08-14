from tuneme.forms import LoginForm


def default_forms(request):
    return {
        'login_form': LoginForm()
    }
