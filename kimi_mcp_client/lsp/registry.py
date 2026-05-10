EXTENSION_TO_SERVER = {
    ".rs": ["rust-analyzer"],
    ".py": ["pyright-langserver", "--stdio"],
    ".go": ["gopls", "serve"],
    ".ts": ["typescript-language-server", "--stdio"],
    ".js": ["typescript-language-server", "--stdio"],
    ".c": ["clangd"],
    ".cpp": ["clangd"],
}
