import cv2
from DataManager import DataManager


class QrCodeScanner:
    def __init__(self, camera_id=0):
        """
        Initialize the QrCodeScanner object.

        Args:
            camera_id (int): ID of the camera to use (default is 0).
        """
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(self.camera_id)
        self.db_manager = DataManager()
    
    def __del__(self):
        """
        Destructor to release the camera when the object is deleted.
        """
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
    
    def scan_realtime_qr_code(self, check_in=True):
        """
        Scan for QR codes in real-time using the camera.

        Returns:
            str or None: QR code data if found, otherwise None.
        """
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Error: couldn't read from webcam")
                break

            qr_code_data = self.decode_qr_code(frame)
            cv2.imshow("QR code Scanner", frame)
            if qr_code_data:
                print("QR Data : ", qr_code_data)

                if check_in:
                    self.db_manager.update_ticket_status(qr_code_data[1:len(qr_code_data)-1],"check_in")
                    print('Check-in complete')
                    # return ('check_in complete')
                else:
                    self.db_manager.update_ticket_status(qr_code_data[1:len(qr_code_data)-1],"check_out")
                    print('Check-out complete')
                    # return ('check_out complete')
                cv2.waitKey(4000)
                # return qr_code_data[1:len(qr_code_data)-1]
            # self.display_qr_result(qr_code_data, frame)
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if not (cv2.getWindowProperty("QR code Scanner", cv2.WND_PROP_VISIBLE)):
                break

        self.cap.release()
        cv2.destroyAllWindows()
        return None
    
    def decode_qr_code(self, frame):
        """
        Decode QR code from the given frame.

        Args:
            frame (numpy.ndarray): Input frame (image) containing the QR code.

        Returns:
            str or None: Decoded QR code data if found, otherwise None.
        """
        detector = cv2.QRCodeDetector()
        value, _, qr_code_data = detector.detectAndDecode(frame)

        if value:
            return value
        return None
    
    def display_qr_result(self, qr_code_data):

            # check if scanned qr code is in the tickets array
            ticket_data = self.db_manager.get_tbl_item_list('Tickets',['ticket_id'])
            # print(ticket_data)

            for ticket in ticket_data:
                # ticket['id'] = f"\"{ticket['id']}\""
                if ticket['ticket_id'] == qr_code_data and ticket['status'] == 'N':
                    # this status should update my Tickets array data of provided ticket_id
                    print("aaja iske andar")
                    DataManager.update_item("Tickets",qr_code_data, "status","S")
                    print("Welcome! your journey has started")
                    # Display green signal for valid ticket
                    # self.display_signal(frame, color=(0,255,0))
                    # cv2.waitKey(3000)
                    break
                else:
                    print("Invalid or already used QR code.")
                    # self.display_signal(frame, color=(255,0,0))
                    # cv2.waitKey(3000)
    
    def display_signal(self, frame, color):
        h, w, _ = frame.shape
        signal_size = 50
        margin = 10
        cv2.rectangle(frame, (margin, margin), (margin + signal_size, margin + signal_size), color, -1)