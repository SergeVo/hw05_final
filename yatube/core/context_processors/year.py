from datetime import datetime


def year(request):
    now = datetime.now()
    return {'year': now.year}
