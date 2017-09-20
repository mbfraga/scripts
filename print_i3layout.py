#!/bin/env python3
# Print a semi-formatted layout of your i3 workspaces (including scratchpad,
# etc)


import i3ipc

def find_nodes(init_node, depth=1):
    for node in init_node.nodes:
        try:
            if depth ==1:
                print("   |-"*depth + node.name )
                #print("id: " + node.window)
            else:
                print("   "*depth + "|-" + node.name)
                #print("id: " + node.window)
        except:
            if depth ==1:
                print("   |-"*depth + node.layout)
            else:
                print("   "*depth + "|-" + node.layout)
            find_nodes(node, depth+1)
    for node in init_node.floating_nodes:
        try:
            if depth ==1:
                print("   |-"*depth + node.name + " [floating]")
                #print("id: " + node.window)
            else:
                print("   "*depth + "|-" + node.name + " [floating]")
                #print("id: " + node.window)
        except:
            if depth ==1:
                print("   |-"*depth + node.layout + " [floating]")
            else:
                print("   "*depth + "|-" + node.layout + " [floating]")
            find_nodes(node, depth+1)



i3 = i3ipc.Connection()

tree = i3.get_tree()
itertree = iter(tree.nodes)

for monitor in itertree:
    print("Monitor:", monitor.name, monitor.rect.x, monitor.rect.y, monitor.rect.width, monitor.rect.height)
    if monitor.name == '__i3':
        for workspace in monitor.nodes[0].nodes:
            print(" |-workspace:", workspace.name, "layout:",  workspace.layout)
            find_nodes(workspace)
    else:
        for workspace in monitor.nodes[1].nodes:
            print(" |-workspace:", workspace.name, "layout:",  workspace.layout)
            find_nodes(workspace)



