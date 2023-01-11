# This script is made to be sourced only
set -e

# Exports host's variables to ensure compatibility
export_host_variables() {
    if [[ "$OSTYPE" =~ 'linux' ]]; then
        export IS_LINUX=1
    else
        export IS_LINUX=0
    fi

    if test "$IS_LINUX" = 0; then
        shopt -s expand_aliases
        alias podman=docker
        alias podman-compose=docker-compose
    fi
}

export_host_variables

# Checks db container status
#
# Returns:
# 0 if db is ready, 1 if it isn't started in 60s
wait_for_db() {
    count=0
    while ! podman exec -it osh-hub pg_isready -h db; do
        sleep 1
        count=$((count + 1))
        if test "$count" -gt 60; then
            return 1
        fi
    done
    return 0
}

# Checks osh container status
#
# @param $1 container name (e.g. hub, worker, client)
#
# Returns:
# 0 if container is running, 1 if it isn't started in 60s
wait_for_container() {
    filename="$(echo "$1" | tr '[:lower:]' '[:upper:]')"
    filename+="_IS_READY"

    containername="osh-"
    containername+="$(echo "$1" | tr '[:upper:]' '[:lower:]')"

    count=0
    while ! podman exec -i "$containername" bash -c "[[ -f /$filename ]]"; do
        sleep 1
        count=$((count + 1))
        if test "$count" -gt 60; then
            return 1
        fi
    done
    return 0
}

# Checks against a program version
#
# @currentver Current software version
# @requiredver Minimum required version
#
# Returns:
# 0 if @currentver >= @requiredver and 1 otherwise
version_compare() {
    currentver="$1"
    requiredver="$2"

    sorted_ver="$(printf '%s\n' "$requiredver" "$currentver" | sort -V | head -n1)"
    if [ "$sorted_ver" = "$requiredver" ]; then
        return 0
    fi
    return 1
}