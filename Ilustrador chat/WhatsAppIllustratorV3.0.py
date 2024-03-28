import os
import tkinter as tk
from tkinter import filedialog



def elegir_archivo():
    archivo_txt = filedialog.askopenfilename(parent=ventana_principal, title="Elegir chat", filetypes=(("Archivos de texto", "*.txt"),))
    with open(archivo_txt, 'r', encoding='UTF-8') as f:
        contenido_txt = f.read()
        # Ruta del archivo HTML de salida
    nombre_archivo=str(archivo_txt.split('/')[-1].replace('.txt',''))
    archivo_txt_path= filedialog.askdirectory(parent=ventana_principal, title="Donde quiere guardar el HTML?")
    print(archivo_txt_path)
    directorio = filedialog.askdirectory(parent=ventana_principal, title="Donde estan los archivos MULTIMEDIA?")  # Aquí va el directorio donde se encuentran los archivos multimedia

    ruta_html=archivo_txt_path + '/' + nombre_archivo +'.html'
    print(ruta_html)
    print(archivo_txt_path.split('/')[-1] + '---' + directorio.split('/')[-1] + '---' + directorio.split('/')[-2])

    
    if archivo_txt_path.split('/')[-1] == directorio.split('/')[-1]:
        dirpath= ''
        print("esto es si son iguales"+dirpath)
    else:
        dirpath= directorio.split('/')[-1]+'/'
        print("esto es si son diferentes"+dirpath) 

    


    for nombre_archivo in os.listdir(directorio):
        if nombre_archivo.endswith('.pdf'):
            os.rename(
                os.path.join(directorio, nombre_archivo),
                os.path.join(directorio, nombre_archivo.replace(' ', '_'))
            )
        else:
            print("NO hay archivos pdf")

           

    def extraer_nombres(archivo):
        

        resultados_img = []
        resultados_audio = []
        resultados_video = []
        resultados_sticker=[]
        resultados_pdf=[]
        
        with open(archivo, 'r', encoding='UTF-8') as f:
            lineas = f.readlines()
            
            for i in range(len(lineas)):
                linea = lineas[i].strip()  # Limpia la línea
                if linea:  # Procesa la línea solo si no está vacía
                    nombres = linea.split()
                    for nombre in nombres:
                        nombre_limpio = nombre.replace('\\', '').replace('\u200e', '').replace('<adjunto: ', '').replace('>','')
                        print(nombre_limpio)
                        if nombre_limpio.lower().endswith(".jpg"):
                            resultados_img.append(nombre_limpio)
                        if nombre_limpio.lower().endswith(".opus"):
                            resultados_audio.append(nombre_limpio)
                        if nombre_limpio.lower().endswith(".mp4"):
                            resultados_video.append(nombre_limpio)    
                        if nombre_limpio.lower().endswith(".webp"):
                            resultados_sticker.append(nombre_limpio)
                        
                    if "(archivo adjunto)" in linea.lower():
                        if i+1 < len(lineas):  # Si hay una línea siguiente
                            nombre_adjunto = lineas[i+1].strip()  # Extrae el nombre del archivo de la línea siguiente
                            if ".pdf" in nombre_adjunto.lower() or ".pdf" in linea.lower():
                                nombre_pdf = nombre_adjunto.replace("<Multimedia omitido>/n","").replace("(archivo adjunto)/n", "").strip()  # Extrae sólo el nombre del archivo
                                resultados_pdf.append(nombre_pdf.replace("\u200e",""))  # Añade el nombre del archivo
        
        
        print(resultados_img, resultados_audio, resultados_video, resultados_sticker, resultados_pdf)        
        return resultados_img, resultados_audio, resultados_video, resultados_sticker, resultados_pdf


    def generar_html(resultados_img, resultados_audio, resultados_video, resultados_sticker, resultados_pdf, contenido_txt):
       

        html = '<html>\n'
        html += '<head>\n'
        html += '<title>Chat Ilustrador</title>\n'
        html += '<style>\n'
        html += '* {\n'   
        html += '  font-family: Cambria;\n'
        # html += '  grid-template-columns: repeat(1, 1fr);\n'
        html += '}\n'
        html += 'body {\n' 
        # html += '  background-image: url("whatsapp.jpg");\n'
        # html += '  background-repeat: no-repeat;\n'
        html += '  background-color: rgb(6, 6, 22);\n'
        html += '  color: white;\n'
        html += '}\n'
        html += 'img {\n'
        html += '  width: 30%;\n'
        html += '  display: block;\n'
        html += '  margin: 10px auto;\n'
        html += '}\n'
        html += 'audio {\n'
        html += '  width: 30%;\n'
        html += '  display: block;\n'
        html += '  margin: 10px auto;\n'
        html += '}\n'
        html += 'pre {\n'
        html += '  white-space: pre-wrap;\n'
        html += '  word-wrap: break-word;\n'
        html += '}\n'
        html += '</style>\n'
        html += '<meta name="author" content="Creado por Carolina Soto - licsotocarolina@gmail.com"/>\n'
        html += '<meta name="copyright" content="Derechos reservados."/>\n'
        html += '</head>\n'
        html += '<body>\n'
        html += '<h1>DIVISIÓN CRIMINALÍSTICA CONCORDIA</h1>\n'
        html += '<h2>INFORME TÉCNICO INFORMÁTICO</h2>\n'
        html += '<h1>Chat de whatsapp extraído.</h1>\n'
        html += '<pre>\n'

        
        
        for nombre_img in resultados_img:
            try:
                contenido_txt = contenido_txt.replace('<adjunto: ','').replace(nombre_img, f'<img src="{dirpath}{nombre_img}" alt="{nombre_img}">')
            except:
                pass
        
        for nombre_audio in resultados_audio:
            try:
                contenido_txt = contenido_txt.replace(nombre_audio, f'<audio controls><source src="{dirpath}{nombre_audio}" type="audio/ogg">Your browser does not support the audio element.</audio>')
                print(nombre_audio)
            except:
                print('esta pasando de ponerle nombre a los audios')
                pass
        
        for nombre_video in resultados_video:
            try:
                contenido_txt = contenido_txt.replace(nombre_video, f'<video controls><source src="{dirpath}{nombre_video}" type="video/mp4">Your browser does not support the video element.</video>')
            except:
                pass
        
        for nombre_sticker in resultados_sticker:
            
            try:
                contenido_txt = contenido_txt.replace(nombre_sticker, f'<img src="{dirpath}{nombre_sticker}" alt="{nombre_sticker}">')
            except:
                pass
        
        for nombre_pdf in set(resultados_pdf):
            try:
                nombre_pdf_sin_espacios = nombre_pdf.replace(" ", "_")
                contenido_txt = contenido_txt.replace(nombre_pdf, f'<a href="{dirpath}{nombre_pdf_sin_espacios}" target="_blank">{nombre_pdf}</a>')
            except:
                pass




        html += contenido_txt
        html += '</pre>\n'
        html += '</body>\n'
        html += '</html>\n'
        return html

   

    # Extraer los nombres de archivo que comienzan con el prefijo
    nombres_archivos = extraer_nombres(archivo_txt)
    nombres_archivos_img = nombres_archivos[0]
    nombres_archivos_audio = nombres_archivos[1]
    nombres_archivos_video = nombres_archivos[2]
    nombres_archivos_sticker = nombres_archivos[3]
    nombres_archivos_pdf = nombres_archivos[4]

   
    # Generar el contenido HTML con el texto y las imágenes y archivos de audio encontrados
   
    html = generar_html(nombres_archivos_img, nombres_archivos_audio, nombres_archivos_video, nombres_archivos_sticker, nombres_archivos_pdf, contenido_txt)
  
    
    def mensaje_html(ruta_html):
        
        # Guardar el contenido HTML en el archivo
        try:
            with open(ruta_html, 'w', encoding='UTF-8') as archivo_html:
                archivo_html.write(html)
                etiqueta="El archivo HTML ha sido generado con éxito!"
                mensaje['text']=etiqueta
            return ruta_html
        except:
            etiqueta="Ha ocurrido un error."
            mensaje['text']=etiqueta
        
    
    extraer_nombres(archivo_txt)
    generar_html(nombres_archivos_img, nombres_archivos_audio, nombres_archivos_video, nombres_archivos_sticker, nombres_archivos_pdf, contenido_txt)
    mensaje_html(ruta_html)

# icono='resources/icono.ico'       
# creacion de instancia de ventana tkinter    
ventana_principal = tk.Tk()
ventana_principal.title("Ilustrador de Chat de Whatsapp")
ventana_principal.config(bg="white")
ventana_principal.geometry("580x350")
# ventana_principal.iconbitmap(icono)
bienvenida1=tk.Label(ventana_principal, text="****Bienvenido al Ilustrador de Chat de Whatsapp****")
bienvenida1.place(x=10, y=20)
bienvenida1.config(bg="gray62", fg="purple", font=("Cambria",18))

boton=tk.Button(ventana_principal, text="INICIAR", command=elegir_archivo)
boton.place(x=20, y=120)
boton.config(bg="purple", fg='white', width=53, height=2, font=("Cambria",14))
mensaje=tk.Label(ventana_principal)
mensaje.place(x=100, y=320)
mensaje.config(bg="white", fg="black", font=("Cambria",12))

boton_salir=tk.Button(ventana_principal, text="SALIR", command=ventana_principal.destroy)
boton_salir.config(bg="purple", fg='white', width=53, height=2, font=("Cambria",14))
boton_salir.place(x=20, y=220)

version=tk.Label(ventana_principal, text="V3.0")
version.place(x=530, y=310)
version.config(bg="gray62", fg="purple", font=("Cambria",8))

ventana_principal.mainloop()


