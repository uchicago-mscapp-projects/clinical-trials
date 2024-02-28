https://api.fda.gov/drug/drugsfda.json?search=submissions.submission_status_date:[20030101+TO+20240219]&skip=0&limit=1000

requests.get('https://api.fda.gov/drug/drugsfda.json?search=submissions.submission_status_date:[20030101+TO+20240219]&skip=0&limit=1000')


payload = {
    'search': 'submissions.submission_status_date:[20030101+TO+20240219]',
    'skip': 0,
    'limit': 1000
}