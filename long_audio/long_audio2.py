import queue
import sounddevice as sd
import soundfile as sf
import threading
import sys
import numpy as np

[sig, fs] = sf.read('VOLVO 48000 #1.wav')
print(len(sig))
print(fs)

blocksize = 2048
buffersize = 20
q = queue.Queue(maxsize=buffersize)
event = threading.Event()

def callback(outdata, frames, time, status):
    assert frames == blocksize
    if status.output_underflow:
        print('Output underflow: increase blocksize?', file=sys.stderr)
        raise sd.CallbackAbort
    assert not status
    try:
        data = q.get_nowait()
    except queue.Empty as e:
        print('Buffer is empty: increase buffersize?', file=sys.stderr)
        raise sd.CallbackAbort from e
    if len(data) < len(outdata):
        outdata[:len(data)] = data
        outdata[len(data):].fill(0)
        raise sd.CallbackStop
    else:
        outdata[:] = data

try:
    with sf.SoundFile('VOLVO 48000 #1.wav') as f:
        for _ in range(buffersize):
            data = f.read(blocksize)
            if not len(data):
                break
            q.put_nowait(data)
        stream = sd.OutputStream(samplerate=fs, blocksize=blocksize,
            callback=callback, finished_callback=event.set)
        with stream:
            timeout = blocksize * buffersize / fs
            while len(data):
                data = f.read(blocksize)
                q.put(data, timeout=timeout)
            event.wait()
except Exception as e:
    print("oops!")

print("testtesttest")


