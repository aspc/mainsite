from aspc.models import Room
from django.db import transaction

@transaction.commit_manually
def suites(data):
    """
    Import suites. Expects data in a (buildingname, (roomnumber, roomnumber, roomnumber)) format.
    """
    try:
        rooms = Room.objects.update(suite=None)
        
        for suite in data:
            new_suite_rooms = Room.objects.filter(building__shortname=suite[0], number_in=suite[1])
            Room.objects.create_suite(new_suite_rooms)
    except:
        transaction.rollback()
    else:
        transaction.commit()


    