import time
import cv2
import qrcode
import json

def generate_qr_code(data, filename):
    # convert Json data to string
    json_data_str = json.dumps(data)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(json_data_str)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')
    img.save(filename)
    img.close()

# def scan_qr_code(image_path):
#     image = cv2.imread(image_path)
#     print("image readed")
#     qr_code_data = None

#     detector = cv2.QRCodeDetector()
#     value, pts, qr_code_data = detector.detectAndDecode(image)

#     if qr_code_data:
#         print("QR DATA:", qr_code_data)
#     else:
#         print("No QR Code found")

def scan_realtime_qr_code():
    cap = cv2.VideoCapture(0)
    qr_code_data=None
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: couldn't read form webcam.")
            break

        qr_code_data = decode_qr_code(frame)
        
        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if qr_code_data:
            print("QR DATA:", qr_code_data)
            # time.sleep(wait_time)
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return qr_code_data


def decode_qr_code(frame):
    detector = cv2.QRCodeDetector()
    value,pts,qr_code_data=detector.detectAndDecode(frame)

    if value:
        return value
    return None

if __name__ == '__main__':

    while True:
        print("1.Generate QR\n2.Read QR\n3.Exit")
        choose = int(input("Enter a number : "))
        
        if choose == 1:
            name = input("Your Name : ")
            age = input("Your Age : ")
            contact = input("contact no. : ")
            address = input("Address : ")

            json_data = {
                "name":name,
                'age':age,
                'contact':contact,
                'address':address
            }

            qr_code_filename = 'generated_qr_json.png'
            generate_qr_code(json_data, qr_code_filename)
            print("QR code generated successfully")
            continue
        elif choose == 2:
            print("opening scanner...")
            scanned_data = scan_realtime_qr_code()
            if scanned_data:
                print("Scanned data outside the function: ", scanned_data)
                continue
        elif choose==3:
            print("exiting programm")
            break
        else:
            print("Invalid choice. please Re-enter")
            continue
        