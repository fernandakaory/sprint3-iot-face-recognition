# 🧠 HealthBet — Reconhecimento Facial Integrado à API

## 📋 Descrição

Este projeto implementa um **sistema de reconhecimento facial** conectado à **API HealthBet**, permitindo o registro automático de acessos de usuários a partir da detecção facial via webcam.  

O script identifica rostos conhecidos utilizando **MediaPipe**, **OpenCV** e **face_recognition**, consulta um arquivo `data.json` com os dados e imagens dos usuários, e registra automaticamente um novo login na API via requisição `POST`.

Além disso, o sistema oferece um menu interativo no console para:
- Visualizar acessos registrados de um usuário (`GET /usuario/{id}/acessos`)
- Realizar um novo login com reconhecimento facial
- Encerrar o programa

---

## ⚙️ Tecnologias Utilizadas

- **Python 3.11**
- **OpenCV**
- **MediaPipe**
- **face_recognition**
- **Requests**
- **API REST (Java Spring Boot – HealthBet)**

---

## 🧩 Estrutura do Projeto
```
├── reconhecimento_facial.py # Script principal em Python
├── data.json # Arquivo JSON com informações dos usuários
├── imagens/ # Pasta com imagens dos usuários cadastrados
└── README.md # Documentação do projeto
```

---

## 📁 Estrutura do Arquivo `data.json`

O arquivo deve conter uma lista de usuários e o caminho das imagens:

```json
{
  "usuarios": [
    {
      "id": 3,
      "caminho": "foto_perfil1.jpg"
    },
    {
      "id": 8,
      "caminho": "foto_perfil2.jpg"
    },
    {
      "id": 12,
      "caminho": "foto_perfil3.png"
    }
  ]
}

```


---

## 🚀 Execução do Projeto

### 1. Instalar Dependências

#### Dependências

Instale as bibliotecas necessárias com os seguintes comandos:

```bash
pip install opencv-python mediapipe
pip install dlib-bin
pip install face-recognition --no-deps
pip install git+https://github.com/ageitgey/face_recognition_models
```

<p> ⚠️ A biblioteca `face_recognition` depende do `dlib`, que pode ser difícil de compilar. Por isso, foi utilizado o pacote `dlib-bin` para facilitar a instalação.  </p>
<p> ⚠️ O MediaPipe é compatível apenas até a versão Python 3.11. Portanto, recomenda-se a utilização em um ambiente virtual (.venv). </p>

---

### 2. Executar o Script

Após garantir que o arquivo `data.json` está corretamente configurado e a API está rodando localmente, execute:

python reconhecimento_facial.py

O menu aparecerá no terminal:

```
=== MENU ===
1 - Ver acessos de um usuário (GET)
2 - Novo login (reconhecimento facial)
3 - Sair
```
---

## 🧠 Como Funciona o Reconhecimento Facial

1. O sistema carrega os **encodings faciais** de cada usuário presente em `data.json`.
2. A webcam é ativada e o **MediaPipe** detecta rostos e landmarks.
3. O **face_recognition** compara o rosto capturado com os encodings conhecidos.
4. Quando há correspondência:
   - O nome do usuário é exibido na tela.
   - Um **POST** é enviado automaticamente para `http://localhost:8080/acessos`.
   - O login é registrado no banco de dados da API.

Pressione `q` para encerrar a janela da webcam.

---

## 🔗 Endpoints Utilizados

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET    | /usuario/{id}/acessos | Retorna os acessos de um usuário |
| POST   | /acessos               | Registra um novo acesso quando o rosto é reconhecido |

---

## 🤖 Executando o Reconhecimento Facial com a API

Para rodar a integração do **reconhecimento facial** com a API:

1. Certifique-se de que a **API HealthBet** está em execução localmente (rode o arquivo `HealthbetApplication.java` no IntelliJ e verifique se o Swagger está acessível em [http://localhost:8080/swagger-ui/index.html](http://localhost:8080/swagger-ui/index.html)).
2. Execute o script Python responsável pelo reconhecimento facial (`reconhecimento_facial.py`).
3. Quando um rosto for identificado, o nome do usuário será reconhecido automaticamente e enviado para o endpoint `/acessos` da API, registrando o login de forma automática.

---

## 💻 Executando a API Localmente

1. Descompacte o projeto Java HealthBet.
2. Abra o projeto no **IntelliJ IDEA**.
3. Localize o arquivo principal:
 **src/main/java/com/healthbet/HealthbetApplication.java**
4. Clique com o botão direito e selecione **Run 'HealthbetApplication'**.
5. Após iniciar, acesse o Swagger da API em:

http://localhost:8080/swagger-ui/index.html


---

## 👩‍💻 Integrantes

- Anny Carolina Andrade Dias — RM98295  
- Fernanda Kaory Saito — RM551104  
- Henrique Lima — RM551528  
- Pedro Emerici Gava — RM551043  
- Pedro Henrique Menezes — RM97432