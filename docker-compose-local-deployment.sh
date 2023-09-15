#!/usr/bin/env bash

args=("$@")
function display_arg_error {
  echo "[INFO] Expected args: 'reset', or 'reload'."
}


if [ ${#args[@]} -eq 0 ] || [ ${#args[@]} -gt 1 ]
then
  display_arg_error
elif [ ${#args[@]} -eq 1 ]
then
  case  $1 in
		"reset" ) echo "[INFO] We (re)initialize the application."
    docker-compose -f docker-compose-local.yml down -v
    sleep 2s
    docker-compose -f docker-compose-local.yml up -d --build
    sleep 1s
    docker-compose -f docker-compose-local.yml exec web python manage.py makemigrations authentication --noinput
    docker-compose -f docker-compose-local.yml exec web python manage.py makemigrations litreview --noinput
    docker-compose -f docker-compose-local.yml exec web python manage.py migrate --noinput
    docker-compose -f docker-compose-local.yml exec web python manage.py init_app_litreview
    docker-compose -f docker-compose-local.yml exec web python manage.py collectstatic --no-input --clear
		;;
		"reload" ) echo "[INFO] We (re)load application."
    docker-compose -f docker-compose-local.yml down -v
    docker-compose -f docker-compose-local.yml up -d
		;;
		*)
		display_arg_error
		;;
	esac
fi
