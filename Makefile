all:
	docker run \
		--rm \
		--pull=always \
		-p 8124:8123 \
		-v $(PWD)/config/:/config \
		-v $(PWD)/custom_components/rutenbeck_tcr:/config/custom_components/rutenbeck_tcr \
		homeassistant/home-assistant
