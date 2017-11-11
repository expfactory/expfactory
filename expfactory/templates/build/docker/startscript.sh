#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "docker run vanessa/expfactory:builder [build|list|test-experiments]"
    expfactory --help
    exit
fi


while true; do
    case ${1:-} in
        -h|--help|help)

            echo "Additional commands:
                  docker run vanessa/expfactory:builder test-experiments"

            exec expfactory --help
            exit
        ;;
        -test-experiments|--te)
            cd /opt/expfactory/expfactory/templates/build/singularity
            exec python3 -m unittest tests.test_experiments
            exit
        ;;
        -ls|--list)
            echo "Experiments in the library:"
            echo
            echo "Experiments in this image:"
            ls /scif/apps -1
            echo
            exec expfactory list
            exit
        ;;
        -*)
            message ERROR "Unknown option: ${1:-}\n"
            exit 1
        ;;
        *)
            break
        ;;
    esac
done

service nginx start
gunicorn --bind 0.0.0.0:5000 expfactory.wsgi:app
service nginx restart
