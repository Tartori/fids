import sqlite3
import os.path


class Database:
    def __init__(self, db_config):
        filepath = 'fids_db.db'
        needs_init = False
        if not os.path.exists(filepath):
            needs_init = True
        self.conn = sqlite3.connect(filepath)
        self.cursor = self.conn.cursor()
        if needs_init:
            self.setup()

    def setup(self):
        self.cursor.execute(
            ("CREATE TABLE FIDS_RUN("
                "id varchar(255), "
                "config_hash varchar(255), "
                "start_time int, "
                "finish_time int, "
                " PRIMARY KEY(id)"
                ");"))
        self.cursor.execute(
            ("CREATE TABLE FIDS_FILE("
                "run_id varchar(255),"
                "path text, "
                "meta_addr int,"
                "meta_access_time int,"
                "meta_access_time_nano int,"
                "meta_attr_state int,"
                "meta_content_len int,"
                "meta_content_ptr int,"
                "meta_creation_time int,"
                "meta_changed_time int,"
                "meta_creation_time_nano int,"
                "meta_changed_time_nano int,"
                "meta_flags int,"
                "meta_gid int,"
                "meta_link int,"
                "meta_mode int,"
                "meta_modification_time int,"
                "meta_modification_time_nano int,"
                "meta_nlink int,"
                "meta_seq int,"
                "meta_size int,"
                "meta_tag int,"
                "meta_type varchar(255),"
                "meta_uid int,"
                "name_flags int,"
                "name_meta_addr int,"
                "name_meta_seq int,"
                "name_name int,"
                "name_size int,"
                "name_par_addr int,"
                "name_par_seq int,"
                "name_short_name int,"
                "name_short_name_size int,"
                "name_tag int,"
                "name_type varchar(255),"
                " PRIMARY KEY (run_id, meta_addr)"
                ");")
        )
        self.cursor.execute(
            ("CREATE TABLE FIDS_FILE_ATTRIBUTE("
                "run_id varchar(255),"
                "file_addr int,"
                "flags int,"
                "id int,"
                "name varchar(255),"
                "name_size int,"
                "at_type varchar(255), "
                " PRIMARY KEY (run_id, file_addr, id)"
                ");"))
        self.cursor.execute(
            ("CREATE TABLE FIDS_FILE_ATTRIBUTE_RUN("
                "run_id varchar(255),"
                "file_addr int,"
                "attribute_id int, "
                "block_addr int, "
                "length int, "
                " PRIMARY KEY(run_id, file_addr, attribute_id, block_addr) "
                ");"))

    def start_run(self, run):
        self.cursor.execute(
            "INSERT INTO FIDS_RUN(id, config_hash, start_time) values (?,?,?); ",
            (run.id,
             run.config_hash,
             run.start_time,
             ))

    def finish_run(self, run):
        self.cursor.execute(
            "UPDATE FIDS_RUN SET finish_time = ? WHERE id = ?; ",
            (run.finish_time,
             run.id,
             )
        )

    def safe_file(self, file, run):
        self.cursor.execute(
            ("INSERT INTO FIDS_FILE("
                "run_id,"
                "path,"
                "meta_addr,"
                "meta_access_time,"
                "meta_access_time_nano,"
                "meta_attr_state,"
                "meta_content_len,"
                "meta_content_ptr,"
                "meta_creation_time,"
                "meta_changed_time,"
                "meta_creation_time_nano,"
                "meta_changed_time_nano,"
                "meta_flags,"
                "meta_gid,"
                "meta_link,"
                "meta_mode,"
                "meta_modification_time,"
                "meta_modification_time_nano,"
                "meta_nlink,"
                "meta_seq,"
                "meta_size,"
                "meta_tag,"
                "meta_type,"
                "meta_uid,"
                "name_flags,"
                "name_meta_addr,"
                "name_meta_seq,"
                "name_name,"
                "name_size,"
                "name_par_addr,"
                "name_par_seq,"
                "name_short_name,"
                "name_short_name_size,"
                "name_tag,"
                "name_type"
                ")values("
                "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); "
             ),
            (
                run.id,
                file.path,
                file.meta_addr,
                file.meta_access_time,
                file.meta_access_time_nano,
                file.meta_attr_state,
                file.meta_content_len,
                file.meta_content_ptr,
                file.meta_creation_time,
                file.meta_changed_time,
                file.meta_creation_time_nano,
                file.meta_changed_time_nano,
                file.meta_flags,
                file.meta_gid,
                file.meta_link,
                file.meta_mode,
                file.meta_modification_time,
                file.meta_modification_time_nano,
                file.meta_nlink,
                file.meta_seq,
                file.meta_size,
                file.meta_tag,
                file.meta_type,
                file.meta_uid,
                file.name_flags,
                file.name_meta_addr,
                file.name_meta_seq,
                file.name_name,
                file.name_size,
                file.name_par_addr,
                file.name_par_seq,
                file.name_short_name,
                file.name_short_name_size,
                file.name_tag,
                file.name_type
            )
        )
        for attribute in file.attributes:
            self.save_attribute(attribute, file.meta_addr, run.id)

    def save_attribute(self, attribute, file_addr, run_id):
        self.cursor.execute(
            ("INSERT INTO FIDS_FILE_ATTRIBUTE("
                "run_id,"
                "file_addr,"
                "flags,"
                "id,"
                "name,"
                "name_size,"
                "at_type"
                ")values("
                "?,?,?,?,?,?,?); "
             ),
            (
                run_id,
                file_addr,
                attribute.flags,
                attribute.id,
                attribute.name,
                attribute.name_size,
                attribute.at_type
            )
        )
        for run in attribute.runs:
            self.save_attribute_run(run, attribute.id, file_addr, run_id)

    def save_attribute_run(self, run, attribute_id, file_addr, run_id):
        self.cursor.execute(
            ("INSERT INTO FIDS_FILE_ATTRIBUTE_RUN("
                "run_id,"
                "file_addr,"
                "attribute_id,"
                "block_addr,"
                "length"
                ")values("
                "?,?,?,?,?); "),
            (run_id, file_addr, attribute_id, run.block_addr, run.length))

    def commit(self):
        self.conn.commit()
