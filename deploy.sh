#!/usr/bin/env bash

APP_DIR=$(readlink -f $0 | xargs dirname)
UI_PORT=8888


__set_up_py_venv(){
	venv_dir=${APP_DIR}/venv
	if [ ! -d ${venv_dir} ];then
		virtualenv -p /usr/bin/python3.7 ${venv_dir}
	fi
	source ${venv_dir}/bin/activate

	# install deps
	pip install -r requirements.txt
}

__kill_process_by_name(){
	process_name=$1
	ps -ef | grep "${process_name}" | grep -v grep |awk '{print $2}' |xargs kill -9 > /dev/null 2>&1 || true
}

__start_web_ui(){
    proj_dir=$1
	pwdir=`pwd`
	cd ${proj_dir}

 	ui_svr_cnt=`ps -ef | grep 'index.py' | grep -v grep |wc -l`
	if [ 0==${ui_svr_cnt} ]; then
		echo "Stop UI"
		__kill_process_by_name "port=${UI_PORT}"
		echo "Restart UI"
		export FLASK_APP=index.py
		nohup python -m flask run --host=0.0.0.0 --port=${UI_PORT} > /dev/null 2>&1 &
	fi

	cd ${pwdir}
}


cd ${APP_DIR}
__set_up_py_venv
__start_web_ui ${APP_DIR}/ui/