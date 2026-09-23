import Foundation
import WebKit

/// Serves the bundled sql-dojo/ web app to WKWebView over a custom
/// `sqldojo://` scheme instead of `file://` or a loopback HTTP server.
///
/// `file://` doesn't work here: WebKit's fetch()/Worker implementation does
/// not support loading resources (module scripts, wasm binaries) from
/// file:// origins at all — a hard WebKit limitation, not something fixable
/// by granting read access. A loopback NWListener-based HTTP server was
/// tried instead, but that adds an async startup race (binding a real socket
/// before the first load) for no benefit over a scheme handler, which Apple
/// documents as exactly this local-content extension point (it's how
/// frameworks like Capacitor/Ionic serve offline web content that needs
/// fetch()/Worker support). A custom scheme is fully fetchable like http(s),
/// has no listening socket (zero network surface, not merely a restricted
/// one), and is served synchronously per-resource by WebKit — no separate
/// "start a server and wait" step to get wrong.
final class LocalSchemeHandler: NSObject, WKURLSchemeHandler {
    static let scheme = "sqldojo"

    private let rootDirectory: URL
    private let chunkSize = 64 * 1024

    init(rootDirectory: URL) {
        self.rootDirectory = rootDirectory
    }

    func webView(_ webView: WKWebView, start urlSchemeTask: WKURLSchemeTask) {
        guard let url = urlSchemeTask.request.url else {
            urlSchemeTask.didFailWithError(URLError(.badURL))
            return
        }

        DiagnosticLogger.log("LocalSchemeHandler: request for \(url.absoluteString)")

        var relativePath = url.path
        while relativePath.hasPrefix("/") { relativePath.removeFirst() }
        if relativePath.isEmpty { relativePath = "index.html" }

        let fileURL = rootDirectory.appendingPathComponent(relativePath)
        let standardizedFile = fileURL.standardizedFileURL.path
        let standardizedRoot = rootDirectory.standardizedFileURL.path

        guard standardizedFile.hasPrefix(standardizedRoot),
              let fileHandle = FileHandle(forReadingAtPath: standardizedFile) else {
            DiagnosticLogger.log("LocalSchemeHandler: 404 for \(relativePath)")
            urlSchemeTask.didFailWithError(URLError(.fileDoesNotExist))
            return
        }
        defer { try? fileHandle.close() }

        let fileSize = (try? FileManager.default.attributesOfItem(atPath: standardizedFile)[.size] as? Int) ?? nil
        let mime = mimeType(forPathExtension: fileURL.pathExtension)
        var headers = ["Content-Type": mime]
        if let fileSize {
            headers["Content-Length"] = String(fileSize)
        }
        // fetch()'s Response.ok/status semantics need a real HTTP-shaped
        // response, not a bare URLResponse — WebAssembly.instantiateStreaming
        // (called from inside the DuckDB worker) silently never resolves
        // against a non-HTTP response even though the bytes transfer fine.
        let response = HTTPURLResponse(
            url: url,
            statusCode: 200,
            httpVersion: "HTTP/1.1",
            headerFields: headers
        )!
        urlSchemeTask.didReceive(response)

        var totalSent = 0
        var chunkCount = 0
        while true {
            let data = fileHandle.readData(ofLength: chunkSize)
            if data.isEmpty { break }
            urlSchemeTask.didReceive(data)
            totalSent += data.count
            chunkCount += 1
        }
        urlSchemeTask.didFinish()

        DiagnosticLogger.log(
            "LocalSchemeHandler: served \(fileURL.lastPathComponent) (\(totalSent) bytes\(chunkCount > 1 ? ", chunked" : ""))"
        )
    }

    func webView(_ webView: WKWebView, stop urlSchemeTask: WKURLSchemeTask) {
        // Reads are synchronous and already complete by the time this could
        // be called; nothing to cancel.
    }

    private func mimeType(forPathExtension pathExtension: String) -> String {
        switch pathExtension {
        case "html": return "text/html"
        case "js", "mjs": return "text/javascript"
        case "wasm": return "application/wasm"
        case "json": return "application/json"
        case "css": return "text/css"
        default: return "application/octet-stream"
        }
    }
}
