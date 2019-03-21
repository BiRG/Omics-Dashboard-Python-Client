# Omics Dashboard Python Client
A python client for accessing an [Omics Dashboard](https://github.com/BiRG/Omics-Dashboard) service.

## Installation
### Requirements
Python 3.4+ or 2.7

You can install from this repository using `pip`:
```bash
pip install git+git://github.com/BiRG/Omics-Dashboard-Python-Client.git
```

## Usage Examples
All records can be edited in a similar fashion, but the `Job` record is not editable here or on the server.

### Log in to service
`credentials.json` (stored with 400 permissions or equivalent):

```json 
{
  "email": "person@company.com",
  "password": "AVeryVeryVeryGoodPassword"
}
```
You can also pass the credentials dictionary directly.

```python
from omics_dashboard_client import Session

session = Session('https://example.com/omics', 'credentials.json')
```
### Access collections
```python
from omics_dashboard_client import Session, Collection
session = Session('https://example.com/omics', 'credentials.json')

# access collection #12
collection = session.get(Collection, 12)

# query all collections to get collections fitting a query
# the data received from the query is small because the files are never downloaded
# search with url query parameters may be added in a later API release
collections = [collection for collection in session.get_all(Collection)
               if collection.name == 'Test Collection']

# access a collection attribute:
collection_name = collection.name

# access a collection file attribute:
proc_log = collection.get_attr('processing_log')
```
### Modify collections
Because files may be large, they are not downloaded by default.
```python
# modify a collection dataset
from omics_dashboard_client import Session, Collection
session = Session('https://example.com/omics', 'credentials.json')

collection = session.get(Collection, 23)

session.download_file(collection)
Y = collection.get_dataset('Y')
Y = 0.01 * Y
collection.set_dataset('Y_modified', Y)
session.update(collection)

# create a new collection from modified collection
Y = collection.get_dataset('Y')
Y = 0.01 * Y
collection.set_dataset('Y', Y)
collection.set_attr('processing_log', 'Scaled spectra by 0.01')
collection.analysis_ids = [1, 2]
session.create(collection)  # the 'id' field will change to that of the new collection

# you can delete the record
session.delete(collection)

```
### Start a workflow on the job server
```python
from omics_dashboard_client import Session, Workflow, Collection
session = Session('https://example.com/omics', 'credentials.json')
collection = session.get(Collection, 12)
workflow = session.get(Workflow, 7)  # Let's say the workflow does PCA on 'Y'
job_params = {
  'inputFilenames': [collection.filename]
}
job = session.submit_job(workflow, job_params)

# you can cancel the job too
msg = session.cancel_job(job)
```
