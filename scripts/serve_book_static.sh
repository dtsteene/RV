#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

host="${HOST:-127.0.0.1}"
port="${PORT:-3300}"
url="http://${host}:${port}/"
pid_file=".myst-static-preview.pid"

stop_build_theme_server() {
    local theme_dir
    theme_dir="$(pwd)/_build/templates/site/myst/book-theme"
    while read -r pid; do
        [[ -z "${pid}" ]] && continue
        local cwd
        cwd="$(readlink -f "/proc/${pid}/cwd" 2>/dev/null || true)"
        if [[ "${cwd}" == "${theme_dir}" ]]; then
            kill "${pid}" 2>/dev/null || true
        fi
    done < <(pgrep -u "${USER}" -f 'node ./server.js' || true)
}

echo "RV static book preview"
echo "host: $(hostname -f 2>/dev/null || hostname)"
echo "url:  ${url}"
echo

if [[ -f "${pid_file}" ]]; then
    old_pid="$(cat "${pid_file}" 2>/dev/null || true)"
    if [[ -n "${old_pid}" ]] && kill -0 "${old_pid}" 2>/dev/null; then
        echo "Stopping previous static preview process ${old_pid}."
        kill "${old_pid}" 2>/dev/null || true
        sleep 1
    fi
fi

if ss -ltn "sport = :${port}" | grep -q LISTEN; then
    echo "Port ${port} is already in use by another process."
    echo "Stop that process or run with a different port, for example: PORT=3301 bash scripts/serve_book_static.sh"
    exit 1
fi

conda run -n RV myst build --html --strict
stop_build_theme_server

echo "Serving _build/html on ${url}"
echo "In VS Code: Ports tab -> Forward Port ${port} -> open the forwarded address."
echo "$$" > "${pid_file}"
exec python -m http.server "${port}" --bind "${host}" -d _build/html
