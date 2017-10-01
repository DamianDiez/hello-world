
import time
import math
import aetros.backend
job = aetros.backend.start_job('marcj/sinus')
sampling_rate = float(job.get_parameter('sampling_rate'))
amplitude = float(job.get_parameter('amplitude'))
sin_channel = job.create_channel('sin', main_graph=True)
cos_channel = job.create_channel('cos', graph_type='bar')
logging_channel = job.create_channel('logging_channel', type=aetros.backend.JobChannel.TEXT)
period = 1.0 / sampling_rate
# The initial timestamp, corresponding to x = 0 in the coordinate axis.
zero_x = time.time()
for iteration in range(1, 50):
    now = time.time()
    x = now - zero_x
    sin_y = amplitude * math.sin(x)
    cos_y = amplitude * math.cos(x)
    # send to AETROS graph
    sin_channel.send(x=x, y=sin_y)
    cos_channel.send(x=x, y=cos_y)
    # Formats a logging entry.
    logging_entry = "sin({x})={sin_y}; cos({x})={cos_y}".format(x=x, sin_y=sin_y, cos_y=cos_y)
    # send custom log channel
    logging_channel.send(x=iteration, y=logging_entry)
    # calculates ETA and set current epoch
    job.progress(iteration, total=50)
    time.sleep(period)
# marks job as done
job.end()
