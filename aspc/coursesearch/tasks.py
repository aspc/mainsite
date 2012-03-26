from celery.task import task

@task
def update_catalog():
    logger = update_catalog.get_logger()
    logger.info("Starting full catalog update")
    logger.info("Full catalog update finished")

@task
def update_enrollments():
    logger = update_registration.get_logger()
    logger.info("Starting update of course enrollments")
    logger.info("Course enrollments update finished")
