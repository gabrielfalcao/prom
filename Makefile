main:
	echo "make prometheus"
	echo "make alertmanager"
	echo "make flask"

prometheus:
	prometheus --config.file=$(shell pwd)/prometheus.yml

alertmanager:
	alertmanager --config.file=$(shell pwd)/alertmanager.yml

web flask:
	pipenv run python webapp/app.py --debug

load:
	@for i in $$(seq 512); do if hey -n 8 -c 8 "http://localhost:5000/"; then echo -ne "\033[0m"; else break; fi; done
