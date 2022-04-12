import antlr4
from nltk.tree import Tree
from nltk.draw.tree import draw_trees
from antlr4.tree.Trees import Trees
from generated.PAMLexer import PAMLexer
from generated.PAMParser import PAMParser
from ExtendedVisitor import ExtendedVisitor


def main():
    # read code from the text file
    # code = open('program.txt', 'r').read()
    code = open('input.txt', 'r').read()

    # using lexer and parser files set up the parsing process
    lexer = PAMLexer(antlr4.InputStream(code))
    stream = antlr4.CommonTokenStream(lexer)
    parser = PAMParser(stream)

    # get the syntax tree
    tree = parser.progr()

    # visit the tree (interpret the program)
    visitor = ExtendedVisitor()
    output = visitor.visit(tree)

    # transform the Tree to the string format and print to console
    tree_string = Trees.toStringTree(tree, None, parser)
    # print(tree_string)

    # draw the tree using nltk library available functionality
    tree_for_nltk = Tree.fromstring(tree_string)
    # draw_trees(tree_for_nltk)


if __name__ == '__main__':
    main()
