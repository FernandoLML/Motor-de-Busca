# Motor de Busca de Documentos 🔍
 
Projeto prático desenvolvido para a disciplina de **Algoritmos Avançados**, focado na implementação de algoritmos de *Substring Search* e instrumentação de telemetria.
 
## 👥 Equipe
* Bruno Franzosi
* Fernando Lucas Moraes da Luz
 
## 🚀 Sobre o Projeto
A aplicação permite o upload de documentos e a realização de buscas textuais utilizando diferentes estratégias algorítmicas, permitindo a comparação de desempenho em tempo real através de um dashboard de observabilidade.
 
### Algoritmos Implementados (Strategy Pattern)
- [ ] **Naive (Força Bruta):** O(N·M)).
- [ ] **Rabin-Karp:** Baseado em hashing rolante.
- [ ] **KMP (Knuth-Morris-Pratt):** Utiliza tabela de falhas.
- [ ] **Boyer-Moore:** Eficiente para textos naturais.
 
### 🛠️ Tecnologias Utilizadas
- **Linguagem:** [Ex: Java / Python / Node.js]
- **Interface:** [Ex: React / HTML & JS]
- **Observabilidade:** OpenTelemetry, Prometheus, Grafana e Tempo.
- **Infraestrutura:** Docker & Docker Compose.
 
## 📊 Observabilidade e Métricas
A aplicação registra automaticamente:
- **Traces:** Fluxo completo desde o upload até o resultado.
- **Metrics:** Tempo de execução (`search_duration_ms`) e total de buscas.
- **Logs:** Detalhes técnicos de cada busca (N, M e ocorrências).
 
## 🔧 Como Executar
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/FernandoLML/Motor-de-Busca.git
