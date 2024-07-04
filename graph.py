import base64
import os
import sys
import zlib

GRAPH_HEADER = """\
digraph G {
    node [margin=0.1 fontcolor=white fontsize=32 width=0.5 shape=box style=filled]
    graph [splines=ortho]
"""

graph = ""

GRAPH_FOOTER = """\
}
"""

def breed_python(fn: str) -> str:
    global graph

    path = os.path.dirname(fn)
    if fn.endswith('/__init__.py'):
        bn = os.path.basename(path)
        path = path[:-(len(bn)+1)]
    else:
        bn = os.path.basename(fn).replace('.py', '')

    while path and os.path.exists(os.path.join(path, '__init__.py')):
        pbn = os.path.basename(path)
        bn = '%s.%s' % (pbn, bn)
        path = path[:-(len(pbn)+1)]

    imports = []
    with open(fn, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('import'):
                for i in line.split(', ')[1:]:
                    j = i.replace('\n', '')
                    if j not in sys.stdlib_module_names or j.split('.')[0] not in sys.stdlib_module_names:
                        if j[0] == '.':
                            j = '.'.join(bn.split('.')[:-1]) + j
                        imports.append(j)
            elif line.startswith('from'):
                j =line.split(' ')[1] 
                if j not in sys.stdlib_module_names or j.split('.')[0] not in sys.stdlib_module_names:
                    if j[0] == '.':
                        j = '.'.join(bn.split('.')[:-1]) + j
                    imports.append(j)

    print(fn, imports)
    for i in imports:
        graph += '    "%s" -> "%s";\n' % (bn, i)
    return ""

def breed_dir(dn: str) -> str:
    files = [f for f in os.listdir(dn) if not f.startswith('.')]

    # Make sure __init__.py is FIRST.
    if '__init__.py' in files:
        files.remove('__init__.py')
        files[0:0] = ['__init__.py']

    # Make sure __main__.py is either excluded, or LAST
    if '__main__.py' in files:
        files.remove('__main__.py')
        files.append('__main__.py')

    for f in files:
        fn = os.path.join(dn, f)
        breed(fn)

    return ""


def breed(fn: str) -> str:
    if os.path.isdir(fn):
        return breed_dir(fn)
    
    extension = fn.split('.')[-1].lower()
    if extension in ('py', 'pyw'):
        return breed_python(fn)

    

if __name__ == "__main__":
    breed(sys.argv[1])

    with open('graph.dot', 'w') as f:
        f.write(GRAPH_HEADER)
        f.write(graph)
        f.write(GRAPH_FOOTER)
