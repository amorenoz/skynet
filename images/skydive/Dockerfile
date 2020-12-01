ARG  BASE=fedora:29
FROM $BASE
RUN dnf install -y openvswitch libpcap libvirt \
    && dnf clean all \
    && rm -rf /var/cache/yum
COPY skydive /usr/bin/skydive
COPY skydive.yml /etc/skydive.yml
ENTRYPOINT ["/usr/bin/skydive", "--conf", "/etc/skydive.yml"]
