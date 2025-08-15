from EventsProject.celery import app

@app.task
def example_task():
    return "Celery is working!"