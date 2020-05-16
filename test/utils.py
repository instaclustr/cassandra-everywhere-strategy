import errno
import os
from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError

_project_dir = Path(__file__).parents[1]


def _project_version() -> str:
    root_pom = ElementTree.parse(_project_dir / 'pom.xml').getroot()
    version_tag = root_pom.find('{http://maven.apache.org/POM/4.0.0}version')
    if version_tag is None:
        raise ParseError('not a pom.xml file (<version> tag not found)')

    return version_tag.text


def default_jar_path():
    return _project_dir / f'target/instaclustr-everywhere-strategy-{_project_version()}.jar'


def add_strategy_jar(cluster_dir: Path, jar_path: Path):
    if not jar_path.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f'{jar_path} not found.')

    with Path(cluster_dir / 'cassandra.in.sh').open('w') as f:
        # f.write('JVM_OPTS="$JVM_OPTS -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005"\n')
        f.write(f'CLASSPATH="$CLASSPATH:{jar_path}"\n')
