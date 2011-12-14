#!/bin/bash

# diese variablen willst du vielleicht anfassen!!!
SAVE_FILE=".ehelp"
EXEC_CMD="smplayer"
#EXEC_CMD="vlc"
ECHO_CMD="kdialog --msgbox"
EXTENSIONS=`cat << END
avi
mkv
ogg
mp3
mpg
rmvb
END`

my_echo()
{
	sh -c "$ECHO_CMD '$1'"
}

exec_file()
{
	echo "$1" > $SAVE_FILE
	nohup $EXEC_CMD "$1" &> /dev/null &
}

is_media_file()
{
	end=${1##*\.}

	for i in $EXTENSIONS 
	do
		if [ "$i" == "$end" ]
		then
			return 0
		fi
	done

	return 1
}

search_dir()
{
	for i in `ls $1`
	do
		cur="$1/$i"

		if [ -d "$cur" ]
		then
			if search_dir "$cur"
			then
				return 0
			fi
		else
			if is_media_file "$cur"
			then
				if [ "$last" == "" ]
				then
					exec_file "$cur"
					return 0
				fi

				if [ "$last" == "$cur" ]
				then
					last=""
				fi
			fi
		fi
	done

	return 1
}

# newline splittet ... fuer's for
IFS=$'\n'

# ein parameter ... das verzeichnis in dem gearbeitet wird
if [ -d "$1" ]
then
	cd $1
elif [ "$1" != "" ]
then
	my_echo "First parameter must be a directory or blank for current directory."
	exit
fi

# laden
if [ -e $SAVE_FILE ]
then
	last=`cat $SAVE_FILE`
fi

search_dir .

if [ $? == 1 ]
then
	if [ "$last" == "" ]
	then
		my_echo "Last Episode reached. You may want to remove $SAVE_FILE"
	else
		my_echo "Bad Bookmark. You may want to remove $SAVE_FILE"
	fi
fi

