## 说明

关于secret的加密验证（数据格式+加密算法）
```python
format_data = json.dumps(json.loads(primary_data,object_pairs_hook=OrderedDict),separators=(',',':'),ensure_ascii=False)
'sha1=' + hmac.new('YourSecret', msg=format_data, digestmod=sha1).hexdigest()
```
