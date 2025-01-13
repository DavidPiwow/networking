import socket
import sys
import time
from urllib.parse import unquote
from sense_hat import SenseHat

display = SenseHat()

def okay_response(msg):
    resp = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
    resp += msg 
    return resp

# why would i not just make it a file? so i can add JAVASCRIPT and be evil <3
def page_get_response(script=""):
     return f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <script>
                {script}
                </script>
                </head>
                <body>
                <h1>hello!</h1>
                <form action="" method="post">
                    <input type="text" name="color" value="(0,0,0)"/>
                    <input type="submit" name="submit" value="Submit"/>
                </form>
                <div>
                <form action="" method="post">
                    <input type="submit" name="close" value="Close"/>
                </form>
                </div>
            </body>
            </html>
            """

def parse_request(buffer):
    msg_str = unquote("".join(buffer))
    if 'color' in msg_str:
        open_p = msg_str.find("color=(")
        close_p = msg_str.find(")",open_p)
        colors = msg_str[open_p+7:close_p].split(",")
        if len(colors)==3:
            try:
                display.clear((int(colors[0]), int(colors[1]), int(colors[2])))
            except ValueError:
                return  page_get_response("alert(\"Please enter in format (R, G, B)\")")
        
    if 'close=Close' in msg_str:
        return """<!DOCTYPE html>
            <html>
                <head>
                    <meta charset="utf-8">
                </head>
                <body>
                    <h1>Goodbye!</h1>
                 </body>
            </html>
            """
                
    return page_get_response()   

def main():
    listen_color = (3, 252, 198)
    wait_color = (252, 227, 3)
    disconnect_color = (158, 3, 60)
    display.low_light = True
    port = 7434
    
    if (len(sys.argv) > 1):
        port = int(sys.argv[1])
    
    cur_socket = socket.socket()
    cur_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    cur_socket.bind(('', port))

    
    cur_socket.listen()
    display.clear(wait_color)
    listening = False    
    while (new_conn := cur_socket.accept()):
        if not listening:
            listening = True
            display.clear(listen_color)
        buffer = []
        new_socket = new_conn[0]
        while (segment := new_socket.recv(4096)): 
            try:
                segment = segment.decode("utf-8")
            finally:
                segment = segment
            
            buffer.append(segment)
        
            if "\r\n\r\n" in segment:
                break
        resp = parse_request(buffer)
        new_socket.send(okay_response(resp).encode("utf-8"))
        new_socket.close()
        
        if "Goodbye" in resp:
            break
                        
        
    cur_socket.close()
    display.show_message("GOODBYE!", text_colour=[255,255,255])
    display.clear()

if __name__ == "__main__":
    main()

