#!/bin/bash

usage () {

    echo "Usage:


    
         docker run <container> [help|list|test-experiments|start]
         docker run -p 80:80 -v /tmp/data:/scif/data <container> start

         Commands:

                help: show help and exit
                list: list experiments in the library
                test: test experiments installed in container
                start: start the container to do the experiments*
                env: search for an environment variable set in the container
         
         *you are required to map port 80, otherwise you won't see the portal at localhost

         Options [start]:

                --db: specify a database url to override the default filesystem
                                 [sqlite|mysql|postgresql]:///

                --studyid:  specify a studyid to override the default

         Examples:

              docker run <container> test
              docker run <container> list
              docker run <container> start
              docker run -p 80:80 <container> --database mysql+pymysql://username:password@host/dbname start
              docker run -p 80:80 <container> --database sqlite start
              docker run -p 80:80 <container> --database postgresql://username:password@host/dbname start

         "
}

if [ $# -eq 0 ]; then
    usage
    exit
fi

EXPFACTORY_START="no"
EXPFACTORY_DATABASE="filesystem"

while true; do
    case ${1:-} in
        -h|--help|help)
            usage
            exit
        ;;
        -test-experiments|--te|test)
            cd /opt/expfactory/expfactory/templates/build
            exec python3 -m unittest tests.test_experiment
            exit
        ;;
        --env|env)
            shift
            env | grep ${1:-}
            exit
        ;;
        --database|--db)
            shift
            EXPFACTORY_DATABASE=${1:-}
            shift
        ;;
        --studyid)
            shift
            EXPFACTORY_STUDY_ID=${1:-}
            echo "Study ID selected as ${EXPFACTORY_STUDYID}"
            export EXPFACTORY_STUDY_ID
            shift
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
            EXPFACTORY_START="yes"
            shift
        ;;
        -*)
            echo "Unknown option: ${1:-}\n"
            exit 1
        ;;
        *)
            break
        ;;
    esac
done

# Are we starting the server?

if [ "${EXPFACTORY_START}" == "yes" ]; then

    echo "Database set as ${EXPFACTORY_DATABASE}"
    export EXPFACTORY_DATABASE

    echo "Starting Web Server"
    echo
    service nginx start
    touch /scif/logs/gunicorn.log
    touch /scif/logs/gunicorn-access.log
    tail -n 0 -f /scif/logs/gunicorn*.log &

    exec  gunicorn expfactory.wsgi:app \
                  --bind 0.0.0.0:5000 \
                  --name expfactory_experiments
                  --workers 5
                  --log-level=info
                  --log-file=/scif/logs/gunicorn.log \
                  --access-logfile=/scif/logs/gunicorn-access.log \
            "$@" & service nginx restart

    # simple manual command could be
    # service nginx start
    # gunicorn --bind 0.0.0.0:5000 expfactory.wsgi:app
    #service nginx restart

    # Keep container running if we get here
    tail -f /dev/null
    exit
fi
