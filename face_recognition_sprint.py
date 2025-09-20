import cv2
import mediapipe as mp
import face_recognition

# ==========================
# CONFIGURAÇÕES INICIAIS
# ==========================
MIN_DETECTION_CONFIDENCE_DEFAULT = 0.5
MODEL_SELECTION_DEFAULT = 0
FACE_MATCH_TOLERANCE_DEFAULT = 0.6
FRAME_RESIZE_DEFAULT = 0.75

# ==========================
# 1. Carregar rosto conhecido
# ==========================
known_image = face_recognition.load_image_file("foto_perfil2.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# ==========================
# 2. Inicializar MediaPipe Face Detection
# ==========================
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

face_detection = mp_face_detection.FaceDetection(
    min_detection_confidence=MIN_DETECTION_CONFIDENCE_DEFAULT,
    model_selection=MODEL_SELECTION_DEFAULT,
)

# ==========================
# 3. Função dummy para trackbars
# ==========================
def nothing(x):
    pass

# ==========================
# 4. Criar janela de controle
# ==========================
cv2.namedWindow("Controles")
cv2.createTrackbar("Confianca", "Controles", int(MIN_DETECTION_CONFIDENCE_DEFAULT*100), 100, nothing)
cv2.createTrackbar("Modelo", "Controles", MODEL_SELECTION_DEFAULT, 1, nothing)
cv2.createTrackbar("Tolerancia", "Controles", int(FACE_MATCH_TOLERANCE_DEFAULT*100), 100, nothing)
cv2.createTrackbar("Resize", "Controles", int(FRAME_RESIZE_DEFAULT*100), 200, nothing)

# ==========================
# 5. Captura de vídeo
# ==========================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro: Não foi possível acessar a webcam.")
    exit()

print("Pressione 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ==========================
    # Leitura dos sliders
    # ==========================
    conf_slider = cv2.getTrackbarPos("Confianca", "Controles") / 100
    model_slider = cv2.getTrackbarPos("Modelo", "Controles")
    tolerance_slider = cv2.getTrackbarPos("Tolerancia", "Controles") / 100
    resize_slider = cv2.getTrackbarPos("Resize", "Controles") / 100

    # Redimensiona o frame conforme slider
    frame = cv2.resize(frame, None, fx=resize_slider, fy=resize_slider)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ==========================
    # Atualiza MediaPipe Face Detection com sliders
    # ==========================
    face_detection = mp_face_detection.FaceDetection(
        min_detection_confidence=conf_slider,
        model_selection=model_slider
    )

    # ==========================
    # Detecta rostos com MediaPipe
    # ==========================
    results = face_detection.process(rgb_frame)

    # ==========================
    # Detecta rostos e encodings para face_recognition
    # ==========================
    face_locations = face_recognition.face_locations(rgb_frame)  # detecta rostos
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=tolerance_slider)
        name = "Usuario" if matches[0] else "Desconhecido"

        # Desenha retângulo + nome
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # ==========================
    # Desenha landmarks básicos (olhos, nariz, boca) do MediaPipe
    # ==========================
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(frame, detection)

            ih, iw, _ = frame.shape
            keypoints = detection.location_data.relative_keypoints
            for kp in keypoints:
                x, y = int(kp.x * iw), int(kp.y * ih)
                cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)  # pontos vermelhos

    # ==========================
    # Exibe frame
    # ==========================
    cv2.imshow("Reconhecimento Facial + Landmarks", frame)

    # Tecla para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
