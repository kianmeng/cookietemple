import os
from subprocess import Popen

import autopep8
import click

from cookietemple.create.create_config import TEMPLATE_STRUCT
from cookietemple.linting.TemplateLinter import TemplateLinter, files_exist_linting

CWD = os.getcwd()


class CliPythonLint(TemplateLinter):
    def __init__(self, path):
        super().__init__(path)

    def lint(self, label):
        methods = ['python_files_exist', 'python_version_consistent']
        super().lint_project(self, methods, label=label)

        # call autopep8
        project_name = TEMPLATE_STRUCT['project_slug']
        project_path = f'{CWD}/{project_name}'
        click.echo(click.style('Running autopep8 to fix pep8 issues in place', ))
        autopep8 = Popen(['autopep8', project_path, '--recursive', '--in-place', '--pep8-passes', '2000'], universal_newlines=True, shell=False, close_fds=True)
        (autopep8_stdout, autopep8_stderr) = autopep8.communicate()

    def python_files_exist(self) -> None:
        """
        Checks a given pipeline directory for required files.
        Iterates through the templates's directory content and checkmarks files for presence.
        Files that **must** be present::
            'setup.py',
            'setup.cfg',
            'MANIFEST.in',
            'tox.ini',
        Files that *should* be present::
            '.github/workflows/build_package.yml',
            '.github/workflows/publish_package.yml',
            '.github/workflows/tox_testsuite.yml',
            '.github/workflows/flake8.yml',
        Files that *must not* be present::
            none
        Files that *should not* be present::
            '__pycache__'
        """

        # NB: Should all be files, not directories
        # List of lists. Passes if any of the files in the sublist are found.
        files_fail = [
            ['setup.py'],
            ['setup.cfg'],
            ['MANIFEST.in'],
            ['tox.ini'],
        ]
        files_warn = [
            [os.path.join('.github', 'workflows', 'build_package.yml')],
            [os.path.join('.github', 'workflows', 'publish_package.yml')],
            [os.path.join('.github', 'workflows', 'tox_testsuite.yml')],
            [os.path.join('.github', 'workflows', 'flake8_linting.yml')],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [
            '__pycache__'
        ]
        files_warn_ifexists = [

        ]

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists)

    def python_version_consistent(self) -> None:
        """
        # TODO implement this
        This method should check that the version is consistent across all files.
        """
        pass
