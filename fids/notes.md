# notes

file.info.meta.size // size in bytes

file.info.meta.crtime //creation time

file.info.meta.mtime //modification time

file.info.meta.atime //access time

file.info.meta.ctime //changed time (rights etcx.)

``` bash
>>> pytsk3.TSK_FS_META_MODE_IRUSR.__str__()
'256'
>>> pytsk3.TSK_FS_META_MODE_IRGRP.__str__()
'32'
>>> pytsk3.TSK_FS_META_MODE_IROTH.__str__()
'4'
>>> pytsk3.TSK_FS_META_MODE_IWUSR.__str__()
'128'
>>> pytsk3.TSK_FS_META_MODE_IWGRP.__str__()
'16'
>>> pytsk3.TSK_FS_META_MODE_IWOTH.__str__()
'2'
>>> pytsk3.TSK_FS_META_MODE_IXUSR.__str__()
'64'
>>> pytsk3.TSK_FS_META_MODE_IXGRP.__str__()
'8'
>>> pytsk3.TSK_FS_META_MODE_IXOTH.__str__()
'1'

```