from background_task.models import Task
def deletingBG():
    Task.objects.all().delete()
    return