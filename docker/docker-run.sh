#!/bin/bash

run_docker_compose() {
    for app_name in "$@"; do
        compose_file="${app_name}/docker-compose.yml"
        env_file="${app_name}/.env"
        
        if [ ! -f "$compose_file" ] || [ ! -f "$env_file" ]; then
            echo "Error: Docker Compose file or .env file not found for ${app_name}. Skipping..."
            continue
        fi
        
        command="docker-compose --env-file ${env_file} -f ${compose_file} up -d"
        if $command; then
            echo "${app_name} started successfully."
        else
            echo "Error: Failed to start ${app_name}."
        fi
    done
}

# Check if app names are provided as command-line arguments
if [ "$#" -lt 1 ]; then
    echo "Please provide at least one app name as an argument."
    exit 1
fi

run_docker_compose "$@"
