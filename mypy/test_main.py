from mypy import checker
import mypy.checkexpr
from mypy.parse import parse
from mypy.options import Options
from mypy.checker import TypeChecker
from mypy.build import BuildManager, State, load_graph
from mypy.modulefinder import BuildSource, SearchPaths
from mypy.version import __version__
from mypy.build import load_plugins_from_config
import os
import sys
from typing import List,Tuple, Dict
from mypy.plugins.default import DefaultPlugin
from mypy.plugin import Plugin, ChainedPlugin
from mypy.errors import Errors, CompileError, ErrorInfo, report_internal_error
from mypy.util import (
    DecodeError, decode_python_encoding, is_sub_path, get_mypy_comments, module_prefix,
    read_py_file, hash_digest, is_typeshed_file, is_stub_package_file, get_top_two_prefixes
)
from mypy.fscache import FileSystemCache
def default_data_dir() -> str:
    """Returns directory containing typeshed directory."""
    return os.path.dirname(__file__)
def load_plugins(options: Options,
                 errors: Errors,
                 stdout,
                 extra_plugins,
                 ) -> Tuple[Plugin, Dict[str, str]]:
    """Load all configured plugins.

    Return a plugin that encapsulates all plugins chained together. Always
    at least include the default plugin (it's last in the chain).
    The second return value is a snapshot of versions/hashes of loaded user
    plugins (for cache validation).
    """
    custom_plugins, snapshot = load_plugins_from_config(options, errors, stdout)

    # custom_plugins += extra_plugins

    default_plugin: Plugin = DefaultPlugin(options)
    if not custom_plugins:
        return default_plugin, snapshot

    # Custom plugins take precedence over the default plugin.
    return ChainedPlugin(options, custom_plugins + [default_plugin]), snapshot

def flush_errors(new_messages: List[str], serious: bool) -> None:
    print('flush errors')
def test_main():
    options = Options()
    tree = parse('a = f(1)', 'name', None, None, options)
    data_dir = default_data_dir()
    search_paths = SearchPaths((), (), (), ())
    source = BuildSource('/data/sunke/type/full_dataset/test_sub/a.py', 'a',None, None)
    source_set = set([source])
    fscache = FileSystemCache()
    cached_read = fscache.read
    errors = Errors(options.show_error_context,
                        options.show_column_numbers,
                        options.show_error_codes,
                        options.pretty,
                        lambda path: read_py_file(path, cached_read, options.python_version),
                        options.show_absolute_path,
                        options.enabled_error_codes,
                        options.disabled_error_codes,
                        options.many_errors_threshold)
    stdout = sys.stdout
    stderr = sys.stderr
    plugin, snapshot = load_plugins(options, errors, stdout, None)
    manager = BuildManager(data_dir, search_paths,
                            ignore_prefix=os.getcwd(),
                            source_set=source_set,
                            reports=None,
                            options=options,
                            version_id=__version__,
                            plugin=plugin,
                            plugins_snapshot=snapshot,
                            errors=errors,
                            flush_errors=flush_errors,
                            fscache=fscache,
                            stdout=stdout,
                            stderr=stderr)
    xpath = '<string>'
    graph = load_graph(source_set, manager)
    st = State(0, path='/data/sunke/type/full_dataset/test_sub/a.py', source=None, manager=manager,
                        root_source=True)
    st.parse_file()
    checker = TypeChecker(manager.errors, manager.modules, options,
                                                tree,  '<string>', manager.plugin)