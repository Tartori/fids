import pytsk3
import uuid


class Run:
    def __init__(self,
                 id=None,
                 block_addr=0,
                 length=0,
                 ):
        if id is None:
            self.id = uuid.uuid1().hex
        else:
            self.id = id
        self.block_addr = block_addr
        self.length = length

    def __repr__(self):
        return ('Run('
                f'id={self.id},'
                f'block_addr={self.block_addr},'
                f'length={self.length},'
                ')')


class Attribute:
    def __init__(self,
                 tsk_attribute=None,
                 id=None,
                 flags=0,
                 tsk_id=0,
                 name="",
                 name_size=0,
                 at_type="",
                 runs=[]
                 ):
        if id is None:
            self.id = uuid.uuid1().hex
        else:
            self.id = id
        self.flags = flags
        self.tsk_id = tsk_id
        self.name = name
        self.name_size = name_size
        self.at_type = at_type
        self.runs = runs
        if tsk_attribute is not None:
            self.parse_tsk_attribute(tsk_attribute)

    def parse_tsk_attribute(self, tsk_attribute):
        self.flags = int(tsk_attribute.info.flags)
        self.tsk_id = tsk_attribute.info.id
        self.name = tsk_attribute.info.name
        self.name_size = tsk_attribute.info.name_size
        self.at_type = str(tsk_attribute.info.type)
        self.runs = []
        for run in tsk_attribute:
            self.runs.append(Run(block_addr=run.addr, length=run.len))

    def __repr__(self):
        return ('Attribute('
                f'id={self.id},'
                f'flags="{self.flags}",'
                f'tsk_id={self.tsk_id},'
                f'name={self.name},'
                f'name_size={self.name_size},'
                f'at_type={self.at_type},'
                f'at_type={self.runs},'
                ')')


class HidsFile:
    def __init__(
            self,
            id=None,
            path="",
            meta_addr=0,
            meta_access_time=0,
            meta_access_time_nano=0,
            meta_attr_state=0,
            meta_content_len=0,
            meta_content_ptr=0,
            meta_creation_time=0,
            meta_changed_time=0,
            meta_creation_time_nano=0,
            meta_changed_time_nano=0,
            meta_flags=0,
            meta_gid=0,
            meta_link=0,
            meta_mode=0,
            meta_modification_time=0,
            meta_modification_time_nano=0,
            meta_nlink=0,
            meta_seq=0,
            meta_size=0,
            meta_tag=0,
            meta_type=0,
            meta_uid=0,
            name_flags=0,
            name_meta_addr=0,
            name_meta_seq=0,
            name_name=0,
            name_size=0,
            name_par_addr=0,
            name_par_seq=0,
            name_short_name=0,
            name_short_name_size=0,
            name_tag=0,
            name_type=0,
            attributes=[],
    ):
        if id is None:
            self.id = uuid.uuid1().hex
        else:
            self.id = id
        self.path = path
        self.meta_addr = meta_addr
        self.meta_access_time = meta_access_time
        self.meta_access_time_nano = meta_access_time_nano
        self.meta_attr_state = meta_attr_state
        self.meta_content_len = meta_content_len
        self.meta_content_ptr = meta_content_ptr
        self.meta_creation_time = meta_creation_time
        self.meta_creation_time_nano = meta_creation_time_nano
        self.meta_changed_time = meta_changed_time
        self.meta_changed_time_nano = meta_changed_time_nano
        self.meta_flags = meta_flags
        self.meta_gid = meta_gid
        self.meta_link = meta_link
        self.meta_mode = meta_mode
        self.meta_modification_time = meta_modification_time
        self.meta_modification_time_nano = meta_modification_time_nano
        self.meta_nlink = meta_nlink
        self.meta_seq = meta_seq
        self.meta_size = meta_size
        self.meta_tag = meta_tag
        self.meta_type = meta_type
        self.meta_uid = meta_uid
        self.name_flags = name_flags
        self.name_meta_addr = name_meta_addr
        self.name_meta_seq = name_meta_seq
        self.name_name = name_name
        self.name_size = name_size
        self.name_par_addr = name_par_addr
        self.name_par_seq = name_par_seq
        self.name_short_name = name_short_name
        self.name_short_name_size = name_short_name_size
        self.name_tag = name_tag
        self.name_type = name_type
        self.attributes = attributes

    def set_everything(self,
                       _,
                       id,
                       path,
                       meta_addr,
                       meta_access_time,
                       meta_access_time_nano,
                       meta_attr_state,
                       meta_content_len,
                       meta_content_ptr,
                       meta_creation_time,
                       meta_changed_time,
                       meta_creation_time_nano,
                       meta_changed_time_nano,
                       meta_flags,
                       meta_gid,
                       meta_link,
                       meta_mode,
                       meta_modification_time,
                       meta_modification_time_nano,
                       meta_nlink,
                       meta_seq,
                       meta_size,
                       meta_tag,
                       meta_type,
                       meta_uid,
                       name_flags,
                       name_meta_addr,
                       name_meta_seq,
                       name_name,
                       name_size,
                       name_par_addr,
                       name_par_seq,
                       name_short_name,
                       name_short_name_size,
                       name_tag,
                       name_type):
        self.id = id
        self.path = path
        self.meta_addr = meta_addr
        self.meta_access_time = meta_access_time
        self.meta_access_time_nano = meta_access_time_nano
        self.meta_attr_state = meta_attr_state
        self.meta_content_len = meta_content_len
        self.meta_content_ptr = meta_content_ptr
        self.meta_creation_time = meta_creation_time
        self.meta_creation_time_nano = meta_creation_time_nano
        self.meta_changed_time = meta_changed_time
        self.meta_changed_time_nano = meta_changed_time_nano
        self.meta_flags = meta_flags
        self.meta_gid = meta_gid
        self.meta_link = meta_link
        self.meta_mode = meta_mode
        self.meta_modification_time = meta_modification_time
        self.meta_modification_time_nano = meta_modification_time_nano
        self.meta_nlink = meta_nlink
        self.meta_seq = meta_seq
        self.meta_size = meta_size
        self.meta_tag = meta_tag
        self.meta_type = meta_type
        self.meta_uid = meta_uid
        self.name_flags = name_flags
        self.name_meta_addr = name_meta_addr
        self.name_meta_seq = name_meta_seq
        self.name_name = name_name
        self.name_size = name_size
        self.name_par_addr = name_par_addr
        self.name_par_seq = name_par_seq
        self.name_short_name = name_short_name
        self.name_short_name_size = name_short_name_size
        self.name_tag = name_tag
        self.name_type = name_type

    def set_path(self, path):
        self.path = path

    def parse_tsk_file(self, tsk_file):
        """ return void
            will parse a TSK_FS_FILE in the structure defined here.
            The TSK API Documentation can be found here
            <http://www.sleuthkit.org/sleuthkit/docs/api-docs/4.5/structTSK__FS__FILE.html>
            Be sure to set the path either in the constructor or with the set_path function.
        """
        if tsk_file.info.meta is not None:
            self.meta_addr = tsk_file.info.meta.addr
            self.meta_access_time = tsk_file.info.meta.atime
            self.meta_access_time_nano = tsk_file.info.meta.atime_nano
            self.meta_attr_state = int(tsk_file.info.meta.attr_state)
            self.meta_content_len = tsk_file.info.meta.content_len
            self.meta_content_ptr = tsk_file.info.meta.content_ptr
            self.meta_creation_time = tsk_file.info.meta.crtime
            self.meta_creation_time_nano = tsk_file.info.meta.crtime_nano
            self.meta_changed_time = tsk_file.info.meta.ctime
            self.meta_changed_time_nano = tsk_file.info.meta.ctime_nano
            self.meta_flags = int(tsk_file.info.meta.flags)
            self.meta_gid = tsk_file.info.meta.gid
            self.meta_link = tsk_file.info.meta.link
            self.meta_mode = int(tsk_file.info.meta.mode)
            self.meta_modification_time = tsk_file.info.meta.mtime
            self.meta_modification_time_nano = tsk_file.info.meta.mtime_nano
            self.meta_nlink = tsk_file.info.meta.nlink
            self.meta_seq = tsk_file.info.meta.seq
            self.meta_size = tsk_file.info.meta.size
            self.meta_tag = tsk_file.info.meta.tag
            self.meta_type = str(tsk_file.info.meta.type)
            self.meta_uid = tsk_file.info.meta.uid
        if tsk_file.info.name is not None:
            self.name_flags = int(tsk_file.info.name.flags)
            self.name_meta_addr = tsk_file.info.name.meta_addr
            self.name_meta_seq = tsk_file.info.name.meta_seq
            self.name_name = tsk_file.info.name.name.decode("ascii")
            self.name_size = tsk_file.info.name.name_size
            self.name_par_addr = tsk_file.info.name.par_addr
            self.name_par_seq = tsk_file.info.name.par_seq
            self.name_short_name = tsk_file.info.name.shrt_name
            self.name_short_name_size = tsk_file.info.name.shrt_name_size
            self.name_tag = tsk_file.info.name.tag
            self.name_type = str(tsk_file.info.name.type)
        self.attributes = []
        for tsk_attribute in tsk_file:
            self.attributes.append(Attribute(tsk_attribute=tsk_attribute))

    def __repr__(self):
        return ('HidsFile('
                f'id="{self.id}",'
                f'path="{self.path}",'
                f'meta_addr={self.meta_addr},'
                f'meta_access_time={self.meta_access_time},'
                f'meta_access_time_nano={self.meta_access_time_nano},'
                f'meta_attr_state={self.meta_attr_state},'
                f'meta_content_len={self.meta_content_len},'
                f'meta_content_ptr={self.meta_content_ptr},'
                f'meta_creation_time={self.meta_creation_time},'
                f'meta_creation_time_nano={self.meta_creation_time_nano},'
                f'meta_changed_time={self.meta_changed_time},'
                f'meta_changed_time_nano={self.meta_changed_time_nano},'
                f'meta_flags={self.meta_flags},'
                f'meta_gid={self.meta_gid},'
                f'meta_link={self.meta_link},'
                f'meta_mode={self.meta_mode},'
                f'meta_modification_time={self.meta_modification_time},'
                f'meta_modification_time_nano={self.meta_modification_time_nano},'
                f'meta_nlink={self.meta_nlink},'
                f'meta_seq={self.meta_seq},'
                f'meta_size={self.meta_size},'
                f'meta_tag={self.meta_tag},'
                f'meta_type={self.meta_type},'
                f'meta_uid={self.meta_uid},'
                f'name_flags={self.name_flags},'
                f'name_meta_addr={self.name_meta_addr},'
                f'name_meta_seq={self.name_meta_seq},'
                f'name_name={self.name_name},'
                f'name_size={self.name_size},'
                f'name_par_addr={self.name_par_addr},'
                f'name_par_seq={self.name_par_seq},'
                f'name_short_name={self.name_short_name},'
                f'name_short_name_size={self.name_short_name_size},'
                f'name_tag={self.name_tag},'
                f'name_type={self.name_type},'
                ')')


# pytsk3.TSK_FS_META_MODE_IRUSR.__str__()
# pytsk3.TSK_FS_META_MODE_IRGRP.__str__()
# pytsk3.TSK_FS_META_MODE_IROTH.__str__()
# pytsk3.TSK_FS_META_MODE_IWUSR.__str__()
# pytsk3.TSK_FS_META_MODE_IWGRP.__str__()
# pytsk3.TSK_FS_META_MODE_IWOTH.__str__()
# pytsk3.TSK_FS_META_MODE_IXUSR.__str__()
# pytsk3.TSK_FS_META_MODE_IXGRP.__str__()
# pytsk3.TSK_FS_META_MODE_IXOTH.__str__()
# path
# tsk_file.info.name.type
