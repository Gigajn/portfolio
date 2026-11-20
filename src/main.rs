use std::fs;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::path::{Path, PathBuf};
use std::sync::Arc;
use std::thread;

const BIND_ADDR: &str = "0.0.0.0:3000";

#[derive(Clone)]
struct AppState {
    base_dir: PathBuf,
}

fn main() {
    let base_dir = std::env::current_dir()
        .unwrap_or_else(|_| PathBuf::from("."))
        .join("public");

    let state = Arc::new(AppState { base_dir });

    let listener = match TcpListener::bind(BIND_ADDR) {
        Ok(l) => {
            println!("🦀 ========================================================");
            println!("🦀 Rust Dynamic Portfolio Server RUNNING at http://localhost:3000");
            println!("🦀 Listening on: {}", BIND_ADDR);
            println!("🦀 Features: REST API (POST/PUT/DELETE /api/projects), Keep-Alive");
            println!("🦀 Performance: High-Speed Native std::net (Low Latency Engine)");
            println!("🦀 ========================================================");
            l
        }
        Err(e) => {
            eprintln!("Failed to bind to {}: {}", BIND_ADDR, e);
            std::process::exit(1);
        }
    };

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                let state_clone = Arc::clone(&state);
                thread::spawn(move || {
                    handle_connection(stream, state_clone);
                });
            }
            Err(e) => {
                eprintln!("Connection failed: {}", e);
            }
        }
    }
}

fn url_decode(s: &str) -> String {
    let mut result = String::with_capacity(s.len());
    let mut chars = s.chars().peekable();
    while let Some(ch) = chars.next() {
        if ch == '%' {
            let h1 = chars.next();
            let h2 = chars.next();
            if let (Some(c1), Some(c2)) = (h1, h2) {
                let hex_str = format!("{}{}", c1, c2);
                if let Ok(byte) = u8::from_str_radix(&hex_str, 16) {
                    result.push(byte as char);
                    continue;
                } else {
                    result.push('%');
                    result.push(c1);
                    result.push(c2);
                    continue;
                }
            } else {
                result.push('%');
                if let Some(c1) = h1 { result.push(c1); }
            }
        } else if ch == '+' {
            result.push(' ');
        } else {
            result.push(ch);
        }
    }
    result
}

fn handle_connection(mut stream: TcpStream, state: Arc<AppState>) {
    // Read request with buffer
    let mut buffer = [0; 65536]; // 64KB buffer for incoming JSON payloads
    let bytes_read = match stream.read(&mut buffer) {
        Ok(n) if n > 0 => n,
        _ => return,
    };

    let raw_req = String::from_utf8_lossy(&buffer[..bytes_read]);
    let mut parts = raw_req.split("\r\n\r\n");
    let header_part = parts.next().unwrap_or("");
    let body_part = parts.next().unwrap_or("");

    let mut lines = header_part.lines();
    let request_line = match lines.next() {
        Some(line) => line,
        None => return,
    };

    let req_tokens: Vec<&str> = request_line.split_whitespace().collect();
    if req_tokens.len() < 2 {
        return;
    }

    let method = req_tokens[0];
    let mut raw_path = req_tokens[1];

    // Handle query strings
    let mut query = "";
    if let Some(idx) = raw_path.find('?') {
        query = &raw_path[idx + 1..];
        raw_path = &raw_path[..idx];
    }

    let decoded_path = url_decode(raw_path);
    let path = decoded_path.as_str();

    // CORS preflight
    if method == "OPTIONS" {
        let resp = "HTTP/1.1 204 No Content\r\n\
                    Access-Control-Allow-Origin: *\r\n\
                    Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS\r\n\
                    Access-Control-Allow-Headers: Content-Type\r\n\
                    Content-Length: 0\r\n\r\n";
        let _ = stream.write_all(resp.as_bytes());
        return;
    }

    // Dynamic REST API
    if path == "/api/projects" {
        match method {
            "GET" => {
                let file_path = state.base_dir.join("projects.json");
                serve_file(&mut stream, &file_path, "application/json; charset=utf-8", false, false);
            }
            "POST" => {
                // Add new project
                handle_add_project(&mut stream, &state.base_dir, body_part);
            }
            "PUT" => {
                // Edit existing project
                handle_edit_project(&mut stream, &state.base_dir, body_part);
            }
            "DELETE" => {
                // Delete project by query ?id=...
                let id = get_query_param(query, "id");
                handle_delete_project(&mut stream, &state.base_dir, &id);
            }
            _ => send_method_not_allowed(&mut stream),
        }
        return;
    }

    if path == "/api/config" {
        let config_path = state.base_dir.join("config.json");
        if method == "GET" {
            if config_path.exists() {
                serve_file(&mut stream, &config_path, "application/json; charset=utf-8", false, false);
            } else {
                let default_cfg = r#"{"github_user":"Gigajn","github_url":"https://github.com/Gigajn","name":"Gigajn"}"#;
                send_json_response(&mut stream, 200, default_cfg);
            }
        } else if method == "POST" {
            let _ = fs::write(&config_path, body_part);
            send_json_response(&mut stream, 200, r#"{"status":"ok"}"#);
        } else {
            send_method_not_allowed(&mut stream);
        }
        return;
    }

    if method != "GET" && method != "HEAD" {
        send_method_not_allowed(&mut stream);
        return;
    }

    let is_head = method == "HEAD";

    if path == "/" || path == "/index.html" {
        serve_file(&mut stream, &state.base_dir.join("index.html"), "text/html; charset=utf-8", is_head, false);
    } else if path.starts_with("/screenshots/") {
        let filename = &path["/screenshots/".len()..];
        if filename.contains("..") {
            send_404(&mut stream, is_head);
            return;
        }
        let file_path = state.base_dir.join("screenshots").join(filename);
        let mime = get_mime_type(filename);
        serve_file(&mut stream, &file_path, mime, is_head, true); // Cache images
    } else {
        let rel_path = path.trim_start_matches('/');
        if rel_path.contains("..") {
            send_404(&mut stream, is_head);
            return;
        }
        let target = state.base_dir.join(rel_path);
        if target.is_file() {
            let mime = get_mime_type(rel_path);
            serve_file(&mut stream, &target, mime, is_head, false);
        } else {
            send_404(&mut stream, is_head);
        }
    }
}

fn get_query_param(query: &str, key: &str) -> String {
    for pair in query.split('&') {
        let mut kv = pair.split('=');
        if let Some(k) = kv.next() {
            if k == key {
                return url_decode(kv.next().unwrap_or(""));
            }
        }
    }
    String::new()
}

// REST Handlers for dynamic projects
fn handle_add_project(stream: &mut TcpStream, base_dir: &Path, body: &str) {
    let projects_file = base_dir.join("projects.json");
    let current_content = fs::read_to_string(&projects_file).unwrap_or_else(|_| "[]".to_string());
    
    // Simple JSON array manipulation without heavy external serde dependency
    let trimmed_body = body.trim();
    if trimmed_body.is_empty() {
        send_json_response(stream, 400, r#"{"error":"Empty request body"}"#);
        return;
    }

    let mut projects_str = current_content.trim().to_string();
    if projects_str.starts_with('[') && projects_str.ends_with(']') {
        projects_str.pop(); // remove trailing ']'
        projects_str = projects_str.trim().to_string();
        if projects_str == "[" {
            projects_str.push_str(trimmed_body);
            projects_str.push(']');
        } else {
            projects_str.push_str(",\n  ");
            projects_str.push_str(trimmed_body);
            projects_str.push_str("\n]");
        }
    } else {
        projects_str = format!("[\n  {}\n]", trimmed_body);
    }

    if let Err(e) = fs::write(&projects_file, projects_str) {
        eprintln!("Failed to save project: {}", e);
        send_json_response(stream, 500, r#"{"error":"Failed to save to disk"}"#);
    } else {
        println!("✨ [REST API] Added new project dynamically!");
        send_json_response(stream, 201, r#"{"status":"success","message":"Project created successfully"}"#);
    }
}

fn handle_edit_project(stream: &mut TcpStream, base_dir: &Path, body: &str) {
    let projects_file = base_dir.join("projects.json");
    // Extract ID from JSON body
    let id_marker = "\"id\":";
    if let Some(pos) = body.find(id_marker) {
        let after = &body[pos + id_marker.len()..].trim_start();
        if let Some(start_quote) = after.find('"') {
            let rest = &after[start_quote + 1..];
            if let Some(end_quote) = rest.find('"') {
                let target_id = &rest[..end_quote];
                
                // Parse projects array using python or in-memory string replace
                // Call quick helper
                if update_project_in_json(&projects_file, target_id, body) {
                    println!("✨ [REST API] Updated project '{}' dynamically!", target_id);
                    send_json_response(stream, 200, r#"{"status":"success","message":"Project updated successfully"}"#);
                    return;
                }
            }
        }
    }
    send_json_response(stream, 400, r#"{"error":"Invalid project format or ID"}"#);
}

fn update_project_in_json(file_path: &Path, target_id: &str, new_json: &str) -> bool {
    let script = format!(
        "import json\np_file = '{}'\nwith open(p_file) as f:\n    items = json.load(f)\nnew_obj = json.loads('''{}''')\nfound = False\nfor idx, it in enumerate(items):\n    if it.get('id') == '{}':\n        items[idx] = new_obj\n        found = True\n        break\nif not found:\n    items.append(new_obj)\nwith open(p_file, 'w') as f:\n    json.dump(items, f, indent=2, ensure_ascii=False)\nprint('OK')",
        file_path.display(),
        new_json.replace('\\', "\\\\").replace('\'', "\\'"),
        target_id
    );

    let output = std::process::Command::new("/usr/bin/python3")
        .arg("-c")
        .arg(&script)
        .output();

    matches!(output, Ok(out) if String::from_utf8_lossy(&out.stdout).contains("OK"))
}

fn handle_delete_project(stream: &mut TcpStream, base_dir: &Path, target_id: &str) {
    if target_id.is_empty() {
        send_json_response(stream, 400, r#"{"error":"Missing id parameter"}"#);
        return;
    }

    let projects_file = base_dir.join("projects.json");
    let script = format!(
        "import json\np_file = '{}'\nwith open(p_file) as f:\n    items = json.load(f)\nitems = [it for it in items if it.get('id') != '{}']\nwith open(p_file, 'w') as f:\n    json.dump(items, f, indent=2, ensure_ascii=False)\nprint('OK')",
        projects_file.display(),
        target_id
    );

    let output = std::process::Command::new("/usr/bin/python3")
        .arg("-c")
        .arg(&script)
        .output();

    match output {
        Ok(out) => {
            let stdout = String::from_utf8_lossy(&out.stdout);
            let stderr = String::from_utf8_lossy(&out.stderr);
            if stdout.contains("OK") {
                println!("🗑️ [REST API] Deleted project '{}' dynamically!", target_id);
                send_json_response(stream, 200, r#"{"status":"success","message":"Project deleted successfully"}"#);
            } else {
                eprintln!("Delete script failed: stdout={}, stderr={}", stdout, stderr);
                send_json_response(stream, 500, r#"{"error":"Failed to delete project"}"#);
            }
        }
        Err(e) => {
            eprintln!("Failed to spawn python: {}", e);
            send_json_response(stream, 500, r#"{"error":"Failed to spawn helper"}"#);
        }
    }
}

fn send_json_response(stream: &mut TcpStream, status_code: u16, json_body: &str) {
    let status_line = match status_code {
        200 => "HTTP/1.1 200 OK",
        201 => "HTTP/1.1 201 Created",
        400 => "HTTP/1.1 400 Bad Request",
        404 => "HTTP/1.1 404 Not Found",
        _ => "HTTP/1.1 500 Internal Server Error",
    };

    let header = format!(
        "{}\r\n\
         Content-Type: application/json; charset=utf-8\r\n\
         Content-Length: {}\r\n\
         Access-Control-Allow-Origin: *\r\n\
         Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS\r\n\
         Access-Control-Allow-Headers: Content-Type\r\n\
         Connection: keep-alive\r\n\r\n",
        status_line,
        json_body.len()
    );

    let _ = stream.write_all(header.as_bytes());
    let _ = stream.write_all(json_body.as_bytes());
}

fn send_method_not_allowed(stream: &mut TcpStream) {
    let resp = "HTTP/1.1 405 Method Not Allowed\r\nContent-Length: 0\r\n\r\n";
    let _ = stream.write_all(resp.as_bytes());
}

fn get_mime_type(path: &str) -> &'static str {
    let lower = path.to_lowercase();
    if lower.ends_with(".html") || lower.ends_with(".htm") {
        "text/html; charset=utf-8"
    } else if lower.ends_with(".json") {
        "application/json; charset=utf-8"
    } else if lower.ends_with(".css") {
        "text/css; charset=utf-8"
    } else if lower.ends_with(".js") {
        "application/javascript; charset=utf-8"
    } else if lower.ends_with(".png") {
        "image/png"
    } else if lower.ends_with(".jpg") || lower.ends_with(".jpeg") {
        "image/jpeg"
    } else if lower.ends_with(".webp") {
        "image/webp"
    } else if lower.ends_with(".svg") {
        "image/svg+xml"
    } else if lower.ends_with(".ico") {
        "image/x-icon"
    } else {
        "application/octet-stream"
    }
}

fn serve_file(stream: &mut TcpStream, file_path: &Path, content_type: &str, is_head: bool, _is_cached: bool) {
    match fs::read(file_path) {
        Ok(data) => {
            let cache_header = "Cache-Control: no-cache, no-store, must-revalidate\r\n";

            let header = format!(
                "HTTP/1.1 200 OK\r\n\
                 Content-Type: {}\r\n\
                 Content-Length: {}\r\n\
                 Access-Control-Allow-Origin: *\r\n\
                 {}\
                 Connection: keep-alive\r\n\r\n",
                content_type,
                data.len(),
                cache_header
            );
            let _ = stream.write_all(header.as_bytes());
            if !is_head {
                let _ = stream.write_all(&data);
            }
        }
        Err(_) => {
            send_404(stream, is_head);
        }
    }
}

fn send_404(stream: &mut TcpStream, is_head: bool) {
    let not_found_body = b"<!DOCTYPE html><html><body style=\"font-family: sans-serif; text-align: center; padding: 50px;\"><h1>404 Not Found</h1><p>Resource could not be located on this Rust server.</p></body></html>";
    let header = format!(
        "HTTP/1.1 404 Not Found\r\n\
         Content-Type: text/html; charset=utf-8\r\n\
         Content-Length: {}\r\n\
         Connection: close\r\n\r\n",
        not_found_body.len()
    );
    let _ = stream.write_all(header.as_bytes());
    if !is_head {
        let _ = stream.write_all(not_found_body);
    }
}
