import cv2


def record_video(out_dir: str, show_frame=True) -> None:
    """Record a video. Presee 'q' to stop."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise Exception("Unable to read camera feed")

    width, height = int(cap.get(3)), int(cap.get(4))
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    out = cv2.VideoWriter(out_dir, fourcc, 10, (width, height))

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        out.write(frame)

        if show_frame:
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()

    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    record_video("pens.avi")
