# yadagelimitsharedfs

```
export YADAGE_IGNORE_PREPUBLISHING=true
export PYTHONPATH=$PWD/plugins:$PYTHONPATH
yadage-run -b foregroundasync py:customstate:setup:global_share workflow_prot.yml --metadir here -k packconfig_spec='{"process": {"interpolated-script-cmd": "custom"}, "publisher": {"frompar-pub": "custom"}, "environment": {"docker-encapsulated": "custom"}}' --plugins=packplugs --visualize
```
