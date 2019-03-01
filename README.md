# Omics Dashboard Python Client
A python client for accessing an [Omics Dashboard](https://github.com/BiRG/Omics-Dashboard) service.

## Usage Examples
### Log in to service
```python
from omics_dashboard_client import Session, Collection, Analysis
import numpy as np

session = Session('https://example.com/omics', 'test@test.net', 'testpass')
```
### Access collections
```python
# access collection #12
collection = session.get_collection(12)

# query all collections to get collections fitting a query
# the data received from the query is small because the files are never downloaded completely
collections = [collection for collection in session.get_all_collections()
               if collection.attrs['name'] == 'Test Collection']

# access a collection attribute:
collection_name = collection.attrs['description']

# access a collection file attribute:
collection_name = collection.file_attrs['processing_log']
```
### Modify collections
```python
# modify a collection dataset
Y = collection.get_dataset('Y')
Y = 0.01 * Y
collection.set_dataset('Y', Y)
collection.commit()

# create a new collection from modified collection
Y = collection.get_dataset('Y')
Y = 0.01 * Y
collection.set_dataset('Y', Y)
collection.file_attrs['processing_log'] = 'Scaled spectra by 0.01'
collection = session.post_collection(collection, analysis_ids=[1, 2])
```

