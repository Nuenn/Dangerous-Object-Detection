import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import cv2
from ultralytics import YOLO
import json
import threading
import asyncio
import time

APiToken = "6722307793:AAFcJtvp_IhfVBVa8OOo_QY-g0PC_LQ0H_E"

obd_stop_flag = False # Object Detection stop flag
# Lock to synchronize access to the stop_flag
lock = threading.Lock()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    # Create a Thread object and pass the function to it
    global obd_stop_flag
    global thread 
    obd_stop_flag = False
    thread = threading.Thread(target=objectDetection, args=(update, context))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Start Object Detection")
    # Start the thread
    thread.start()

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global obd_stop_flag
    global thread 
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Object Detection Stop!")
    # Set the flag to stop the thread
    with lock:  # Acquire the lock
        obd_stop_flag = True

    # Wait for the thread to finish
    thread.join()

async def sendImage(update: Update, context: ContextTypes.DEFAULT_TYPE, image_bytes, verbose):
    try:
        # await context.bot.send_message(chat_id=update.effective_chat.id, text="Detecting Dangerous Object: \n"+verbose)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_bytes,  caption="Detecting Dangerous Object: \n"+verbose)  
    except Exception as e:
        print("\n An error occured when send image:", e)
    
    print("\nimage send")

def run_send_image(update, context, image_bytes, verbose):
    asyncio.run(sendImage(update, context, image_bytes, verbose))

def objectDetection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Starting Object Detection\n")
    start_time = time.time()
    current_time = 0
    interval = 30 # set minute of interval
    # Load the YOLOv8 model
    model = YOLO('yolov8n.pt')

    # Open the video file
    cap = cv2.VideoCapture(1)

    # Check for the blacklisted object
    def check_for_blacklisted_object(json_string):
        parsed_data = json.loads(json_string)
        blacklisted = ["knife", "person"]
        blacklisted_exists = any(item['name'] in blacklisted for item in parsed_data)
        if blacklisted_exists:
            print("At least one blacklisted item exists in the JSON.")
        else:
            print("No blacklisted items exist in the JSON.")    
        return blacklisted_exists

    # Loop through the video frames
    while cap.isOpened() and not obd_stop_flag:
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame)

            # Visualize the results on the frame
            result = results[0]    
            annotated_frame = result.plot()        

            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Check elapsed time
            elapsed_time = current_time - start_time

            if check_for_blacklisted_object(result.tojson()) and current_time == 0 or elapsed_time >= interval * 60:
                # Set Current time
                current_time = time.time()
                image_bytes = cv2.imencode('.jpg', annotated_frame)[1].tobytes()
                verbose = result.verbose()
                thread_send_image = threading.Thread(target=run_send_image, args=(update, context, image_bytes, verbose))  
                thread_send_image.start()                            

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q") :
                break
            print ("\nobd_stop_flag:"+str(obd_stop_flag))
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows() 

if __name__ == '__main__':
    application = ApplicationBuilder().token(APiToken).build()
    
    start_handler = CommandHandler('start', start)
    stop_handler = CommandHandler('stop', stop)
    application.add_handler(start_handler)
    application.add_handler(stop_handler)
    
    application.run_polling()    