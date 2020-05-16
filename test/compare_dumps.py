import json
import sys
from collections import defaultdict

from pathlib import Path
from typing import NamedTuple, Tuple, Sequence, Iterable

import logging

from ccmlib.node import Node

logger = logging.getLogger(__name__)


class Cell(NamedTuple):
    name: str
    value: str


class Row(NamedTuple):
    cells: Tuple[Cell]


class Partition(NamedTuple):
    key: Tuple[str]
    rows: Tuple[Row]


def parse_cell(raw_cell: dict):
    return Cell(
        name=raw_cell['name'],
        value=raw_cell['value']
    )


def parse_row(raw_row: dict):
    return Row(
        cells=tuple(parse_cell(raw_cell) for raw_cell in raw_row['cells'])
    )


def parse_partition(raw_partition: dict):
    return Partition(
        key=tuple(raw_partition['partition']['key']),
        rows=tuple(parse_row(raw_row) for raw_row in raw_partition['rows'])
    )


def json2partitions(s: str):
    raw_dump = json.loads(s)

    return tuple(parse_partition(raw_partition) for raw_partition in raw_dump)


def compare_sstable_dumps(d: Path):
    partitions = defaultdict(list)

    for path in d.glob('*.json'):
        with path.open() as dumpf:
            partitions[json2partitions(dumpf.read())].append(path)

    if len(partitions) == 1:
        logger.info('Dumps are identical.')
    else:
        logger.info('Dumps differ.')

    for partitions, files in partitions.items():
        logger.info('Partitions:')
        [logger.info(f'\t{p}') for p in partitions]
        logger.info('... are shared by the following dumps:')
        [logger.info(f'\t{f.name}') for f in files]


def flush_dump_compare(nodes: Iterable[Node], dump_dir: Path):
    logger.info('Flushing SSTables')
    for node in nodes:
        node.flush()

    logger.info('Compacting SSTables')
    for node in nodes:
        node.compact()

    logger.info('Dumping SSTables')
    for node in nodes:
        results = node.run_sstabledump(keyspace='example')
        for i, result in enumerate(results):
            path = (dump_dir / f'{node.ip_addr}-{i}.json')
            logger.info(f'Writing {node.ip_addr} dump to {path}')
            with path.open('wb') as f:
                f.write(result.stdout)

    logger.info('Comparing dumps')
    compare_sstable_dumps(dump_dir)


if __name__ == "__main__":
    compare_sstable_dumps(Path(sys.argv[1]))