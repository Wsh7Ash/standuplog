from datetime import datetime, timedelta

RECORD_SEP = '\x1e'
FIELD_SEP = '\x1f'

def parse_log(git_log_output):
    commits = []
    for record in git_log_output.split(RECORD_SEP):
        record = record.strip()
        if not record:
            continue
        parts = record.split(FIELD_SEP)
        if len(parts) != 3:
            continue
        iso, author, subject = parts
        try:
            ts = datetime.fromisoformat(iso)
        except ValueError:
            continue
        commits.append({'ts': ts, 'author': author, 'subject': subject})
    return commits

def digest(commits, now=None):
    now = now or datetime.now()
    yesterday = now - timedelta(days=1)
    buckets = {}
    for c in commits:
        day = 'today' if c['ts'].date() == now.date() else ('yesterday' if c['ts'].date() == yesterday.date() else 'older')
        if day == 'older':
            continue
        buckets.setdefault(c['author'], {'today': [], 'yesterday': []})[day].append(c['subject'])
    return buckets
