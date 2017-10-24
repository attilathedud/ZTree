# ZTree

This project is no longer being maintained and has been supplanted by [Inform Mapper.](https://github.com/attilathedud/inform_mapper/)

<div>
  <img src="https://attilathedud.github.io/ZTree/display_mode_0.png" alt="display mode 0">
  Display mode 0 shows every node present in the game and links objects to their parents. Passing in the sibling flag will also display sibling relations between nodes.
  <img src="https://attilathedud.github.io/ZTree/display_mode_1.png" alt="display mode 1">
  Display mode 1 shows all the rooms in the game with directional edges drawn. Nodes that aren't legally interpreted as rooms but can be moved to will be displayed as just text.
  <img src="https://attilathedud.github.io/ZTree/display_mode_2.png" alt="display mode 2">
  Display mode 2 shows all the objects in the game and their relations (e.g., if a pen is inside a drawer inside a desk).
  <img src="https://attilathedud.github.io/ZTree/display_mode_3.png" alt="display mode 3">
  Display mode 3 shows all objects inside their respective room with directions between rooms drawn. Somewhat experimental. Objects with no valid room as drawn as text with no node.
</div>

## About
ZTree is a python graphing tool that constructs network graphs of Z-Machine games (http://inform-fiction.org/zmachine/). It is packaged with a slimmed-down version of Mark Howell's ZTools to dump the game files. A helper script can be found in the "Scripts" directory and is supposed to be run from there like so:
```
./dump_game ../Games/awaken.z5
```

Dumps of the following games are already provided (as they were used for testing):
- Adventureland
- awaken
- happy

These dumps (specifically the object files) are then passed into the ZTree.py parser like follows:
```
python ZTree.py -o ../Dumps/awaken.z5_object_dump -n 1,2,3,4,6,19,20,21,22,23,118,125 -d 1

python ZTree.py -o ../Dumps/Adventureland.z5_object_dump -n 2,4,6

python ZTree.py -o ../Dumps/happy.z5_object_dump -n 1,2,4,6,19,20,21,22,24 -d 3
```

ZTree then uses Matplotlib to display an interactive version of the networked graph of nodes.

Usage options are as follows:
```
usage: ZTree.py -o <object_file> -n <node1,node2,node3>

ZTree version 1.0 - maps Infocom story files into a directional graph. By Nathan Tucker.

	-o, --objects	path to object file (from infodump -o)
	-s, --siblings	display sibling relations (default false)
	-n, --nodes	comma-separated list of nodes to ignore
	-d, --display	display all nodes(0), only rooms(1), only objects(2), objects in rooms(3)

example: ZTree.py -o ../Dumps/awaken.z5 -n 1,4,6,118,125
```

The different display modes are shown above.

## Source
ZTree is licensed under the Apache License, so feel free to play around with the source. It uses the following resources from the following sources:
- https://networkx.github.io/
- http://brew.sh/
- http://penandpants.com/2013/04/04/install-scientific-python-on-mac-os-x/
- https://github.com/Homebrew/homebrew-python
- graphviz from brew
- https://pygraphviz.github.io/
- http://inform-fiction.org/zmachine/ztools.html
- http://ifarchive.org/if-archive/games/zcode/
