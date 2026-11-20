#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Fast launch: only compile if binary is missing or source code has changed
if [ ! -f "portfolio_server" ] || [ "src/main.rs" -nt "portfolio_server" ]; then
    echo "🦀 Compiling optimized Rust Portfolio Server..."
    rustc -O src/main.rs -o portfolio_server
fi

echo "🚀 Launching Rust Dynamic Portfolio Server on http://localhost:3000 ..."
exec ./portfolio_server
