# fdp-skydive

Testing Fast DataPath visualization in Skydive

## skylab
**skylab** is a cli tool to start a skydive demo lab with ovn-k8s

Requirements:

- Only tested on Fedora (TODO: versions)
- Docker (note on recent Fedora versions you might need to disable cgroups v2. Yo can do that by running `grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=0"
` and rebooting)
- golang




