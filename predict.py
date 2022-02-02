import pickle
from mypy.main import process_options
import sys
from mypy import build
from mypy.fscache import FileSystemCache
from mypy.dmypy_server import Server
from mypy.dmypy_util import DEFAULT_STATUS_FILE
from mypy.build import sorted_components
from mypy.nodes import (
    ArgKind, ARG_STAR, ARG_STAR2, FuncDef, MypyFile, SymbolTable,
    Decorator, RefExpr,
    SymbolNode, TypeInfo, Expression, ReturnStmt, CallExpr,
    reverse_builtin_aliases,ClassDef
)
from typing import get_type_hints, Union
from collections.abc import Callable
from mypy.traverser import TraverserVisitor
from mypy.types import (
    Type, AnyType, CallableType, FunctionLike, Overloaded, TupleType, TypedDictType,
    Instance, NoneType, strip_type, TypeType, TypeOfAny,
    UnionType, TypeVarId, TypeVarType, PartialType, DeletedType, UninhabitedType,
    is_named_instance, union_items, TypeQuery, LiteralType,
    is_optional, remove_optional, TypeTranslator, StarType, get_proper_type, ProperType,
    get_proper_types, is_literal_type, TypeAliasType, TypeGuardedType)  
import mypy
import os
import argparse
from mypy.remover import TypeHintRemover
from mypy.stubgen import main_args
import ast
from mypy.build import process_graph
# a:Union[int,str,bool]
# def f(x):
#     x()
#     lis = get_type_hints(x)
#     print(lis)
# main()
# main_args(sys.argv[:2])
mutable_funcs = []
args = sys.argv[1:]
mode = args[1]
args = args[0:1]
print(args)


def build_cache(options):
    options.check_untyped_defs = True
    options.allow_redefinition = True
    options.incremental = True
    options.use_builtins_fixtures = False # 这个必须为False
    options.show_traceback = False
    options.error_summary = False
    options.fine_grained_incremental = False
    options.use_fine_grained_cache = False
    options.cache_fine_grained = False
    options.local_partial_types = False
    options.preserve_asts = True
    options.export_types = True
    options.check_untyped_defs = True
    options.strict_optional = True
    options.show_column_numbers = True
    
    return options
def order_function(order):
    return []

fscache = FileSystemCache()

def clear_annotation(path):
    source = open(path).read()
    # parse the source code into an AST
    parsed_source = ast.parse(source)
    # remove all type annotations, function return type definitions
    # and import statements from 'typing'
    transformed = TypeHintRemover().visit(parsed_source)
    # convert the AST back to source code
    transformed_code = ast.unparse(transformed)

    with open(path, 'w+') as f:
        f.write(transformed_code)
def clear_cache(module):
    module = module.replace('.','/')
    path1 = '.mypy_cache/3.9/' + module + '.data.json'
    path2 = '.mypy_cache/3.9/' + module + '.meta.json'
    if os.path.exists(path1):
        os.remove(path1)
    if os.path.exists(path2):
        os.remove(path2)
    path1 = '.mypy_cache/3.9/' + module + '/__init__.data.json'
    path2 = '.mypy_cache/3.9/' + module + '/__init__.meta.json'
    if os.path.exists(path1):
        os.remove(path1)
    if os.path.exists(path2):
        os.remove(path2)
    
sources, options = process_options(args, stdout=sys.stdout, stderr=sys.stderr,
                                    fscache=fscache)
options.mode = mode
for source in sources:
    # clear_annotation(source.path)
    clear_cache(source.module)
modules = [x.module for x in sources]
options = build_cache(options)
# rebuild or zhiru

result = build.build(sources=sources, options=options, modules=modules)
# 第三方库如果只有代码，也应该考虑
# server = Server(options, DEFAULT_STATUS_FILE)
# for source in sources:
#     clear_cache(source.module)
# response = server.check(result, sources, is_tty=False, terminal_width=-1)


# graph = server.fine_grained_manager.graph

# sccs = sorted_components(graph)
# targets_file = []
# user_types = []
# top_level_targets = []
# for scc in sccs:
#     for module in scc:
#         target_func = []
#         if module in modules and (module.find(main_name) != -1 if main_name is not None else True):
#             state = graph[module]
#             state._type_checker.reset()
#             for name in state.tree.names:
#                 symbol = state.tree.names[name]
#                 node = symbol.node
#                 if isinstance(node, TypeInfo):
#                     user_types.append(node)
#             # server.fine_grained_manager.update([(state.id, state.path)], [])
#             for def_ in state.tree.defs:
#                 if isinstance(def_, FuncDef):
#                     target_func.append((def_, state))
#                     mutable_funcs.append(def_.fullname)
#                 elif isinstance(def_, ClassDef):
#                     for ddef in def_.defs.body:
#                         if isinstance(ddef, FuncDef):
#                             target_func.append((ddef, state))
#                             mutable_funcs.append(ddef.fullname)
#             targets_file.append((module, target_func)) 

# user_type_instances = []
# origin_type_instances = []
# for typ in user_types:
#     any_type = AnyType(TypeOfAny.from_omitted_generics)
#     user_type_instances.append(Instance(typ, [any_type] * len(typ.defn.type_vars)))
#     origin_type_instances.append(Instance(typ, [any_type] * len(typ.defn.type_vars)))

# # targets, suggests, global_type_map, global_incompatible = server.suggest_whole_project(targets_file, user_types)
# server.fine_grained_manager.manager.server = server

# server.fine_grained_manager.manager.errors.reset()
# server.fine_grained_manager.manager.mutable_funcs.extend(mutable_funcs)
# global_type_map = server.suggest_whole_project(targets_file, user_types)
# process_graph(server.fine_grained_manager.graph, server.fine_grained_manager.manager)
# main_args(sys.argv[:2], graph)
# worklist = [['start']]
# single_incompatible1 = server.fine_grained_manager.manager.single_incompatible
# single_incompatible2 = server.fine_grained_manager.manager.errors.single_incompatible
# double_incompatible = server.fine_grained_manager.manager.incompatible
# def contains_all(items, state):
#     return all(item in state for item in items)
# for stub in global_type_map:
#     if stub.split(':')[-1] == 'self':
#         continue

#     assert len(global_type_map[stub]) > 0
#     new_worklist = []
#     for typ in global_type_map[stub]:
        
#         if (stub in single_incompatible1 and typ in single_incompatible1[stub]) or (stub in single_incompatible2 and typ in single_incompatible2[stub]):
#             continue
#         id_pair = (stub, typ)
#         tmp = []
#         for state in worklist:
#             if (id_pair not in double_incompatible) or (not any([contains_all(x, state) for x in double_incompatible[id_pair]])):
#                 new_state = [x for x in state]
#                 new_state.append(id_pair)
#                 new_worklist.append(new_state)
#             else:
#                 print('ok')
#     assert len(new_worklist) > 0
#     worklist = new_worklist
# print(worklist)
# # target_suggest = list(zip(targets, suggests))
# # with open('save_' + save_name,'wb') as f:
# #     pickle.dump(target_suggest, f)
