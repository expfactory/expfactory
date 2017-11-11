#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "docker run vanessa/expfactory:builder [help|list|test-experiments|start]"
    echo "docker run -p 80:80 -v /tmp/data:/scif/data vanessa/expfactory:builder start"
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
        -test-experiments|--te|test)
            cd /opt/expfactory/expfactory/templates/build/singularity
            exec python3 -m unittest tests.test_experiments
            exit
        ;;
        -ls|--list|list)
            echo "Experiments in this image:"
            ls /scif/apps -1
            echo
            echo "Experiments in the library:"
            exec expfactory list
            exit
        ;;
        -s|--start|start)
            echo "Starting Web Server"
            echo
            service nginx start
            gunicorn --bind 0.0.0.0:5000 expfactory.wsgi:app
            service nginx restart
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
