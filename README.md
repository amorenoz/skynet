# SkyNet

OVS/OVN visualization testing tools based on [Skydive](https://github.com/skydive-project/skydive)

## Getting started

### Installing skynet

Create a python virtual environment

        python -m venv venv; source venv/bin/activate

Install the local python package (development mode)

        pip install -r requirements.txt -e .

### Skydive
Skynet requires skydive to be running on the target cluster. This can be achieved by several
means.

This repository offers some scripts that aim to ease the deployment of skydive in some
platforms

Read [skydive's documentation](https://github.com/skydive-project/skydive)
for more information

#### Building skydive
Install skydive's building dependencies:

        dnf install protobuf-compiler protobuf-devel libpcap-devel

A Makefile is provided to ease the compilation of skydive:

        make skydive

This will download the right version of skydive (currently my private branch), build it
and install it in `bin/skydive`.

This Makefile (as well as many of the scripts) the directory `workdir` as working directory.
This can be modified by setting the `SKYNET_WORKDIR`


#### Deploy skydive
There are different ways to deploy skydive depending on your platform, see
[Supported Platforms](#supported-platforms)

### Run skynet
Once skydive has been deployed, skynet cli utility can be used

        skynet

See `skynet --help` for more information

## Supported Platforms
- [KIND (development)](#kind)
- [ovn-fake-multinode](#ovn-fake-multinode)

### KIND
To run the tool on a development-oriented KIND setup, a script called `skylab` is provided.
It helps setting up a KIND lab for development

### Requirements
- Only tested on Fedora (TODO: versions)
- Docker (note on recent Fedora versions you might need to disable cgroups v2.
Yo can do that by running `grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=0"
` and rebooting)
- golang
- Kubectl (There is a bug in 1.19.0 that messes up the port forwarding: https://github.com/kubernetes/kubectl/issues/929)
- On Fedora32, the recent change to use nftables as the default backend in
Firewalld has broken Docker networking, so I'm afraid you'll need to change it back to iptables:

      sed -i /etc/firewalld/firewalld.conf 's/FirewallBackend=.*/FirewallBackend=iptables/'
      systemctl restart firewalld
- Skydive requires many inotify watchers. In order to avoid future issues, increase the maximum inotify instances: `sudo sysctl user.max_inotify_instances=256`

### Create the lab

    ./scripts/skylab create

Note it will ask you for your sudo password for some operations (opening a port in firewalld)

### Start the lab
Build skydive's Kubernetes image:

    make k8s

And start the lab:

    ./scripts/skylab start

The KIND cluster can be access by exporting the created KUBECONFIG

    export KUBECONFIG=~/admin.conf

### Build skydive k8s image and load it to KIND
Possibly after modifying something in skydive's code in
`workdir/go/src/github.com/skydive-project/skydive`, just run the following
command to deploy the changes into the KIND lab

    ./scripts skylab apply

### Forward the skydive ports for convenience
The `k8s` script can be used for that:

    ./scripts k8s forward

Also, if you want to access Kibana to inspect the ElasticSearch database directly, run

    ./scripts/kibana start

If you're running skylab in a remote VM, you might need to forward those ports to your local host with a comand such as

    ssh -N -L 9200:localhost:9200 -L 8080:localhost:8082 virtlab510.virt.lab.eng.bos.redhat.com

### Hack skydive

    cd workdir/go/src/github.com/skydive-project/skydive
    ...modify code...

Build and redeploy skydive with the current working-dir changes

    ./scripts/skylab apply

### Stop the lab

    ./scripts/skylab stop

### Clean the lab

    ./scripts/skylab clean

## ovn-fake-multinode
If you're using [ovn-fake-multinode](https://github.com/ovn-org/ovn-fake-multinode) to test OVN/OVS,
first build skydive for this specific target

    make clean; make ovn-fake-multinode

### Install skydive onto ovn-fake-multinode
This will install skydive in `bin/skydive`. Then, install skydive into your
multinode fake cluster using the convenience script:

    sudo ./scripts/ovn-fake install bin/skydive
    Skydive successfully installed in ovn-fake-multinode
    Skydive API is available at 170.168.0.2:8082
    You can access the skydive's API by running your commands inside the 'ovnfake-int' namespace                                                                                                                         

### Run skynet
The above script will create a network namespace called `ovnfake-int` that has access to skydive's API:

    sudo --preserve-env=PWD ip netns exec ovnfake-int su -- $(whoami)

Download the requirements (if you haven't already) and run the tool:

    python -m venv venv; source venv/bin/activate; pip install -r requirements.txt; export PYTHONPATH=$PWD
    ./bin/skynet --skydive 170.168.0.2:8082 summary

### Uninstall skydive from ovn-fake-multinode
To uninstall the current skydive binary from your cluster run:

    sudo ./scripts/ovn-fake uninstall