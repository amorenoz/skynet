# skynet

Fast DataPath visualization in Skydive


## Supported platforms
- KIND (development)
- ...

# Install skynet

Create a python virtual environment

        python -m venv venv; source venv/bin/activate

Install the local python package (development mode)

        pip install -r requirements.txt -e .

# Run sykdive

## Download and build skydive
For now, some features required for skynet to work are only in my private repo:

        git clone https://github.com/amorenoz/skydive.git
        git checkout rfe/ovn-sb

Build skydive:

        make && make install

## Deploy in Kubernetes
Copy the skydive binary to the images file and build skydive container

        pushd images/skydive
        cp {SKYDIVE_SOURCE_PATH}/skydive .
        docker build -t skydive:devel .
        popd

Deploy skydive into your cluster

        kubectl apply -f deployments/skydive.yaml

After a while, skydive will be running. Now, forward skydive's ports:

        kubectl port-forward --namespace skydive service/skydive-analyzer 8082 9200


# Run skynet
Once skydive has been deployed, skynet cli utility can be used

        skynet summary


See 'skynet --help' for more information


# Auxiliary tools
## skylab
**skylab** is a cli tool to start a skydive demo lab with ovn-k8s

### Requirements
- Only tested on Fedora (TODO: versions)
- Docker (note on recent Fedora versions you might need to disable cgroups v2. Yo can do that by running `grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=0"
` and rebooting)
- golang
- Kubectl (There is a bug in 1.19.0 that messes up the port forwarding: https://github.com/kubernetes/kubectl/issues/929)
- On Fedora32, the recent change to use nftables as the default backend in Firewalld has broken Docker networking, so I'm afraid you'll need to change it back to iptables:

      sed -i /etc/firewalld/firewalld.conf 's/FirewallBackend=.*/FirewallBackend=iptables/'
      systemctl restart firewalld


### Create the lab

    ./scripts/skylab create

Note it will ask you for your sudo password for some operations (opening a port in firewalld)

### Start the lab

    ./scripts/skylab up


### Access the Skydive UI

    ./scripts/skylab forward
    ./scripts/skylab kibana

Now you can access Skydive UI at localhost:8082 and Kibana dashboard at localhost:5601
If you're running skylab in a remote VM, you might need to forward those ports to your local host with a comand such as

    ssh -N -L 9200:localhost:9200 -L 8080:localhost:8082 virtlab510.virt.lab.eng.bos.redhat.com


### Hack skydive

    cd fdp-skydive/go/src/github.com/skydive-project/skydive
    ...modify code...

Build and redeploy skydive with the current working-dir changes

    ./scripts/skylab apply

### Stop the lab

    ./scripts/skylab down

### Clean the lab

    ./scripts/skylab up

