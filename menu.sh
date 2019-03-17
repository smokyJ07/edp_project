#!/bin/bash
cd /
cd /home/pi/Desktop/edp_program
choice="1"
until [ "$choice" = "0" ]; do
	echo -n "Enter a program to execute (1-SR,2-APP,0-quit):"
	read -t10 choice
	if [ $? -gt 128 ]; then
		echo "Timed out, SR starts on default..."
		choice="1"
	fi
	case $choice  in
		1 ) python3 p_recog4.py;;
		2 ) python3 app_recog.py;;
		0 ) exit;;
		* ) echo "Enter 1,2 or 0";;
	esac
done
cd /
