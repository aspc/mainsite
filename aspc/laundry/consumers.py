from aspc.laundry.models import LaundryMachine, StatusChange
from aspc.college.models import Building
from channels import Group
from collections import deque
import math
import numpy

CACHE_SIZE = 100
ACTIVE_THRESHOLD = 0.05
MAX_VALUE = 10.0
machines = LaundryMachine.objects.all()
machine_table = dict([ (machine.building.name+'_'+machine.name, deque()) for machine in machines])

def add_entry(d, entry, max_size):
    while len(d) >= max_size:
        d.popleft()
    d.append(entry)

def classify_status(cache):
    variance = numpy.var(list(cache))
    print variance
    if variance > ACTIVE_THRESHOLD:
        return (1, variance)
    return (0, variance)

def process_stream(message):
    message_parts = message.content['text'].split(',')
    dorm_name, machine_name, X, Y, Z = (
        message_parts[0], message_parts[1], float(message_parts[2]), float(message_parts[3]), float(message_parts[4]))
    dorm = Building.objects.get(name=dorm_name)
    try:
        machine = LaundryMachine.objects.get(building=dorm, name = machine_name)
        machine_cache = machine_table[machine.building.name+'_'+machine.name]
        magnitude = math.sqrt((abs(X)**2 + abs(Y)**2 + abs(Z)**2)/3.0)
        add_entry(machine_cache, magnitude, CACHE_SIZE)
        status, variance = classify_status(machine_cache)
        Group('machine-%d' % machine.pk).send({
            'text': str(variance)
        })
        if machine.status != status:
            StatusChange(machine=machine, new_status=status).save()
        machine.status = status
        print machine.status
        machine.save()
    except Exception as e:
        raise
    print machine_table

def machine_details(message, pk):
    Group('machine-%s' % pk).add(message.reply_channel)