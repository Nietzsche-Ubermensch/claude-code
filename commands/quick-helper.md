name: quick-helper
version: 1.0.0
description: Quick code helper commands

commands:
  - name: /quick-review
    description: Fast code review
    prompt: |
      Quick code review of the provided files.
      Check for: bugs, performance issues, best practices.
      Keep it under 200 words.
      Files: {files}
  
  - name: /quick-test
    description: Generate tests quickly
    prompt: |
      Generate unit tests for the provided code.
      Use the appropriate testing framework.
      Cover main functionality and edge cases.
      Files: {files}
  
  - name: /quick-fix
    description: Quick bug fix
    prompt: |
      Analyze this error and suggest a fix.
      Error: {error}
      File: {file}
      Provide: root cause + solution + code

examples:
  - usage: "/quick-review @auth.js"
  - usage: "/quick-test @utils.py"
  - usage: "/quick-fix 'TypeError' @app.js"
