#!/usr/bin/python
# -*- coding: ascii -*-
'''
Check by brute force (and a simple heuristic) if a given "sentence"
can be generated with different BNFs provided.

Last modified on 28.11.2012

@author: adrianus
'''

def apply_rule(node, root, occurence, new):
    """ Applies a rule to a given node at the given occurence of root. """
    count = 0
    for i in range(0, len(node)):
        if node[i] == root:
            if occurence == count:
                return node[:i] + new + node[i+1:]
            else:
                count += 1
                
def get_occurences(node, root):
    """ Count occurences of root in node. """
    count = 0
    for c in node: 
        if c == root: count += 1
    return count
    
def filter_impossible(children, depth, wanted):
    """ A simple filter for removing umpossible combinations. """
    i = 0
    while i < len(children[depth]):
        child = children[depth][i]
        if child.count('(') > wanted.count('(') or child.count('h') > wanted.count('h'): 
            del children[depth][i]
            i -= 1
        i += 1
    return children

def testfor(rule, wanted):
    """ Tests a given sentence (wanted) with a given BNF (rule)"""
    root = rule[0]
    max_depth = 10

    children = []
    children.append([root])
    for i in range(1, max_depth+1):
        children.append([])
    depth = 0
    variant = 0
    
    while depth < max_depth:
        # pick next node
        node = children[depth][variant]

        # generate all children by expanding node
        new_children = []
        for i in range(1, len(rule)):
            for occurence in range(0, get_occurences(node, root)):
                new_children.append(apply_rule(node, root, occurence, rule[i]))
    
        # check if we're finished
        if wanted in new_children: return True
        children[depth+1].extend(new_children)
        
        # iterate: decide which node to pick next
        if variant == len(children[depth])-1: # go down
            depth += 1
            variant = 0
            children[depth] = list(set(children[depth])) # remove duplicates
            children = filter_impossible(children, depth, wanted) # filter

            # if no more possibilities, we're finished
            if len(children[depth]) == 0: break
            
        else:
            variant += 1
    
    return False

def main():
    # read file
    f = open("bnf.txt", 'rb')
    lines = f.readlines()

    # parse text
    defs = []
    def_names = []
    tests = []
    test_names = []
    
    def_flag = False
    test_flag = False
    for line in lines:
        if test_flag and not line.startswith("#"):
            t = line.split(" ")
            test_names.append(t[0])
            tests.append(t[1].split("\n")[0])
        
        elif def_flag and not line.startswith("#"):
            defs.append(line)
            def_flag = False
            
        else: #reset flags
            test_flag = False
            def_flag = False
        
        if line.startswith('#def'):
            def_names.append(line.split(" ")[1].split("\n")[0])
            print "Definition found:", def_names[-1]
            def_flag = True
            
        elif line.startswith('#tests'):
            test_flag = True

    # building rules
    print "\nBuilding rules..."
    rules = []
    for d in defs:    
        d = d.split("|")
        l = []
        for part in d:
            if len(part.split(":=")) > 1: 
                l.append(part.split(":=")[0])
                part = part.split(":=")[1]
            if part == "_": l.append("")
            else: l.append(part)
        rules.append(l)
        
    print "Cleaning rules..."
    for rule in rules:
        root = rule[0].replace(' ', '')
        for i in range(0, len(rule)):
            rule[i] = rule[i].replace('\n', '')
            rule[i] = rule[i].replace('_', '')
            rule[i] = rule[i].replace(root, 'x')
            rule[i] = rule[i].replace('"', '')
            rule[i] = rule[i].replace(' ', '')
            
    print "rules:", rules
    print "\nRunning tests..."

    # tests
    for test in range(0, len(tests)):
        possible = []
        for d in range(0, len(defs)):
            possible.append(testfor(rules[d], tests[test]))
        
        info = "Test " + test_names[test] + " " + tests[test] + " <-- "
        for p in range(0, len(possible)):
            if possible[p]:
                info += def_names[p] + " "
        print(info)

if __name__ == "__main__":
    main()
