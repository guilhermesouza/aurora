window.onload=function() {
    var editor = CodeMirror.fromTextArea(document.getElementById("id_body"), {
        mode: {name: "python",
               version: 2,
               singleLineStringErrors: false},
        lineNumbers: true,
        indentUnit: 4,
        tabMode: "shift",
        matchBrackets: true
    });
}