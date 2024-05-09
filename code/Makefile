all: clean run

run: clean
	ryu-manager emergency_slicing.py &
	echo
	sudo python3 my_network.py

clean:
	mn -c
