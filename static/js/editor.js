// Monaco Editor utilities for StudySprint

class CodeEditor {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.editor = null;
        this.options = {
            language: 'python',
            theme: 'vs-dark',
            fontSize: 14,
            automaticLayout: true,
            minimap: { enabled: false },
            wordWrap: 'on',
            scrollBeyondLastLine: false,
            ...options
        };
    }
    
    async init() {
        return new Promise((resolve, reject) => {
            if (!window.require) {
                reject(new Error('Monaco loader not available'));
                return;
            }
            
            require.config({ 
                paths: { 'vs': 'https://unpkg.com/monaco-editor@0.44.0/min/vs' }
            });
            
            require(['vs/editor/editor.main'], () => {
                try {
                    this.editor = monaco.editor.create(
                        document.getElementById(this.containerId), 
                        this.options
                    );
                    resolve(this.editor);
                } catch (error) {
                    reject(error);
                }
            });
        });
    }
    
    getValue() {
        return this.editor ? this.editor.getValue() : '';
    }
    
    setValue(value) {
        if (this.editor) {
            this.editor.setValue(value);
        }
    }
    
    insertText(text) {
        if (this.editor) {
            const position = this.editor.getPosition();
            const range = new monaco.Range(
                position.lineNumber,
                position.column,
                position.lineNumber,
                position.column
            );
            this.editor.executeEdits('', [{ range, text }]);
        }
    }
    
    focus() {
        if (this.editor) {
            this.editor.focus();
        }
    }
    
    resize() {
        if (this.editor) {
            this.editor.layout();
        }
    }
    
    setTheme(theme) {
        if (this.editor) {
            monaco.editor.setTheme(theme);
        }
    }
    
    setLanguage(language) {
        if (this.editor) {
            monaco.editor.setModelLanguage(this.editor.getModel(), language);
        }
    }
}

// Utility functions for code execution
class CodeRunner {
    constructor(submitUrl) {
        this.submitUrl = submitUrl;
    }
    
    async runCode(code) {
        const response = await fetch(this.submitUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    }
}

// Common starter code templates
const STARTER_TEMPLATES = {
    python: {
        twoSum: `def solution(nums, target):
    """
    Given an array of integers and a target, return indices of two numbers that add up to target.
    """
    # Your code here
    pass`,
        
        reverseString: `def solution(s):
    """
    Reverse a string.
    """
    # Your code here
    pass`,
        
        fibonacci: `def solution(n):
    """
    Return the nth Fibonacci number.
    """
    # Your code here
    pass`,
        
        palindrome: `def solution(s):
    """
    Check if a string is a palindrome.
    """
    # Your code here
    pass`
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CodeEditor, CodeRunner, STARTER_TEMPLATES };
} 