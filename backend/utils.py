from datetime import datetime, timezone

def strfdelta(tdelta, fmt):
    d = {'d': tdelta.days}
    d['h'], rem = divmod(tdelta.seconds, 3600)
    d['m'], d['s'] = divmod(rem, 60)
    return fmt.format(**d)

def report_dataset_updates(latest_timestamp, num_new_datasets):
    date_obj = datetime.fromisoformat(latest_timestamp).replace(tzinfo=timezone.utc)
    time_elapsed = datetime.now(timezone.utc) - date_obj
    pretty_elapsed = strfdelta(time_elapsed, '{d} days, {h} hours, {m} minutes, and {s} seconds')
    print(f'{num_new_datasets} datasets have been created since last update to index ({pretty_elapsed} ago)')

