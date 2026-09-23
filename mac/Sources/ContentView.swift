import SwiftUI
import WebKit

struct ContentView: View {
    var body: some View {
        SQLDojoWebView()
            .frame(minWidth: 1024, minHeight: 720)
    }
}

private struct SQLDojoWebView: NSViewRepresentable {
    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    func makeNSView(context: Context) -> WKWebView {
        let configuration = WKWebViewConfiguration()
        let resourceRoot = Bundle.main.resourceURL!.appendingPathComponent("sql-dojo")
        configuration.setURLSchemeHandler(
            LocalSchemeHandler(rootDirectory: resourceRoot),
            forURLScheme: LocalSchemeHandler.scheme
        )
        configuration.userContentController.add(context.coordinator, name: "log")

        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.navigationDelegate = context.coordinator

        let appURL = URL(string: "\(LocalSchemeHandler.scheme)://app/index.html")!
        DiagnosticLogger.log("Loading \(appURL.absoluteString)")
        webView.load(URLRequest(url: appURL))
        return webView
    }

    func updateNSView(_ nsView: WKWebView, context: Context) {}

    final class Coordinator: NSObject, WKNavigationDelegate, WKScriptMessageHandler {
        func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            DiagnosticLogger.log("Navigation finished successfully")
        }

        func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
            DiagnosticLogger.log("Navigation failed: \(error.localizedDescription)")
        }

        func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
            DiagnosticLogger.log("Provisional navigation failed: \(error.localizedDescription)")
        }

        func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
            DiagnosticLogger.log("JS: \(message.body)")
        }
    }
}
