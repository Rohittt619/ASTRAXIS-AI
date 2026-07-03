# Multi-Agent Threat Modeling Framework

ASTRAXIS-AI adopts a graph-centric threat modeling methodology:

```
[Untrusted Entry Node] ---> [Agent Node] ---> [Tool Execution] ---> [Sensitive Data Target]
```

By computing graph shortest paths and degree centralities, the system identifies key bottleneck agents that require defensive hardening.
