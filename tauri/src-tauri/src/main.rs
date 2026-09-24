// Cross-platform native shell for SQL Dojo, replacing the macOS-only Swift/SwiftUI/WKWebView
// shell. Tauri wraps the same static web app (../../webapp, unmodified) in each OS's own
// webview — WKWebView on macOS, WebView2 on Windows — matching the original design's intent
// of "no bundled browser engine" without the platform-specific rewrite that implies.
use std::fs::{self, OpenOptions};
use std::io::Write;
use std::path::PathBuf;
use std::sync::Mutex;

use tauri::{Manager, State};

struct LogPath(Mutex<PathBuf>);

fn write_log_line(path: &PathBuf, message: &str) {
    let timestamp = chrono::Utc::now().format("%Y-%m-%dT%H:%M:%SZ");
    let line = format!("[{timestamp}] {message}\n");
    if let Some(parent) = path.parent() {
        let _ = fs::create_dir_all(parent);
    }
    if let Ok(mut file) = OpenOptions::new().create(true).append(true).open(path) {
        let _ = file.write_all(line.as_bytes());
    }
}

// Invoked from index.html's existing window.webkit-style log hooks (extended to also check
// for Tauri's global bridge) — same diagnostic trail the Swift shell wrote, same file name,
// just resolved to the correct per-OS app-data location instead of a hardcoded macOS path.
#[tauri::command]
fn log_message(state: State<LogPath>, message: String) {
    let path = state.0.lock().unwrap();
    write_log_line(&path, &format!("JS: {message}"));
}

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let log_dir = app
                .path()
                .app_log_dir()
                .unwrap_or_else(|_| app.path().app_data_dir().expect("resolve app data dir"));
            let log_path = log_dir.join("sqldojo.log");
            write_log_line(&log_path, "SQL Dojo (Tauri) starting");
            app.manage(LogPath(Mutex::new(log_path)));
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![log_message])
        .run(tauri::generate_context!())
        .expect("error while running SQL Dojo");
}
