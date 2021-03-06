"""Generic node traverser visitor"""

from extyper.traverser import TraverserVisitor
from extyper.nodes import Block, MypyFile


class TreeFreer(TraverserVisitor):
    def visit_block(self, block: Block) -> None:
        super().visit_block(block)
        block.body.clear()


def free_tree(tree: MypyFile) -> None:
    """Free all the ASTs associated with a module.

    This needs to be done recursively, since symbol tables contain
    references to definitions, so those won't be freed but we want their
    contents to be.
    """
    tree.accept(TreeFreer())
    tree.defs.clear()
