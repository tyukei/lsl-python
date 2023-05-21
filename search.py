import pylsl

# ストリームを探す
streams = pylsl.resolve_streams()
for stream in streams:
    print("Stream name:", stream.name())
    print("Stream type:", stream.type())
    print("Stream source ID:", stream.source_id())
    print("Stream channel count:", stream.channel_count())
    print("Stream nominal sampling rate:", stream.nominal_srate())
    print("Stream channel format:", stream.channel_format())