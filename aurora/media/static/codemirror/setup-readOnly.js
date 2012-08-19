var editor = CodeMirror.fromTextArea(document.getElementById("task-body"), {
    mode: {name: "python",
           version: 2,
           singleLineStringErrors: false},
    lineNumbers: true,
    indentUnit: 4,
    tabMode: "shift",
    matchBrackets: true,
    readOnly: true
});