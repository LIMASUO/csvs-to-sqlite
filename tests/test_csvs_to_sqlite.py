from click.testing import CliRunner
from csvs_to_sqlite import cli
import sqlite3

CSV = '''county,precinct,office,district,party,candidate,votes
Yolo,100001,President,,LIB,Gary Johnson,41
Yolo,100001,President,,PAF,Gloria Estela La Riva,8
Yolo,100001,Proposition 51,,,No,398
Yolo,100001,Proposition 51,,,Yes,460
Yolo,100001,State Assembly,7,DEM,Kevin McCarty,572
Yolo,100001,State Assembly,7,REP,Ryan K. Brown,291'''


def test_flat():
    runner = CliRunner()
    with runner.isolated_filesystem():
        open('test.csv', 'w').write(CSV)
        result = runner.invoke(cli.cli, ['test.csv', 'test.db'])
        assert result.exit_code == 0
        assert result.output.strip().endswith('Created test.db from 1 CSV file')
        conn = sqlite3.connect('test.db')
        assert [
            (0, 'county', 'TEXT', 0, None, 0),
            (1, 'precinct', 'INTEGER', 0, None, 0),
            (2, 'office', 'TEXT', 0, None, 0),
            (3, 'district', 'REAL', 0, None, 0),
            (4, 'party', 'TEXT', 0, None, 0),
            (5, 'candidate', 'TEXT', 0, None, 0),
            (6, 'votes', 'INTEGER', 0, None, 0)
        ] == list(conn.execute('PRAGMA table_info(test)'))
        assert [
            ('Yolo', 100001, 'President', None, 'LIB', 'Gary Johnson', 41),
            ('Yolo', 100001, 'President', None, 'PAF', 'Gloria Estela La Riva', 8),
            ('Yolo', 100001, 'Proposition 51', None, None, 'No', 398),
            ('Yolo', 100001, 'Proposition 51', None, None, 'Yes', 460),
            ('Yolo', 100001, 'State Assembly', 7.0, 'DEM', 'Kevin McCarty', 572),
            ('Yolo', 100001, 'State Assembly', 7.0, 'REP', 'Ryan K. Brown', 291)
        ] == conn.execute('select * from test').fetchall()
