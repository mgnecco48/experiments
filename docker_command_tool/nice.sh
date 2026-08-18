#!/usr/bin/env bash

options=(
    "Execute shell commands"
    "List services"
    "Takedown"
    "Rebuild"
    "Logs"
    "Exit"
)

width=$COLUMNS
gum style \
    --foreground "cyan" --border-foreground "cyan" --border="rounded" \
    --align center --width 40 --margin "1 2" --padding "2 4" \
    --bold 'Dockerizer' 'Your Docker friend!!!'

choice=$(printf "%s\n" "${options[@]}" | gum choose --header "What do you want to do")
case "$choice" in
"Execute shell commands")
    container=$(docker ps --format {{.Names}} | gum choose --header "Choose a container")
    docker exec -i "$container" sh
    ;;
"List services")
    docker compose ps
    ;;
"Takedown")
    docker compose down
    ;;
"Rebuild")
    docker compose up -d
    ;;
"Logs")
    service=$(docker compose ps --services | gum choose --header "Choose a service to view logs")
    docker compose logs "$service"
    ;;
"Exit")
    exit 1
    ;;
esac
