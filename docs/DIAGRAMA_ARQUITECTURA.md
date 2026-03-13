# Diagrama de Arquitectura (Mermaid)

Esta sección proporciona una visualización de alto nivel de cómo se despliega y conecta el sistema.

```mermaid
flowchart LR
    subgraph Usuario
        A[Usuario (Navegador)]
    end

    subgraph Frontend
        A --> B[Render (Web Service)]
        B --> C[Flask App (app.py)]
        C --> D[Templates Jinja2 + Static (CSS/JS)]
    end

    subgraph Base de Datos
        C --> E[Aiven MySQL]
    end

    subgraph Integraciones
        B --> F[GitHub (Repositorio)]
        %% (Opcional) Analítica / monitoreo
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#bfb,stroke:#333,stroke-width:2px
    style D fill:#ffb,stroke:#333,stroke-width:2px
    style E fill:#fbb,stroke:#333,stroke-width:2px
    style F fill:#ccc,stroke:#333,stroke-width:2px
    style G fill:#fcf,stroke:#333,stroke-width:2px
```

> 💡 Para renderizar este diagrama, usa un viewer de Markdown que soporte Mermaid (GitHub, VS Code con extensión, etc.).
