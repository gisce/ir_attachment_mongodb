# Store OpenERP attachments to MongoDB

To migrate data, rewrite `datas` field of `ir.attachment` model like the 
following **erppeek** snippet:

```python
ira = C.IrAttachment
ira_ids = ira.search()

for ira_id in ira_ids:
    datas = ira.read(ira_id, ['datas'])['datas']
    ira.write([ira_id], {'datas': datas})
```
