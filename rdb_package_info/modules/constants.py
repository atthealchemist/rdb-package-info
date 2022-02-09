

API_BASE_URL = "https://rdb.altlinux.org/api"
API_BRANCHES_LIST_URL = API_BASE_URL + "/site/all_pkgsets"
API_EXPORT_PACKAGES_URL = API_BASE_URL + "/export/branch_binary_packages/{branch}"

SQL_PACKAGES_TABLE_COLUMNS = (
    'name', 'version', 'branch_name', 'release',
    'arch', 'disttag', 'buildtime', 'source',
    'epoch'
)
SQL_INIT_PACKAGES_TABLE = """
create table if not exists packages
(
    id integer primary key,
    name text,
    version text,
    branch_name text,
    release text,
    arch text,
    disttag text,
    buildtime int,
    source text,
    epoch int
)
"""

SQL_ADD_PACKAGES = """
insert into packages
(
    name,
    version,
    branch_name,
    release,
    arch,
    disttag,
    buildtime,
    source,
    epoch
) values (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
SQL_GET_PACKAGES_FOR_BRANCH = "select {columns} from packages where branch_name='{branch_name}'"
SQL_COUNT_PACKAGES_FOR_BRANCH = "select count(*) from packages where branch_name='{branch_name}'"
