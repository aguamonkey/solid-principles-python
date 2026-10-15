# Answer notes

[Prompts](INTERVIEW.md)

Exporters captures named renderers, export_page reads through a pager port, and HTTP selects a name. A test-only renderer uses the unchanged policy. The earlier CLI lab adds separate versioned payload-compatibility reasoning.

Implement a renderer over the supplied immutable tuple and register it at composition. Use JSON encoding for each line so embedded newlines in station text do not corrupt record boundaries. Keep export_page and storage unchanged.

Discuss the actual mechanism and its limits. The backend decisions separate policy guarantees from the extra contracts that public deployment or remote suppliers would require.
