# 🧠 Reconhecimento Facial com MediaPipe e face_recognition

Este projeto realiza **reconhecimento facial em tempo real** utilizando a webcam, combinando as bibliotecas **MediaPipe** (para detecção facial e landmarks) e **face_recognition** (para identificação de rostos conhecidos). Ele também permite o ajuste dinâmico de parâmetros via interface com sliders (trackbars).

---

## 🎯 Objetivo

O objetivo deste projeto é detectar rostos em tempo real e identificar se o rosto capturado pela webcam corresponde a uma imagem previamente conhecida (neste caso, `foto_fernanda.jpg`). Além disso, o sistema exibe landmarks faciais (olhos, nariz, boca) e permite o ajuste de parâmetros como confiança, modelo de detecção, tolerância de reconhecimento e redimensionamento do frame.

---

## ▶️ Como Executar

1. **Clone o repositório** ou copie os arquivos para seu ambiente local.
2. Certifique-se de ter uma imagem chamada `foto_fernanda.jpg` no mesmo diretório do script.
3. Execute o script Python:

```bash
python nome_do_arquivo.py
```

4. Uma janela chamada **"Controles"** será aberta com sliders para ajustar os parâmetros em tempo real.
5. A janela **"Reconhecimento Facial + Landmarks"** exibirá o vídeo da webcam com as detecções.
6. Pressione **`q`** para encerrar a execução.

---

## 💻 Ambiente de Desenvolvimento

- **Python**: 3.10 (recomendado)
- **IDE recomendada**: [PyCharm](httpsta a organização e execução do projeto)
- **Sprint**: Projeto desenvolvido na Sprint de IoT

---

## 📦 Dependências

Instale as bibliotecas necessárias com os seguintes comandos:

```bash
pip install opencv-python mediapipe
pip install dlib-bin
pip install face-recognition --no-deps
pip install git+https://github.com/ageitgey/face_recognition_models
```

> ⚠️ A biblioteca `face_recognition` depende do `dlib`, que pode ser difícil de compilar. Por isso, foi utilizado o pacote `dlib-bin` para facilitar a instalação.

---

## 🎛️ Parâmetros Ajustáveis

Durante a execução, você pode ajustar os seguintes parâmetros na janela **"Controles"**:

| Parâmetro     | Descrição                                                                 |
|---------------|---------------------------------------------------------------------------|
| **Confianca**     | Nível de confiança para detecção facial (MediaPipe).                     |
| **Modelo**        | Modelo de detecção: `0` para curto alcance, `1` para longo alcance.      |
| **Tolerancia**    | Tolerância para comparação de rostos (face_recognition).                 |
| **Resize**        | Fator de redimensionamento do frame da webcam (para melhorar desempenho).|

---

## 🧠 Organização do Código

O código está dividido em seções bem definidas:

1. **Configurações iniciais**: parâmetros padrão.
2. **Carregamento do rosto conhecido**.
3. **Inicialização do MediaPipe**.
4. **Criação da interface de controle (trackbars)**.
5. **Captura de vídeo e loop principal**:
   - Leitura dos sliders.
   - Redimensionamento e conversão de cor.
   - Detecção facial com MediaPipe.
   - Reconhecimento facial com face_recognition.
   - Desenho de landmarks e identificação.
6. **Finalização**: liberação da webcam e fechamento das janelas.

---

## ⚖️ Nota Ética sobre Uso de Dados Faciais

Este projeto utiliza **dados faciais sensíveis** e, portanto, deve ser usado com responsabilidade. Algumas considerações importantes:

- A imagem usada para reconhecimento (`foto_fernanda.jpg`) deve ser de **uso pessoal e autorizado**.
- Evite utilizar imagens de terceiros sem consentimento explícito.
- Este projeto é **educacional** e não deve ser utilizado para fins de vigilância, discriminação ou qualquer uso que viole a privacidade e os direitos individuais.
- Sempre informe os usuários quando estiver capturando ou processando imagens faciais.
- O uso ético da tecnologia é essencial para garantir a confiança e o respeito à privacidade.

---

## 📌 Observações Finais

- O desempenho pode variar dependendo da iluminação, qualidade da webcam e posicionamento do rosto.
- Ajuste os parâmetros para obter melhores resultados em diferentes ambientes.
- Certifique-se de que a imagem de referência (`foto_fernanda.jpg`) esteja bem iluminada e com o rosto visível.
- O projeto pode ser expandido para múltiplos rostos conhecidos, salvamento de logs, ou integração com bancos de dados.
- Testado com Python 3.10 e bibliotecas compatíveis com essa versão.

---

## 👩‍💻 Autora

**Fernanda Kaory Saito**  
Projeto desenvolvido para fins acadêmicos na Sprint de IoT.

---
