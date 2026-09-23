import Foundation

/// Appends timestamped lines to a plain text log file so failures are
/// inspectable afterward with a plain file read — no Console.app permissions
/// needed, and nothing relies on the app's own (possibly broken) UI to report
/// what went wrong.
enum DiagnosticLogger {
    private static let formatter: ISO8601DateFormatter = ISO8601DateFormatter()

    private static let logURL: URL = {
        let supportDir = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("SQL Dojo", isDirectory: true)
        try? FileManager.default.createDirectory(at: supportDir, withIntermediateDirectories: true)
        return supportDir.appendingPathComponent("sqldojo.log")
    }()

    private static let queue = DispatchQueue(label: "com.mauriceallen.sqldojo.diagnosticlogger")

    static func log(_ message: String) {
        let line = "[\(formatter.string(from: Date()))] \(message)\n"
        queue.async {
            guard let data = line.data(using: .utf8) else { return }
            if let handle = try? FileHandle(forWritingTo: logURL) {
                defer { try? handle.close() }
                handle.seekToEndOfFile()
                handle.write(data)
            } else {
                try? data.write(to: logURL)
            }
        }
    }
}
