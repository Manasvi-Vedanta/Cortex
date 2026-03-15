# Hybrid-GenMentor System Pipeline with Processing Times

```mermaid
flowchart TD
    A["🎯 User Input\n(Career Goal + Existing Skills)"] -->|"~0.01s"| B["🔍 Goal Expansion\n& Embedding Generation"]
    
    B -->|"~0.02s"| C["📊 FAISS Occupation Matching\n(768-dim Sentence Transformer)"]
    
    C -->|"~0.5s"| D["🗄️ ESCO Database Query\n(SQLite: Skills + Relations)"]
    
    D -->|"~3.5s"| E["🤖 LLM Skill Prioritization\n(GPT-5.2 / Gemini)\ntemperature=0.2"]
    
    E -->|"~0.3s"| F["📉 Skill Gap Calculation\n(Existing vs Required)"]
    
    F -->|"~0.1s"| G["🔗 Dependency Graph\n(NetworkX DAG +\nTopological Sort)"]
    
    G -->|"~15s"| H["🤖 LLM Session Organization\n(GPT-5.2 / Gemini)\ntemperature=0.2\nmax_tokens=2048"]
    
    H -->|"~0.5s"| I["📚 Resource Enrichment\n& Guide Generation"]
    
    I -->|"~4s"| J["⚡ Difficulty Scoring\n& Duration Estimation"]
    
    J --> K["✅ Complete Learning Path\nAvg: 24.12s total"]

    K -->|"~23.82s"| L["📝 Quiz Generation\n(GPT-5.2 / Gemini)\ntemperature=0.3\nmax_tokens=3000"]
    
    L --> M["🎓 Final Output\n(Path + Quiz)\nTotal: ~91.53s"]

    subgraph EMBEDDING ["Embedding Layer (Local)"]
        direction LR
        B
        C
    end

    subgraph ESCO ["ESCO Knowledge Base"]
        direction LR
        D
    end

    subgraph LLM_CALLS ["LLM API Calls (~42s / 77% of path time)"]
        direction LR
        E
        H
    end

    subgraph PATH_GEN ["Path Generation Pipeline (24.12s avg)"]
        direction TB
        EMBEDDING
        ESCO
        LLM_CALLS
        F
        G
        I
        J
    end

    style A fill:#4CAF50,color:#fff,stroke:#388E3C
    style K fill:#2196F3,color:#fff,stroke:#1565C0
    style M fill:#FF9800,color:#fff,stroke:#E65100
    style LLM_CALLS fill:#FFF3E0,stroke:#FF9800,stroke-width:2px
    style PATH_GEN fill:#E3F2FD,stroke:#2196F3,stroke-width:2px
    style EMBEDDING fill:#E8F5E9,stroke:#4CAF50
    style ESCO fill:#F3E5F5,stroke:#9C27B0
```

## Pipeline Stage Breakdown

| Stage | Component | Time | % of Path |
|-------|-----------|------|-----------|
| 1 | Goal Expansion & Embedding | ~0.01s | <1% |
| 2 | FAISS Occupation Matching | ~0.02s | <1% |
| 3 | ESCO Database Query | ~0.5s | 2% |
| 4 | **LLM Skill Prioritization** | **~3.5s** | **15%** |
| 5 | Skill Gap Calculation | ~0.3s | 1% |
| 6 | Dependency Graph (NetworkX) | ~0.1s | <1% |
| 7 | **LLM Session Organization** | **~15s** | **62%** |
| 8 | Resource Enrichment | ~0.5s | 2% |
| 9 | Difficulty Scoring | ~4s | 17% |
| **Total Path Generation** | | **24.12s** | **100%** |
| **Quiz Generation** | | **23.82s** | — |
| **Other (overhead)** | | **43.59s** | — |
| **Total per test case** | | **91.53s** | — |
