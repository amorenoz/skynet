SKYDIVE_REPO?=https://github.com/amorenoz/skydive.git
SKYDIVE_REF?=rfe/ovn-sb
SKYNET_WORKDIR?=$(shell pwd)/workdir
SKYDIVE_IMG?=skydive:devel
RUNC_CMD?=docker

GOPATH=$(SKYNET_WORKDIR)/go
SKYDIVE_DIR=$(GOPATH)/src/github.com/skydive-project/skydive

OVN_FAKE_BUILD_FLAGS="WITH_LIBVIRT_GO=false \
                      WITH_LXD=false \
                      WITH_OPENCONTRAIL=false \
                      WITH_K8S=false \
                      WITH_ISTIO=false \
                      WITH_DPDK=false \
                      WITH_HELM=false"

.PHONY: help
help: ## Show this help.
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: skydive
skydive: bin/skydive ## Build the skydive binary (result in bin/skydive)

k8s: BUILD_FLAGS=$(K8S_BUILD_FLAGS) ## Build skydive binary and image (tagged as "skydive::devel") for Kubernetes
k8s: bin/skydive
	@cp bin/skydive images/skydive
	@cd images/skydive; $(RUNC_CMD) build -t $(SKYDIVE_IMG) . && rm skydive


ovn-fake-multinode: BUILD_FLAGS=$(OVN_FAKE_BUILD_FLAGS) ## Build skydive for ovn-fake-multinode
ovn-fake-multinode: bin/skydive

bin/skydive: ${SKYDIVE_DIR}/skydive
	cp $(SKYDIVE_DIR)/skydive bin

$(SKYDIVE_DIR)/skydive: $(SKYDIVE_DIR)
	@export GOPATH=$(GOPATH);  \
	make -C $(SKYDIVE_DIR) build $(BUILD_FLAGS); \
	make -C $(SKYDIVE_DIR) install

$(SKYDIVE_DIR):
	@mkdir -p $(GOPATH)/src/github.com/skydive-project
	@git clone https://github.com/skydive-project/skydive.git $(SKYDIVE_DIR)
	@(cd $(SKYDIVE_DIR); \
        if [[ $(SKYDIVE_REPO) != "default" ]]; then \
            git remote add alt $(SKYDIVE_REPO); \
            git fetch alt; \
            git checkout alt/$(SKYDIVE_REF); \
        fi)

.PHONY: clean
clean: ## Fast clean the the skydive binary (useful to quickly rebuild skydive changes)
	@rm -f bin/skydive
	@rm -f $(SKYDIVE_DIR)/skydive

.PHONY: fullclean
fullclean: clean ## Fully clean all the working directory
	@export GOPATH=$(GOPATH); go clean -modcache
	@rm -fr $(SKYDIVE_DIR);
	@$(RUNC_CMD) rmi $(SKYDIVE_IMG) 2>/dev/null || true

