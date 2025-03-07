def print_tree(lifelogs):
  for lifelog in lifelogs:
    root = lifelog.get("tree")
    
    def print_node(node, depth=0):
      text = node.get("content", "")
      if node.get("speakerName"):
        text = f"{node.get('speakerName')}: {text}"
      print("  " * depth + text, end="\n\n")
      for child in node.get("children", []):
        print_node(child, depth + 1)
    
    print_node(root)
