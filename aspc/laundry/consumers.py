from aspc.laundry.models import LaundryMachine, StatusChange

machines = LaundryMachine.objects.all()
machine_table = [ (machine.building.name+'_'+machine.name, []) for machine in machines]

def ws_echo(message):
    message.reply_channel.send({
        'text': message.content['text'],
    })