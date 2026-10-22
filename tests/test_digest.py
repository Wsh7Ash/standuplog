from datetime import datetime
from standuplog.digest import parse_log, digest, RECORD_SEP, FIELD_SEP
def make(iso, author, subj):
    return FIELD_SEP.join([iso, author, subj])
def test_parse_and_bucket():
    now = datetime(2026, 10, 27, 18, 0)
    log = RECORD_SEP.join([
        make('2026-10-27T09:00:00', 'ada', 'fix login'),
        make('2026-10-26T15:00:00', 'ada', 'add tests'),
        make('2026-10-20T10:00:00', 'bob', 'old commit'),
    ])
    commits = parse_log(log)
    assert len(commits) == 3
    buckets = digest(commits, now)
    assert 'bob' not in buckets
    assert buckets['ada']['today'] == ['fix login']
    assert buckets['ada']['yesterday'] == ['add tests']
def test_bad_records_skipped():
    assert parse_log('garbage' + RECORD_SEP) == []
