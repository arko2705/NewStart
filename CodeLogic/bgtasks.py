from celery import current_app
def deletingBG():
    current_app.control.purge()       ##deletes everything in queue,afaik.
    return

