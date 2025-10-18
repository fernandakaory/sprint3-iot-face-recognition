import cv2
import mediapipe as mp
import face_recognition
import requests
from datetime import datetime
import sys
import time
import json

# -----------------------------
# CONFIGURAÇÕES INICIAIS
# -----------------------------
MIN_DETECTION_CONFIDENCE_DEFAULT = 0.5
MODEL_SELECTION_DEFAULT = 0
FACE_MATCH_TOLERANCE_DEFAULT = 0.4
FRAME_RESIZE_DEFAULT = 0.75

API_BASE_URL = "http://localhost:8080"  # base da API
JSON_PATH = "data.json"  # caminho do arquivo JSON externo

# -----------------------------
# CARREGA JSON DE USUÁRIOS E ENCODINGS
# -----------------------------
try:
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        usuarios_data = json.load(f)

    usuarios = []
    for u in usuarios_data["usuarios"]:
        try:
            image = face_recognition.load_image_file(u["caminho"])
            encoding = face_recognition.face_encodings(image)[0]
            usuarios.append({
                "id": u["id"],
                "caminho": u["caminho"],
                "nome_usuario": u.get("nome_usuario", f"Usuario {u['id']}"),
                "encoding": encoding
            })
        except Exception as e:
            print(f"Erro ao processar imagem {u['caminho']} (id {u['id']}): {e}")
except FileNotFoundError:
    print(f"Arquivo JSON não encontrado: {JSON_PATH}")
    sys.exit(1)
except Exception as e:
    print(f"Erro ao carregar dados do JSON: {e}")
    sys.exit(1)

if not usuarios:
    print("Nenhum usuário válido encontrado no JSON. Encerrando.")
    sys.exit(1)

# -----------------------------
# INICIALIZAÇÃO MEDIAPIPE
# -----------------------------
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# -----------------------------
# FUNÇÕES
# -----------------------------
def show_menu():
    print("\n=== MENU ===")
    print("1 - Ver acessos de um usuário (GET)")
    print("2 - Novo login (reconhecimento facial)")
    print("3 - Sair")
    return input("Escolha uma opção: ").strip()

def ver_logins():
    try:
        usuario_id = input("Digite o ID do usuário para consultar acessos: ").strip()
        if not usuario_id.isdigit():
            print("ID inválido.")
            return
        usuario_id = int(usuario_id)
        r = requests.get(f"{API_BASE_URL}/usuario/{usuario_id}/acessos", timeout=5)
        if r.status_code == 200:
            try:
                data = r.json()
            except ValueError:
                print("Resposta da API não é JSON válido.")
                return
            if not data:
                print("Nenhum acesso registrado para este usuário.")
                return
            print(f"\n--- Acessos do usuário {usuario_id} ---")
            for item in data:
                print(item)
        else:
            print(f"Erro ao consultar API: status {r.status_code}")
    except requests.RequestException as e:
        print(f"Erro de conexão com a API: {e}")

def novo_login_automatico():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: não foi possível acessar a webcam.")
        return False

    face_detected = False

    with mp_face_detection.FaceDetection(
        min_detection_confidence=MIN_DETECTION_CONFIDENCE_DEFAULT,
        model_selection=MODEL_SELECTION_DEFAULT
    ) as face_detection, mp_face_mesh.FaceMesh(
        max_num_faces=2,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        print("Aguardando reconhecimento facial... (pressione 'q' para sair)")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Falha ao capturar frame da webcam.")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results_detection = face_detection.process(rgb_frame)
            results_mesh = face_mesh.process(rgb_frame)

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matched = False
                matched_id = None
                matched_nome = None
                for u in usuarios:
                    if face_recognition.compare_faces([u["encoding"]], face_encoding, tolerance=FACE_MATCH_TOLERANCE_DEFAULT)[0]:
                        matched = True
                        matched_id = u["id"]
                        matched_nome = u["nome_usuario"]
                        break

                label = f"{matched_nome or 'Desconhecido'} (ID {matched_id})" if matched else "Desconhecido"
                color = (0, 255, 0) if matched else (0, 0, 255)

                # Desenha retângulo e label
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                # Envia POST apenas uma vez
                if matched and not face_detected:
                    face_detected = True
                    payload = {"idUsuario": matched_id, "nome_usuario": matched_nome}
                    print(f"\nRosto reconhecido! Enviando registro do ID {matched_id}, nome {matched_nome}...")
                    try:
                        r = requests.post(f"{API_BASE_URL}/acessos", json=payload, timeout=5)
                        if r.status_code in (200, 201):
                            print("Login registrado com sucesso!")
                        else:
                            print(f"Erro ao registrar login: status {r.status_code}. Conteúdo: {r.text}")
                    except requests.RequestException as e:
                        print(f"Erro ao conectar com API: {e}")

            # Desenha landmarks simples do FaceMesh
            if results_mesh.multi_face_landmarks:
                for face_landmarks in results_mesh.multi_face_landmarks:
                    for lm in face_landmarks.landmark:
                        h, w, _ = frame.shape
                        x, y = int(lm.x * w), int(lm.y * h)
                        cv2.circle(frame, (x, y), 1, (255, 0, 0), -1)

            # Desenha detections do MediaPipe
            if results_detection.detections:
                for detection in results_detection.detections:
                    mp_drawing.draw_detection(frame, detection)

            cv2.imshow("Reconhecimento Facial", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Encerrando webcam...")
                break

        cap.release()
        cv2.destroyAllWindows()
        return True

# -----------------------------
# LOOP PRINCIPAL
# -----------------------------
def main():
    while True:
        opcao = show_menu()
        if opcao == "1":
            ver_logins()
        elif opcao == "2":
            novo_login_automatico()
        elif opcao == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
