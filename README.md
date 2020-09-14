# fdp-skydive

Testing Fast DataPath visualization in Skydive

## Requirements

- Only tested on Fedora (TODO: versions)
- Docker (note on recent Fedora versions you might need to disable cgroups v2. Yo can do that by running `grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=0"
` and rebooting)
- golang
- Kubectl (There is a bug in 1.19.0 that messes up the port forwarding: https://github.com/kubernetes/kubectl/issues/929)
- On Fedora32, the recent change to use nftables as the default backend in Firewalld has broken Docker networking, so I'm afraid you'll need to change it back to iptables:

      sed -i /etc/firewalld/firewalld.conf 's/FirewallBackend=.*/FirewallBackend=iptables/'
      systemctl restart firewalld


## skylab
**skylab** is a cli tool to start a skydive demo lab with ovn-k8s

### Create the lab

    skylab create

Note it will ask you for your sudo password for some operations (opening a port in firewalld)

### Start the lab

    skylab up


### Access the Skydive UI

    skylab forward &
    skydive kibana

Now you can access Skydive UI at localhost:8082 and Kibana dashboard at localhost:5601
If you're running skylab in a remote VM, you might need to forward those ports to your local host with a comand such as

    ssh -N -L 9200:localhost:9200 -L 8080:localhost:8082 virtlab510.virt.lab.eng.bos.redhat.com


### Stop the lab

    skylab down

### Clean the lab

    skylab up

